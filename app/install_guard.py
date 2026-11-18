"""Yarım kalmış bir kurulumu Qt yüklenmeden önce yakalar (Windows paketi).

Tam kurulum önce eski `_internal` klasörünü siliyor, sonra yenisini yazıyor.
Arada kurulum kesilirse ya da kişi programı kurulum sürerken açarsa paket
eksik kalıyor ve PySide6 daha içe aktarılırken düşüyor. Kişi de anlamsız bir
Python hatası görüyordu (1.8.0, "shiboken6\\libshiboken does not exist").

Bu modül `main.py`'nin en başında, Qt'ye dokunmadan çalışıyor:

- kurulum programı hâlâ çalışıyorsa (`SETUP_MUTEX`) "güncelleniyor" deyip
  çıkıyor;
- gerekli dosyalardan biri eksikse ya da kurulumun bıraktığı işaret dosyası
  (`PENDING_FILE`, kurulum başında yazılıp sonunda siliniyor) duruyorsa
  kurulumun yeniden çalıştırılmasını öneriyor: indirilmiş tam kurulum varsa
  onu açıyor, yoksa sürüm sayfasını.

Ekran Windows'un kendi ileti kutusu (`MessageBoxW`); Qt'nin yüklenemediği
durumda başka arayüz yok. Bayraklı açılışlar (hatırlatma denetimi,
denetleyici, alt süreç, açılış animasyonu) soru sormadan çıkıyor.
"""

from __future__ import annotations

import ctypes
import os
import sys
from collections.abc import Callable
from pathlib import Path

# Kurulum programı (`installer/odyssey.iss`) ile aynı adlar.
PENDING_FILE = "install-pending.txt"
SETUP_MUTEX = "Odyssey.Setup"

# PySide6 açılırken ilk ihtiyaç duyulanlar (`_internal`'a göre). Paket
# değişirse `tools/build_exe.py` derlemeden sonra hepsinin var olduğunu
# denetliyor; yoksa bu denetim sağlam paketi de bozuk sayardı.
REQUIRED_FILES = (
    "shiboken6/Shiboken.pyd",
    "PySide6/QtCore.pyd",
    "PySide6/Qt6Core.dll",
    "PySide6/QtWidgets.pyd",
    "PySide6/QtWebEngineCore.pyd",
)

RELEASES_URL = "https://github.com/AlicanKaya192/Odyssey/releases/latest"

MB_OK = 0x0
MB_YESNO = 0x4
MB_ICONWARNING = 0x30
MB_ICONINFORMATION = 0x40
IDYES = 6
SYNCHRONIZE = 0x00100000

TEXTS = {
    "tr": {
        "title": "Odyssey",
        "installing": (
            "Odyssey güncelleniyor.\n\n"
            "Güncelleme bitince program kendiliğinden açılacak. Birkaç dakika "
            "sürebilir; bilgisayarı kapatmayın."
        ),
        "broken": (
            "Odyssey'nin bazı dosyaları eksik: son güncelleme yarıda "
            "kalmış olabilir.\n\nİlerlemeniz, notlarınız ve ayarlarınız "
            "yerinde; yalnızca program dosyaları yeniden kurulacak."
        ),
        "broken_setup": "\n\nKurulumu yeniden başlatayım mı?",
        "broken_page": (
            "\n\nİndirme sayfasını açayım mı? Oradaki "
            "\"Odyssey-…-setup.exe\" dosyasını indirip çalıştırmanız yeterli."
        ),
    },
    "en": {
        "title": "Odyssey",
        "installing": (
            "Odyssey is being updated.\n\n"
            "It will open by itself when the update finishes. This can take "
            "a few minutes; please don't turn off the computer."
        ),
        "broken": (
            "Some of Odyssey's files are missing: the last update may not "
            "have finished.\n\nYour progress, notes and settings are safe; "
            "only the program files will be reinstalled."
        ),
        "broken_setup": "\n\nRestart the installation now?",
        "broken_page": (
            "\n\nOpen the download page? Download and run the "
            "\"Odyssey-…-setup.exe\" file there."
        ),
    },
}

# Soru sormadan çıkılan açılışlar: kişi bir pencere beklemiyor.
QUIET_FLAGS = ("--reminder-check", "--run-harness", "--multiprocessing-fork", "--intro")


def missing_files(internal_dir: Path) -> list[str]:
    return [name for name in REQUIRED_FILES if not (internal_dir / name).is_file()]


