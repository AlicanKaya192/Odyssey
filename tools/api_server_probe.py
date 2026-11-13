"""Alıştırma sunucusunu (`sandbox/api_sandbox.py`) tek başına deneyip adım
adım süre ölçer; takılırsa yığın dökümü basar.

Mac'te API 1 alıştırmalarının hepsi süre aşımına düştü (13 Kasım, CI); bu
araç nerede beklendiğini gösteriyor. Kullanım: api_server_probe.py
"""
from __future__ import annotations

import faulthandler
import socket
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sandbox"))

import api_sandbox  # noqa: E402

ROUTES = '''
def handle(request):
    return 200, {"ok": True, "path": request.path}
'''


def adim(ad: str, baslangic: float) -> float:
    simdi = time.monotonic()
    print(f"{ad:28} {simdi - baslangic:6.2f} sn", flush=True)
    return simdi


def main() -> int:
    faulthandler.dump_traceback_later(25, exit=True)
    t = time.monotonic()
    print("hostname:", socket.gethostname(), flush=True)
    t = adim("gethostname", t)
    with tempfile.TemporaryDirectory() as klasor:
        (Path(klasor) / api_sandbox.ROUTES_FILE).write_text(ROUTES, encoding="utf-8")
        server = api_sandbox.start_if_present(Path(klasor))
        t = adim("sunucu açıldı", t)
        print("adres:", socket.getaddrinfo(api_sandbox.API_HOST, 80)[0][4], flush=True)
        t = adim("getaddrinfo(api)", t)
        import urllib.request
        print("proxies:", urllib.request.getproxies(), flush=True)
        t = adim("getproxies", t)
        with urllib.request.urlopen(f"http://{api_sandbox.API_HOST}/books", timeout=10) as cevap:
            print("urllib:", cevap.status, cevap.read()[:60], flush=True)
        t = adim("urllib isteği", t)
        import requests
        t = adim("import requests", t)
        cevap = requests.get(f"http://{api_sandbox.API_HOST}/books", timeout=10)
        print("requests:", cevap.status_code, cevap.text[:60], flush=True)
        adim("requests isteği", t)
        if hasattr(server, "stop"):
            server.stop()
    faulthandler.cancel_dump_traceback_later()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
