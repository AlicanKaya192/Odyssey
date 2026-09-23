"""Windows bildirimleri: uygulama kimliği, bildirimi gösterme, açık mı?

**Kimlik.** Paketlenmemiş (MSIX olmayan) bir uygulamanın bildirimi ancak
kimliği kayıtlıysa görünüyor. Kayıt kullanıcının kendi kayıt defteri
dalına yazılıyor (`HKCU\\Software\\Classes\\AppUserModelId\\...`), yönetici
izni istemiyor. Aynı dala `odyssey://` bağlantısı da yazılıyor: bildirime
tıklanınca Windows onu açıyor, o da Odyssey'i başlatıyor.

**Gösterme.** WinRT bildirim API'si Python'dan doğrudan çağrılamıyor;
ek bir kütüphane yerine Windows'la gelen PowerShell kullanılıyor
(`-EncodedCommand`, pencere açılmadan). Ölçüldü: ~0,3 sn.

**Açık mı?** Uygulama açıkken adlandırılmış bir kilit (mutex) tutuyor.
Hatırlatma denetleyicisi kilide bakıp program açıksa bildirim
göndermiyor: kişi zaten uygulamanın başında. Bildirime tıklayıp ikinci bir
pencere açılmasının önüne de aynı kilit geçiyor.
"""

from __future__ import annotations

import base64
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

# `main.py` görev çubuğu için de aynı kimliği kullanıyor.
APP_ID = "AlicanKaya.Odyssey"
PROTOCOL = "odyssey"
MUTEX_NAME = "Local\\Odyssey.Running"

_AUMID_KEY = rf"Software\Classes\AppUserModelId\{APP_ID}"
_PROTOCOL_KEY = rf"Software\Classes\{PROTOCOL}"

_mutex_handle = None


def supported() -> bool:
    return sys.platform == "win32"


# --- kimlik ve bağlantı --------------------------------------------------


def register(icon_path: Path | None, launch_command: str) -> None:
    """Uygulama kimliğini ve `odyssey://` bağlantısını kaydeder."""
    if not supported():
        return
    import winreg

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, _AUMID_KEY) as key:
        winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "Odyssey")
        if icon_path is not None:
            winreg.SetValueEx(key, "IconUri", 0, winreg.REG_SZ, str(icon_path))

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, _PROTOCOL_KEY) as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "URL:Odyssey")
        winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
    with winreg.CreateKey(
        winreg.HKEY_CURRENT_USER, _PROTOCOL_KEY + r"\shell\open\command"
    ) as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'{launch_command} "%1"')


def unregister() -> None:
    """Kayıtları siler (hatırlatmalar kapatılınca)."""
    if not supported():
        return
    import winreg

    for path in (
        _PROTOCOL_KEY + r"\shell\open\command",
        _PROTOCOL_KEY + r"\shell\open",
        _PROTOCOL_KEY + r"\shell",
        _PROTOCOL_KEY,
        _AUMID_KEY,
    ):
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, path)
        except OSError:
            pass


# --- bildirim ------------------------------------------------------------


def toast_xml(title: str, body: str, icon_path: Path | None) -> str:
    logo = ""
    if icon_path is not None:
        logo = (
            '<image placement="appLogoOverride" '
            f"src={quoteattr('file:///' + icon_path.as_posix())}/>"
        )
    return (
        f'<toast activationType="protocol" launch="{PROTOCOL}://open">'
        '<visual><binding template="ToastGeneric">'
        f"<text>{escape(title)}</text><text>{escape(body)}</text>{logo}"
        "</binding></visual></toast>"
    )


def show_toast(title: str, body: str, icon_path: Path | None = None) -> bool:
    """Bildirimi gösterir; başarılıysa True."""
    if not supported():
        return False
    xml = toast_xml(title, body, icon_path).replace("'", "''")
    script = (
        "[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, "
        "ContentType = WindowsRuntime] > $null\n"
        "[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, "
        "ContentType = WindowsRuntime] > $null\n"
        "$xml = New-Object Windows.Data.Xml.Dom.XmlDocument\n"
        f"$xml.LoadXml('{xml}')\n"
        "$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)\n"
        "[Windows.UI.Notifications.ToastNotificationManager]::"
        f"CreateToastNotifier('{APP_ID}').Show($toast)\n"
    )
    try:
        result = subprocess.run(
            [
                "powershell.exe", "-NoProfile", "-NonInteractive",
                "-ExecutionPolicy", "Bypass",
                "-EncodedCommand", base64.b64encode(script.encode("utf-16-le")).decode(),
            ],
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0


# --- program açık mı? ----------------------------------------------------


def _kernel32():
    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    # Argüman tipleri bildirilmeden 64 bitlik tanıtıcı 32 bite kırpılıyor.
    kernel32.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
    kernel32.CreateMutexW.restype = wintypes.HANDLE
    kernel32.OpenMutexW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
    kernel32.OpenMutexW.restype = wintypes.HANDLE
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    return kernel32


def claim_running() -> None:
    """Uygulama açıkken tutulan kilidi alır (süreç kapanınca kendiliğinden bırakılır)."""
    global _mutex_handle
    if not supported() or _mutex_handle:
        return
    try:
        _mutex_handle = _kernel32().CreateMutexW(None, False, MUTEX_NAME)
    except (OSError, AttributeError):
        _mutex_handle = None


def app_running() -> bool:
    """Odyssey'in başka bir penceresi açık mı?"""
    if not supported():
        return False
    try:
        kernel32 = _kernel32()
        synchronize = 0x00100000
        handle = kernel32.OpenMutexW(synchronize, False, MUTEX_NAME)
    except (OSError, AttributeError):
        return False
    if handle:
        kernel32.CloseHandle(handle)
        return True
    return False
