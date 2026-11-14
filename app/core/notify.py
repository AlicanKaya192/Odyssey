"""Sistem bildirimi ve "program açık" kilidi: Windows ya da macOS.

Windows'ta `win_notify` (bildirim, `odyssey://` kaydı, adlı kilit), macOS'ta
`mac_notify` (`osascript`, dosya kilidi). Çağıranlar (hatırlatmalar,
zamanlayıcı bildirimi, açılış) platformu bilmiyor.
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import mac_notify, win_notify


def supported() -> bool:
    return win_notify.supported() or mac_notify.supported()


def show(title: str, body: str, icon_path: Path | None = None) -> bool:
    """Bildirimi gösterir; gösterildiyse True. macOS'ta simge kullanılmıyor."""
    if sys.platform == "darwin":
        return mac_notify.show(title, body)
    return win_notify.show_toast(title, body, icon_path)


def claim_running() -> None:
    if sys.platform == "darwin":
        mac_notify.claim_running()
    else:
        win_notify.claim_running()


def app_running() -> bool:
    if sys.platform == "darwin":
        return mac_notify.app_running()
    return win_notify.app_running()