def assess(app_dir: Path, internal_dir: Path, setup_running: bool) -> str:
    """"ok", "installing" (kurulum sürüyor) ya da "broken" (yarım kurulum)."""
    if setup_running:
        return "installing"
    if (app_dir / PENDING_FILE).exists() or missing_files(internal_dir):
        return "broken"
    return "ok"


def find_setup(updates_dir: Path) -> Path | None:
    """İndirilmiş en yeni tam kurulum (`Odyssey-<sürüm>-setup.exe`).

    Yama seçilmiyor: yarım kalan kurulum tam kurulumdu ve yama eksik
    dosyaları tamamlamaz. `MZ` imzası olmayan dosya sayılmıyor.
    """
    try:
        adaylar = [p for p in updates_dir.glob("Odyssey-*-setup.exe") if p.is_file()]
    except OSError:
        return None
    for aday in sorted(adaylar, key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            with aday.open("rb") as dosya:
                if dosya.read(2) == b"MZ":
                    return aday
        except OSError:
            continue
    return None


def message(lang: str, kind: str, has_setup: bool) -> tuple[str, str]:
    metinler = TEXTS.get(lang, TEXTS["en"])
    metin = metinler[kind]
    if kind == "broken":
        metin += metinler["broken_setup"] if has_setup else metinler["broken_page"]
    return metinler["title"], metin


def windows_language() -> str:
    """Windows'un ekran dili Türkçeyse `tr`, değilse `en` (Qt'siz)."""
    try:
        kimlik = ctypes.windll.kernel32.GetUserDefaultUILanguage()
    except (AttributeError, OSError):
        return "en"
    return "tr" if kimlik & 0x3FF == 0x1F else "en"


def _setup_running() -> bool:
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.OpenMutexW.argtypes = (ctypes.c_uint32, ctypes.c_int, ctypes.c_wchar_p)
    kernel32.OpenMutexW.restype = ctypes.c_void_p
    kernel32.CloseHandle.argtypes = (ctypes.c_void_p,)
    kernel32.CloseHandle.restype = ctypes.c_int
    tutamac = kernel32.OpenMutexW(SYNCHRONIZE, False, SETUP_MUTEX)
    if not tutamac:
        return False
    kernel32.CloseHandle(tutamac)
    return True


def _ask(title: str, text: str, question: bool) -> bool:
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    user32.MessageBoxW.argtypes = (ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint)
    user32.MessageBoxW.restype = ctypes.c_int
    tur = (MB_YESNO | MB_ICONWARNING) if question else (MB_OK | MB_ICONINFORMATION)
    return user32.MessageBoxW(None, text, title, tur) == IDYES


def _launch(setup: Path) -> None:
    import subprocess

    # Pencereli kurulum: kişi ilerlemeyi görsün. Klasör sayfası çıkmıyor
    # (`DisableDirPage=auto`), aynı yere kuruluyor.
    subprocess.Popen([str(setup)], cwd=str(setup.parent), close_fds=True)


def _open_url(url: str) -> None:
    os.startfile(url)  # noqa: S606 — sabit, bilinen adres


def _updates_dir() -> Path:
    from app.paths import updates_dir

    return updates_dir()


def check(
    argv: list[str] | None = None,
    *,
    app_dir: Path | None = None,
    internal_dir: Path | None = None,
    updates: Callable[[], Path] = _updates_dir,
    setup_running: Callable[[], bool] = _setup_running,
    lang: str | None = None,
    ask: Callable[[str, str, bool], bool] = _ask,
    launch: Callable[[Path], None] = _launch,
    open_url: Callable[[str], None] = _open_url,
) -> None:
    """Paket sağlamsa hiçbir şey yapmaz; değilse kişiye söyleyip çıkar."""
    if internal_dir is None:
        if sys.platform != "win32" or not getattr(sys, "frozen", False):
            return
        app_dir = Path(sys.executable).resolve().parent
        internal_dir = Path(getattr(sys, "_MEIPASS", app_dir / "_internal"))
    argv = sys.argv if argv is None else argv

    durum = assess(app_dir, internal_dir, setup_running())
    if durum == "ok":
        return
    if any(arg in QUIET_FLAGS for arg in argv[1:]):
        raise SystemExit(1)

    dil = lang or windows_language()
    if durum == "installing":
        ask(*message(dil, "installing", has_setup=False), False)
        raise SystemExit(0)

    kurulum = find_setup(updates())
    if ask(*message(dil, "broken", has_setup=kurulum is not None), True):
        if kurulum is not None:
            launch(kurulum)
        else:
            open_url(RELEASES_URL)
    raise SystemExit(1)
