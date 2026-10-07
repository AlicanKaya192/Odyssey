"""API 2 alıştırmaları: kişinin FastAPI uygulamasını sunucu açmadan denetlemek.

`http` kontrolü uygulama nesnesini (`app`) `TestClient` ile süreç içinde
çağırıyor: port açılmıyor, ağ yok, güvenlik duvarı sormuyor. Adımlar sırayla
uygulanıyor ve durum taşınıyor (önce `POST`, sonra aynı kaydı `GET`);
bir adımın yanıtından değer saklanıp sonraki adımın adresinde kullanılabiliyor.

`pytest` kontrolü kişinin yazdığı testleri aynı süreçte çalıştırıyor.
`mutants` verilirse uygulamanın bilerek bozulmuş bir hâliyle testler yeniden
çalıştırılıyor: iyi bir test bozuk kodu yakalamalı (en az biri düşmeli).

Sonuç Docker kontrolleri gibi `{"reason", "values"}`; arayüz metni
`check.http.<sebep>` / `check.pytest.<sebep>`.
"""

from __future__ import annotations

import contextlib
import importlib
import io
import json
import sys
import traceback
from pathlib import Path

ANY = "<any>"
BODY_PREVIEW = 300
# İstek panelinde gösterilen yanıtın en fazla uzunluğu.
CAPTURE_LIMIT = 20000


def _fail(reason: str, **values) -> dict:
    return {"passed": False, "detail": {"reason": reason, "values": values}}


def _ok(**values) -> dict:
    return {"passed": True, "detail": {"reason": "", "values": values}}


def guard_uvicorn(sources: list[str]) -> None:
    """`uvicorn.run(app)` denetimi sonsuza kadar bekletmesin.

    Kişi dosyasının sonuna `if __name__ == "__main__": uvicorn.run(app)`
    yazabilir (derste de öyle). Denetleyici giriş dosyasını `__main__` olarak
    çalıştırdığı için sunucu açılır ve süre dolana kadar asılı kalırdı. Burada
    `run` hiçbir şey yapmayan bir işleve çevriliyor; denetim uygulamayı
    sunucusuz çağırıyor.
    """
    if not any("uvicorn" in source for source in sources):
        return
    try:
        import uvicorn
    except ImportError:
        return
    uvicorn.run = lambda *args, **kwargs: None


def _short(value) -> str:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    text = " ".join(str(text).split())
    return text if len(text) <= BODY_PREVIEW else text[: BODY_PREVIEW - 1] + "…"


def _user_line(exc: BaseException, workspace: Path) -> tuple[str, int]:
    """Hatanın kişinin dosyalarındaki son satırı: (dosya adı, satır)."""
    root = str(workspace.resolve()).lower()
    found = ("", 0)
    for frame in traceback.extract_tb(exc.__traceback__):
        path = str(Path(frame.filename).resolve()).lower()
        if path.startswith(root):
            found = (Path(frame.filename).name, frame.lineno or 0)
    return found


def _find_app(check: dict, namespace: dict):
    """Kontrolün baktığı uygulama: giriş dosyasındaki ad ya da `module` içindeki."""
    name = str(check.get("app", "app"))
    module = check.get("module")
    if module:
        try:
            space = vars(importlib.import_module(str(module)))
        except Exception as exc:  # noqa: BLE001 - kişinin modülü her şeyi atabilir
            return None, _fail("import_error", module=module, error=f"{type(exc).__name__}: {exc}")
    else:
        space = namespace
    app = space.get(name)
    if app is None:
        return None, _fail("no_app", name=name)
    if not callable(app) or not hasattr(app, "routes"):
        return None, _fail("not_app", name=name, kind=type(app).__name__)
    return app, None


def _fill(value, saved: dict):
    """Adres ve gövdedeki `{ad}` yer tutucularını saklanan değerlerle doldurur."""
    if isinstance(value, str):
        for key, saved_value in saved.items():
            value = value.replace("{" + key + "}", str(saved_value))
        return value
    if isinstance(value, dict):
        return {k: _fill(v, saved) for k, v in value.items()}
    if isinstance(value, list):
        return [_fill(v, saved) for v in value]
    return value


def _matches(expected, actual) -> bool:
    """`json_has`: beklenen alanlar gelen yanıtta aynı değerle var mı (`<any>` her değer)."""
    if expected == ANY:
        return True
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            key in actual and _matches(value, actual[key]) for key, value in expected.items()
        )
    if isinstance(expected, list):
        return isinstance(actual, list) and len(expected) == len(actual) and all(
            _matches(e, a) for e, a in zip(expected, actual)
        )
    return expected == actual


