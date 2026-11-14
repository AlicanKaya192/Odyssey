"""macOS bildirimi ve "program açık" kilidi (seri hatırlatmaları için).

- **Bildirim:** sistemle gelen `osascript` ile `display notification`.
  Başlık ve metin betiğin içine yazılmıyor, argüman olarak veriliyor; tırnak
  ya da AppleScript sözcüğü içeren metin betiği bozamıyor. İmzasız bir
  uygulama kendi adına bildirim izni alamadığı için bildirim macOS'ta
  "Script Editor" (Komut Dosyası Düzenleyicisi) adıyla görünüyor.
- **Kilit:** açık uygulama veri klasöründeki `running.lock` dosyasını
  `fcntl.flock` ile tutuyor; süreç kapanınca kilit kendiliğinden kalkıyor.
  Hatırlatma denetleyicisi kilidi alamıyorsa program açık demek.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from ..paths import user_data_dir

OSASCRIPT = "/usr/bin/osascript"
SCRIPT = (
    "on run argv",
    "display notification (item 2 of argv) with title (item 1 of argv)",
    "end run",
)
LOCK_NAME = "running.lock"

_lock_file = None


def _osascript_exists() -> bool:
    return Path(OSASCRIPT).exists()


def supported() -> bool:
    return sys.platform == "darwin" and _osascript_exists()


def show(title: str, body: str) -> bool:
    """Bildirimi gösterir; gösterildiyse True."""
    if not supported():
        return False
    komut = [OSASCRIPT]
    for satir in SCRIPT:
        komut += ["-e", satir]
    komut += [title, body]
    try:
        sonuc = subprocess.run(komut, capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return False
    return sonuc.returncode == 0


def _lock_path() -> Path:
    return user_data_dir() / LOCK_NAME


def claim_running() -> None:
    """Uygulama açıkken tutulan kilidi alır."""
    global _lock_file
    if sys.platform != "darwin" or _lock_file is not None:
        return
    import fcntl

    try:
        dosya = open(_lock_path(), "a")
    except OSError:
        return
    try:
        fcntl.flock(dosya.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        dosya.close()
        return
    _lock_file = dosya


def app_running() -> bool:
    """Odyssey başka bir süreçte açık mı?"""
    if sys.platform != "darwin":
        return False
    import fcntl

    yol = _lock_path()
    if not yol.exists():
        return False
    try:
        dosya = open(yol, "a")
    except OSError:
        return False
    try:
        fcntl.flock(dosya.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return True
    else:
        fcntl.flock(dosya.fileno(), fcntl.LOCK_UN)
        return False
    finally:
        dosya.close()
