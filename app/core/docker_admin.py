"""Docker'la uygulamanın kendi sürecinden konuşan küçük işler.

Alıştırmanın kendisi denetleyicide çalışıyor (`sandbox/docker_runner.py`).
Burada kalanlar: Docker'ın durumu (Ayarlar), Odyssey'nin bıraktığı
imajları listeleyip silmek ve süresi dolan bir çalıştırmanın arkada
kalan konteynerlerini temizlemek. Denetleyici süre dolunca öldürülüyor ve
kendi temizliğini yapamıyor; o iş buraya düşüyor.

Yalnızca `odyssey=1` etiketli şeylere dokunuluyor; kişinin kendi
imajları ve konteynerleri listelenmiyor da silinmiyor da.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from . import log

CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

# `docker info` Docker Desktop kapalıyken hemen dönüyor; açılırken
# beklemek anlamsız.
INFO_TIMEOUT_SEC = 10
ADMIN_TIMEOUT_SEC = 120


def docker_path() -> str:
    """`docker` komutunun yolu; bulunamazsa boş (denetleyicidekiyle aynı arama)."""
    found = shutil.which("docker")
    if found:
        return found
    for base in (os.environ.get("ProgramFiles", ""), os.environ.get("LOCALAPPDATA", "")):
        if not base:
            continue
        for candidate in (
            Path(base) / "Docker" / "Docker" / "resources" / "bin" / "docker.exe",
            Path(base) / "Programs" / "DockerDesktop" / "resources" / "bin" / "docker.exe",
        ):
            if candidate.is_file():
                return str(candidate)
    return ""


def _call(args: list[str], timeout: float) -> subprocess.CompletedProcess | None:
    exe = docker_path()
    if not exe:
        return None
    try:
        return subprocess.run(
            [exe, *args], capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=timeout, creationflags=CREATE_NO_WINDOW, stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.TimeoutExpired):
        log.get(__name__).exception("docker %s", args[:2])
        return None


def status() -> dict:
    """{"state": "ok" | "missing" | "stopped", "version": "29.8.0"}."""
    if not docker_path():
        return {"state": "missing", "version": ""}
    done = _call(["info", "--format", "{{.ServerVersion}}"], INFO_TIMEOUT_SEC)
    version = (done.stdout.strip() if done else "")
    if done is None or done.returncode != 0 or not version:
        return {"state": "stopped", "version": ""}
    return {"state": "ok", "version": version}


def list_images() -> list[dict]:
    """Odyssey'nin kurduğu imajlar: {"id", "name", "size"} (boyut metin, Docker'ın yazdığı)."""
    done = _call(["images", "--filter", "label=odyssey=1", "--format", "{{json .}}"], ADMIN_TIMEOUT_SEC)
    images = []
    for line in (done.stdout.splitlines() if done and done.returncode == 0 else []):
        try:
            item = json.loads(line)
        except ValueError:
            continue
        images.append({"id": item.get("ID", ""), "name": f"{item.get('Repository', '')}:{item.get('Tag', '')}",
                       "size": item.get("Size", "")})
    return images


def remove_images() -> int:
    """Odyssey'nin imajlarını ve kalan konteynerlerini siler; silinen imaj sayısı."""
    containers = _call(["ps", "-aq", "--filter", "label=odyssey=1"], ADMIN_TIMEOUT_SEC)
    ids = containers.stdout.split() if containers and containers.returncode == 0 else []
    if ids:
        _call(["rm", "-f", "-v", *ids], ADMIN_TIMEOUT_SEC)
    images = list_images()
    if images:
        _call(["rmi", "-f", *{item["id"] for item in images}], ADMIN_TIMEOUT_SEC)
    _call(["image", "prune", "-f", "--filter", "label=odyssey=1"], ADMIN_TIMEOUT_SEC)
    return len(images)


def size_mb(text: str) -> float:
    """Docker'ın yazdığı boyutu (`178MB`, `1.2GB`, `850kB`) megabayta çevirir."""
    text = text.strip()
    for unit, factor in (("GB", 1000.0), ("MB", 1.0), ("kB", 0.001), ("B", 0.000001)):
        if text.endswith(unit):
            try:
                return float(text[: -len(unit)]) * factor
            except ValueError:
                return 0.0
    return 0.0


# Alıştırmaların `FROM` satırlarındaki iki hazır imaj (Kurulum bölümü
# çektiriyor). Silinirse sonraki Docker alıştırmasında yeniden iniyor.
BASE_IMAGES = ("python:3.13-slim", "alpine:3.22")


