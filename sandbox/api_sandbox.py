"""API alıştırmalarının sunucusu: denetleyicinin içinde, yalnızca bu bilgisayarda.

Alıştırma klasöründe `api_routes.py` varsa denetleyici, kullanıcının kodunu
çalıştırmadan önce bu sunucuyu açıyor. Kullanıcı gerçek bir adres yazıyor:

    http://api.odyssey.test/books

`.test` uzantısı dünyada hiçbir siteye ait değil (internette ayrılmış bir ad).
Bu süreçte o ad `127.0.0.1` ve sunucunun rastgele seçilen portuna
yönlendiriliyor (`socket.getaddrinfo` sarılıyor); istek bilgisayardan
çıkmıyor, güvenlik duvarı sormuyor, aynı anda çalışan iki alıştırma
birbirinin portunu kullanmıyor. `requests` de `urllib` de gerçek bir
soketle konuşuyor: zaman aşımı, 404, 429 gerçekten yaşanıyor.

`api_routes.py` sözleşmesi:

    def handle(request):
        # request.method, .path, .query (ad → son değer), .query_all
        # (ad → liste), .headers (küçük harfli adlar), .body (metin),
        # .json (gövde JSON ise ayrıştırılmış hâli, değilse None)
        return 200, {"id": 1}                    # durum, gövde
        return 404, {"error": "..."}, {"Retry-After": "2"}   # + başlıklar

Gövde sözlük ya da listeyse JSON, metinse düz metin, `None` ise boş gidiyor.
Başlıklardaki `X-Delay` (saniye) yanıtı geciktiriyor; zaman aşımı
alıştırmaları için. Modülün durumu (kayıtlar, sayaçlar) her çalıştırmada
baştan kuruluyor.

Gelen her istek kayda giriyor (`log`): `requests` kontrolü ve terminaldeki
`→ GET /books 200` satırları buradan.
"""

from __future__ import annotations

import importlib.util
import json
import os
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

API_HOST = "api.odyssey.test"
ROUTES_FILE = "api_routes.py"
# Kayıtta gövdenin en fazla bu kadarı tutuluyor.
MAX_LOGGED_BODY = 2000


class ApiRequest:
    """Sunucuya gelen bir istek; `api_routes.handle` bunu alıyor."""

    def __init__(self, method: str, target: str, headers: dict, body: str) -> None:
        parts = urlsplit(target)
        self.method = method
        self.path = parts.path
        self.query_all = parse_qs(parts.query, keep_blank_values=True)
        self.query = {name: values[-1] for name, values in self.query_all.items()}
        self.headers = headers
        self.body = body
        try:
            self.json = json.loads(body) if body else None
        except ValueError:
            self.json = None


class ApiServer:
    """Arka planda çalışan sunucu ve gelen isteklerin kaydı."""

    def __init__(self, routes_path: Path) -> None:
        spec = importlib.util.spec_from_file_location("_odyssey_api_routes", routes_path)
        self.routes = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.routes)
        self.log: list[dict] = []
        self._started = time.monotonic()
        self._lock = threading.Lock()
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), self._handler_class())
        self._server.daemon_threads = True
        self.port = self._server.server_address[1]
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    def _handler_class(self):
        owner = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def _serve(self) -> None:
                length = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(length).decode("utf-8", "replace") if length else ""
                headers = {name.lower(): value for name, value in self.headers.items()}
                request = ApiRequest(self.command, self.path, headers, body)
                entry = {
                    "method": request.method,
                    "path": request.path,
                    "query": request.query,
                    "headers": headers,
                    "body": body[:MAX_LOGGED_BODY],
                    "json": request.json,
                    "t": round(time.monotonic() - owner._started, 3),
                    "status": 500,
                }
                with owner._lock:
                    owner.log.append(entry)
                try:
                    result = owner.routes.handle(request)
                except Exception as exc:  # alıştırma sunucusunun hatası: 500
                    result = (500, {"error": "server error", "detail": str(exc)})
                status, payload, extra = _normalise(result)
                entry["status"] = status
                delay = float(extra.pop("X-Delay", 0) or 0)
                if delay:
                    time.sleep(delay)
                if isinstance(payload, (dict, list)):
                    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
                    content_type = "application/json; charset=utf-8"
                elif payload is None:
                    data, content_type = b"", ""
                else:
                    data = str(payload).encode("utf-8")
                    content_type = "text/plain; charset=utf-8"
                try:
                    self.send_response(status)
                    if content_type:
                        self.send_header("Content-Type", content_type)
                    for name, value in extra.items():
                        self.send_header(name, str(value))
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    if self.command != "HEAD":
                        self.wfile.write(data)
                except OSError:
                    # İstemci beklemeden gitti (zaman aşımı): yazacak yer yok.
                    pass

            do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = do_HEAD = do_OPTIONS = _serve

            def log_message(self, *_args) -> None:  # noqa: D102
                return

        return Handler

    def start(self) -> None:
        self._thread.start()
        _route_host(self.port)

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()

    def summary(self) -> list[dict]:
        """Sonuca yazılan kayıt (başlıklar ve gövde dahil)."""
        with self._lock:
            return [dict(entry) for entry in self.log]


