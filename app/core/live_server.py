"""API 2: kişinin FastAPI uygulamasını gerçekten çalıştırmak ("Sunucuyu başlat").

Denetim uygulamayı sunucusuz çağırıyor (`sandbox/fastapi_sandbox.py`); ama
kişi yazdığı API'yi tarayıcıda, `/docs` sayfasında ya da Postman gibi bir
araçla denemek isteyebilir. Burada uygulama denetleyici sürecinde
`uvicorn` ile `127.0.0.1`'de boş bir portta açılıyor: yalnızca bu bilgisayardan
ulaşılıyor, güvenlik duvarı sormuyor. Süreç alıştırmalardaki gibi bellek
sınırlı bir işte; alıştırma değişince, durdurulunca ya da Odyssey kapanınca
öldürülüyor.

Swagger UI dosyaları `app/resources/swagger-ui/` altında varsa `/docs`
internetsiz açılıyor; yoksa FastAPI'nin kendi sayfası (internet ister).
"""

from __future__ import annotations

import atexit
import json
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from . import log
from .memory_limit import CREATE_SUSPENDED, MemoryJob
from .runner import _child_env, _harness_command, _kill_tree, _prepare_workspace, _write_files
from ..paths import install_root

READY_TIMEOUT_SEC = 20
LOG_TAIL_CHARS = 3000

_running: list["LiveServer"] = []


def docs_dir() -> Path:
    return install_root() / "app" / "resources" / "swagger-ui"


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


class LiveServer:
    """Açılmış bir uygulama sunucusu."""

    def __init__(self, process: subprocess.Popen, job: MemoryJob | None, workspace: Path, port: int,
                 log_path: Path) -> None:
        self.process = process
        self._job = job
        self.workspace = workspace
        self.port = port
        self.log_path = log_path

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def running(self) -> bool:
        return self.process.poll() is None

    def wait_ready(self, timeout: float = READY_TIMEOUT_SEC) -> bool:
        """`/openapi.json` cevap verene kadar bekler; süreç biterse hemen döner."""
        until = time.monotonic() + timeout
        while time.monotonic() < until:
            if not self.running():
                return False
            try:
                with urllib.request.urlopen(f"{self.url}/openapi.json", timeout=1):
                    return True
            except OSError:
                time.sleep(0.2)
        return False

    def log_tail(self) -> str:
        try:
            text = self.log_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return ""
        return text[-LOG_TAIL_CHARS:]

    def stop(self) -> None:
        if self.running():
            _kill_tree(self.process)
        if self._job is not None:
            self._job.close()
            self._job = None
        shutil.rmtree(self.workspace, ignore_errors=True)
        if self in _running:
            _running.remove(self)


def start(files: dict[str, str], exercise_dir: Path | None, entry: str, *, module: str = "",
          app: str = "app") -> LiveServer:
    """Dosyaları geçici klasöre yazar ve uygulamayı ayrı süreçte açar."""
    workspace = _prepare_workspace(exercise_dir)
    _write_files(workspace, files)
    port = free_port()
    job_path = workspace / "job.json"
    log_path = workspace / "server.log"
    job_path.write_text(json.dumps({
        "serve": True, "workspace": str(workspace), "entry": entry, "module": module, "app": app,
        "port": port, "docs_dir": str(docs_dir()), "result_path": str(workspace / "result.json"),
    }, ensure_ascii=False), encoding="utf-8")

    flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    job = MemoryJob.create()
    if job is not None:
        flags |= CREATE_SUSPENDED
    handle = log_path.open("w", encoding="utf-8")
    try:
        process = subprocess.Popen(  # noqa: S603 — denetleyici, sabit komut
            _harness_command(job_path), cwd=workspace, stdout=handle, stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL, creationflags=flags, env=_child_env(),
        )
    finally:
        handle.close()
    if job is not None:
        job.attach(process)
    server = LiveServer(process, job, workspace, port, log_path)
    _running.append(server)
    return server


def stop_all() -> None:
    """Açık bütün sunucuları kapatır (Odyssey kapanırken)."""
    for server in list(_running):
        try:
            server.stop()
        except Exception:  # noqa: BLE001 - kapanışta hiçbir şey programı durdurmasın
            log.get(__name__).exception("Sunucu kapatılamadı")


atexit.register(stop_all)