def list_base_images() -> list[dict]:
    """Bilgisayarda duran taban imajlar: {"id", "name", "size"}."""
    done = _call(["images", "--format", "{{json .}}"], ADMIN_TIMEOUT_SEC)
    images = []
    for line in (done.stdout.splitlines() if done and done.returncode == 0 else []):
        try:
            item = json.loads(line)
        except ValueError:
            continue
        name = f"{item.get('Repository', '')}:{item.get('Tag', '')}"
        if name in BASE_IMAGES:
            images.append({"id": item.get("ID", ""), "name": name, "size": item.get("Size", "")})
    return images


def remove_base_images() -> int:
    """Taban imajları siler (kullanan konteyner varsa Docker reddediyor)."""
    images = list_base_images()
    if images:
        _call(["rmi", *[item["name"] for item in images]], ADMIN_TIMEOUT_SEC)
    return len(images) - len(list_base_images())


def build_cache_mb() -> float:
    """Derleme önbelleğinin kapladığı yer (bütün projelerin ortak önbelleği)."""
    done = _call(["system", "df", "--format", "{{json .}}"], ADMIN_TIMEOUT_SEC)
    for line in (done.stdout.splitlines() if done and done.returncode == 0 else []):
        try:
            item = json.loads(line)
        except ValueError:
            continue
        if item.get("Type") == "Build Cache":
            return size_mb(str(item.get("Size", "")))
    return 0.0


def prune_build_cache() -> None:
    """Kullanılmayan derleme önbelleğinin tamamını siler.

    Önbellek etiketle ayrılamıyor; kişinin kendi projelerinin önbelleği de
    gidiyor. Zararı yok: o projeler bir sonraki derlemede biraz yavaş kurulur.
    """
    _call(["builder", "prune", "-a", "-f"], ADMIN_TIMEOUT_SEC)


# --- Docker Desktop'ı kapatmak ---------------------------------------------
#
# Docker Desktop açık kaldıkça bellek tutuyor (WSL sanal makinesi). Kişi onu
# yalnızca Odyssey için açmış olabilir ve kapatmayı unutur; bu oturumda bir
# Docker alıştırması çalıştıysa ve ayar açıksa Odyssey kapanırken kapatılıyor.

AUTOSTOP_KEY = "docker_autostop"
_used_this_session = False


def mark_used() -> None:
    """Bu oturumda bir Docker alıştırması çalıştı (runner çağırıyor)."""
    global _used_this_session
    _used_this_session = True


def used_this_session() -> bool:
    return _used_this_session


def autostop_enabled(store) -> bool:
    return store.setting(AUTOSTOP_KEY, "1") != "0"


def set_autostop(store, enabled: bool) -> None:
    store.set_setting(AUTOSTOP_KEY, "1" if enabled else "0")


def stop_desktop() -> bool:
    """Docker Desktop'a kapanmasını söyler; beklemez (Odyssey'nin kapanışı uzamasın).

    `docker desktop stop` Docker Desktop 4.37'den beri var; eski sürümde komut
    yok ve hiçbir şey olmuyor.
    """
    exe = docker_path()
    if not exe:
        return False
    flags = CREATE_NO_WINDOW
    if sys.platform == "win32":
        flags |= subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    try:
        subprocess.Popen(  # noqa: S603 — sabit komut
            [exe, "desktop", "stop", "--detach"], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, creationflags=flags, close_fds=True,
        )
    except OSError:
        log.get(__name__).exception("docker desktop stop")
        return False
    return True


def stop_if_used(store) -> bool:
    """Odyssey kapanırken: bu oturumda Docker kullanıldıysa ve ayar açıksa kapat."""
    if not (_used_this_session and autostop_enabled(store)):
        return False
    return stop_desktop()


def cleanup_run(run_id: str) -> None:
    """Süresi dolan çalıştırmanın konteynerlerini, ağlarını ve volume'larını siler."""
    if not docker_path() or not run_id:
        return
    project = f"odyssey-{run_id}"
    for label in (f"odyssey.run={run_id}", f"com.docker.compose.project={project}"):
        done = _call(["ps", "-aq", "--filter", f"label={label}"], 30)
        ids = done.stdout.split() if done and done.returncode == 0 else []
        if ids:
            _call(["rm", "-f", "-v", *ids], 60)
    for kind in ("network", "volume"):
        for label in (f"com.docker.compose.project={project}", f"odyssey.run={run_id}"):
            done = _call([kind, "ls", "-q", "--filter", f"label={label}"], 30)
            ids = done.stdout.split() if done and done.returncode == 0 else []
            if ids:
                _call([kind, "rm", *ids], 60)