def _normalise(result) -> tuple[int, object, dict]:
    if isinstance(result, tuple):
        status = int(result[0])
        payload = result[1] if len(result) > 1 else None
        extra = dict(result[2]) if len(result) > 2 and result[2] else {}
        return status, payload, extra
    return 200, result, {}


_original_getaddrinfo = socket.getaddrinfo


def _route_host(port: int) -> None:
    """`api.odyssey.test` adını bu süreçte sunucuya yönlendirir."""

    def getaddrinfo(host, service, *args, **kwargs):
        if isinstance(host, (bytes, bytearray)):
            host = host.decode("ascii", "ignore")
        if isinstance(host, str) and host.lower().rstrip(".") == API_HOST:
            return [(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", ("127.0.0.1", port))]
        return _original_getaddrinfo(host, service, *args, **kwargs)

    socket.getaddrinfo = getaddrinfo
    # Bilgisayarda bir vekil sunucu (proxy) ayarlıysa istekler ona gitmesin.
    yok = os.environ.get("NO_PROXY", "")
    os.environ["NO_PROXY"] = ",".join(filter(None, [yok, API_HOST, "127.0.0.1", "localhost"]))
    os.environ["no_proxy"] = os.environ["NO_PROXY"]


def start_if_present(workspace: Path) -> ApiServer | None:
    """Çalışma klasöründe `api_routes.py` varsa sunucuyu açar."""
    path = workspace / ROUTES_FILE
    if not path.exists():
        return None
    server = ApiServer(path)
    server.start()
    return server


def _matches(entry: dict, check: dict) -> bool:
    if check.get("method") and entry["method"].upper() != str(check["method"]).upper():
        return False
    if check.get("path") and entry["path"] != check["path"]:
        return False
    for name, value in (check.get("query") or {}).items():
        if str(entry["query"].get(name)) != str(value):
            return False
    for name in check.get("no_query") or []:
        if name in entry["query"]:
            return False
    for name, value in (check.get("headers") or {}).items():
        if entry["headers"].get(name.lower()) != str(value):
            return False
    if "json" in check and entry.get("json") != check["json"]:
        return False
    return True


def check_requests(check: dict, log: list[dict]) -> dict:
    """`requests` kontrolü: kayıtta tarife uyan istek sayısı (ve aralığı).

    `min` (varsayılan 1) ve `max` sayıyı sınırlıyor; `min_gap` uyan
    ardışık iki istek arasında en az kaç saniye geçmesi gerektiğini
    söylüyor (beklemeden yeniden deneyen kod düşsün).
    """
    found = [entry for entry in log if _matches(entry, check)]
    count = len(found)
    low = int(check.get("min", 1))
    high = check.get("max")
    passed = count >= low and (high is None or count <= int(high))
    detail = {
        "method": str(check.get("method", "")).upper(),
        "path": check.get("path", ""),
        "count": count,
        "min": low,
        "max": high,
        "total": len(log),
    }
    gap = check.get("min_gap")
    if passed and gap is not None and len(found) > 1:
        smallest = min(b["t"] - a["t"] for a, b in zip(found, found[1:]))
        detail["gap"] = round(smallest, 2)
        detail["min_gap"] = gap
        passed = smallest + 0.05 >= float(gap)
    return {"passed": passed, "detail": detail}