def check_http(check: dict, namespace: dict, workspace: Path, log: list[dict]) -> dict:
    """Adımları sırayla uygular; ilk tutmayan adımda durur."""
    app, error = _find_app(check, namespace)
    if error:
        return error
    try:
        from fastapi.testclient import TestClient
    except ImportError as exc:
        return _fail("no_fastapi", error=str(exc))

    saved: dict = {}
    steps = check.get("steps") or []
    try:
        client_cm = TestClient(app)
        client = client_cm.__enter__()
    except Exception as exc:  # noqa: BLE001 - açılışta (lifespan) kişinin kodu patlayabilir
        dosya, satir = _user_line(exc, workspace)
        return _fail("startup_error_at" if dosya else "startup_error", error=f"{type(exc).__name__}: {exc}",
                     file=dosya, line=satir)
    try:
        for index, step in enumerate(steps, start=1):
            method = str(step.get("method", "GET")).upper()
            path = _fill(str(step.get("path", "/")), saved)
            request = f"{method} {path}"
            kwargs = {}
            for key in ("json", "params", "headers", "data"):
                if key in step:
                    kwargs[key] = _fill(step[key], saved)
            try:
                response = client.request(method, path, **kwargs)
            except Exception as exc:  # noqa: BLE001 - uç noktanın içindeki hata
                dosya, satir = _user_line(exc, workspace)
                log.append({"method": method, "path": path.split("?")[0], "query": {}, "status": 500})
                return _fail("server_error_at" if dosya else "server_error", step=index, request=request,
                             error=f"{type(exc).__name__}: {exc}", file=dosya, line=satir)
            log.append({"method": method, "path": path.split("?")[0],
                        "query": dict(kwargs.get("params") or {}), "status": response.status_code})
            try:
                body = response.json()
                is_json = True
            except ValueError:
                body = response.text
                is_json = False

            expect = step.get("expect") or {}
            if "status" in expect and response.status_code != int(expect["status"]):
                return _fail("status", step=index, request=request, expected=int(expect["status"]),
                             actual=response.status_code, body=_short(body))
            if "json" in expect:
                if not is_json:
                    return _fail("not_json", step=index, request=request, actual=_short(body))
                if body != expect["json"]:
                    return _fail("json", step=index, request=request,
                                 expected=json.dumps(expect["json"], ensure_ascii=False),
                                 actual=json.dumps(body, ensure_ascii=False))
            if "json_has" in expect:
                if not is_json:
                    return _fail("not_json", step=index, request=request, actual=_short(body))
                if not _matches(expect["json_has"], body):
                    return _fail("json_has", step=index, request=request,
                                 expected=json.dumps(expect["json_has"], ensure_ascii=False),
                                 actual=json.dumps(body, ensure_ascii=False))
            if "json_len" in expect:
                count = len(body) if isinstance(body, (list, dict)) else -1
                if count != int(expect["json_len"]):
                    return _fail("json_len", step=index, request=request, expected=int(expect["json_len"]),
                                 actual=count)
            if "contains" in expect and str(expect["contains"]) not in response.text:
                return _fail("contains", step=index, request=request, expected=str(expect["contains"]),
                             actual=_short(response.text))
            for header, value in (expect.get("headers") or {}).items():
                got = response.headers.get(header)
                if got is None or (value != ANY and str(value) not in got):
                    return _fail("header", step=index, request=request, header=header,
                                 expected=str(value), actual=got or "—")
            for name, field in (step.get("save") or {}).items():
                if isinstance(body, dict) and field in body:
                    saved[name] = body[field]
            if step.get("capture"):
                # İstek paneli: yanıtın kendisi gösteriliyor (kontrol değil).
                text = json.dumps(body, ensure_ascii=False, indent=2) if is_json else response.text
                return _ok(status=response.status_code, request=request, body=text[:CAPTURE_LIMIT],
                           content_type=response.headers.get("content-type", ""))
    finally:
        with contextlib.suppress(Exception):
            client_cm.__exit__(None, None, None)
    return _ok(steps=len(steps))


# --- pytest -----------------------------------------------------------------


class _Collector:
    """Test sonuçlarını toplayan küçük pytest eklentisi."""

    def __init__(self) -> None:
        self.passed: list[str] = []
        self.failed: list[tuple[str, str]] = []
        self.collect_errors: list[str] = []

    def pytest_runtest_logreport(self, report) -> None:  # noqa: D102
        name = report.nodeid.split("::")[-1]
        if report.when == "call" and report.passed:
            self.passed.append(name)
        elif report.failed:
            crash = getattr(report.longrepr, "reprcrash", None)
            message = getattr(crash, "message", "") or str(report.longrepr).strip().splitlines()[-1:]
            self.failed.append((name, _short(message if isinstance(message, str) else " ".join(message))))

    def pytest_collectreport(self, report) -> None:  # noqa: D102
        if report.failed:
            text = str(report.longrepr).strip().splitlines()
            self.collect_errors.append(_short(text[-1] if text else ""))


def _forget_workspace_modules(workspace: Path) -> None:
    """Çalışma klasöründen içe aktarılmış modülleri unutur (bozuk hâl yeniden okunsun)."""
    root = str(workspace.resolve()).lower()
    for name, module in list(sys.modules.items()):
        path = getattr(module, "__file__", None)
        if path and str(Path(path).resolve()).lower().startswith(root):
            del sys.modules[name]


def _run_pytest(files: list[str], workspace: Path) -> tuple[_Collector, int, str]:
    import pytest

    collector = _Collector()
    buffer = io.StringIO()
    args = [*files, "-q", "-p", "no:cacheprovider", "--no-header", "-o", "console_output_style=classic",
            "--rootdir", str(workspace), "-W", "ignore::DeprecationWarning"]
    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
        code = pytest.main(args, plugins=[collector])
    return collector, int(code), buffer.getvalue()


def check_pytest(check: dict, workspace: Path) -> dict:
    """Kişinin testleri: hepsi geçmeli, en az `min` test olmalı, bozuk kodu yakalamalı."""
    try:
        import pytest  # noqa: F401
    except ImportError as exc:
        return _fail("no_pytest", error=str(exc))
    files = [str(f) for f in (check.get("files") or [check.get("file", "test_main.py")])]
    for name in files:
        if not (workspace / name).is_file():
            return _fail("no_file", file=name)

    _forget_workspace_modules(workspace)
    collector, _code, _out = _run_pytest(files, workspace)
    if collector.collect_errors:
        return _fail("collect_error", error=collector.collect_errors[0])
    total = len(collector.passed) + len(collector.failed)
    if total == 0:
        return _fail("no_tests", file=files[0])
    if collector.failed:
        name, message = collector.failed[0]
        return _fail("failed", count=len(collector.failed), total=total, name=name, error=message)
    low = int(check.get("min", 1))
    if total < low:
        return _fail("too_few", count=total, min=low)

    # Bozuk sürümler: testlerden en az biri düşmeli.
    for mutant in check.get("mutants") or []:
        target = workspace / str(mutant["file"])
        original = target.read_text(encoding="utf-8")
        try:
            target.write_text(str(mutant["source"]), encoding="utf-8")
            _forget_workspace_modules(workspace)
            caught, _c, _o = _run_pytest(files, workspace)
        finally:
            target.write_text(original, encoding="utf-8")
            _forget_workspace_modules(workspace)
        if not caught.failed and not caught.collect_errors:
            # `bug` iki dilli olabilir ({tr, en}); dili grader seçiyor.
            bug = mutant.get("bug", "")
            return _fail("missed_bug", bug=bug if isinstance(bug, dict) else str(bug), total=total)
    return _ok(count=total)


# --- Sunucuyu başlat ----------------------------------------------------------


def _local_docs(app, docs_dir: Path) -> bool:
    """`/docs` sayfasını pakete konan Swagger UI dosyalarıyla sunar.

    FastAPI'nin kendi `/docs` sayfası betiği ve stili internetten (CDN)
    yüklüyor; internet yoksa sayfa boş kalıyor. Dosyalar pakette varsa o
    yol kaldırılıp aynı sayfa yerel dosyalarla kuruluyor.
    """
    js, css = docs_dir / "swagger-ui-bundle.js", docs_dir / "swagger-ui.css"
    if not (js.is_file() and css.is_file()) or not getattr(app, "docs_url", None):
        return False
    from fastapi.openapi.docs import get_swagger_ui_html
    from starlette.staticfiles import StaticFiles

    yol = app.docs_url
    app.router.routes = [r for r in app.router.routes if getattr(r, "path", None) != yol]
    app.mount("/_odyssey-docs", StaticFiles(directory=str(docs_dir)), name="odyssey-docs")

    @app.get(yol, include_in_schema=False)
    def _docs():
        return get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title + " - Swagger UI",
                                   swagger_js_url="/_odyssey-docs/swagger-ui-bundle.js",
                                   swagger_css_url="/_odyssey-docs/swagger-ui.css",
                                   swagger_favicon_url="/_odyssey-docs/favicon.png")
    return True


def serve(job: dict) -> int:
    """Kişinin uygulamasını `127.0.0.1:<port>`'ta uvicorn ile açar (öldürülene kadar)."""
    workspace = Path(job["workspace"]).resolve()
    if str(workspace) not in sys.path:
        sys.path.insert(0, str(workspace))
    import os

    os.chdir(workspace)
    module = str(job.get("module") or Path(job.get("entry") or "main.py").stem)
    name = str(job.get("app", "app"))
    try:
        app = getattr(importlib.import_module(module), name)
    except Exception:  # noqa: BLE001 - kişinin kodu her şeyi atabilir; günlüğe yazılıyor
        traceback.print_exc()
        return 1
    _local_docs(app, Path(job.get("docs_dir") or ""))
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=int(job["port"]), log_level="info")
    return 0
