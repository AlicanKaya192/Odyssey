"""Tarayıcı bileşeninin (QtWebEngine) dosyalarını arka planda önceden okur.

Bilgisayar yeni açıldığında ya da dosyalar Windows'un belleğinden düştüğünde
bu bileşenin ~300 MB'lık dosyası diskten okunuyor. Açılışta okunduğunda ana
pencere 15 sn'yi geçiyordu (15 Ekim, `odyssey.log`). Belge alanlı ekranlar
artık pencere göründükten sonra kuruluyor; dosyalar önce bu iş parçacığında
okunuyor. Okuma sırasında Python kilidi (GIL) bırakıldığı için arayüz
donmuyor; ardından gelen kurulum dosyaları bellekte buluyor.

Okunan veri atılıyor, hiçbir yere yazılmıyor.
"""

from __future__ import annotations

import threading
import time
from pathlib import Path

# Bileşenin açılışta gerçekten yüklediği dosyalar (PySide6 klasörüne göre).
FILES = (
    "Qt6WebEngineCore.dll",
    "Qt6WebEngineWidgets.dll",
    "Qt6WebChannel.dll",
    "QtWebEngineCore.pyd",
    "QtWebEngineWidgets.pyd",
    "QtWebChannel.pyd",
    "QtWebEngineProcess.exe",
    "resources/icudtl.dat",
    "resources/v8_context_snapshot.bin",
    "resources/qtwebengine_resources.pak",
    "resources/qtwebengine_resources_100p.pak",
    "resources/qtwebengine_resources_200p.pak",
)

CHUNK_BYTES = 1 << 20


def engine_files() -> list[Path]:
    """Var olan dosyalar; paketlenmiş programda da aynı yerleşim."""
    import PySide6

    base = Path(PySide6.__file__).parent
    return [base / name for name in FILES if (base / name).is_file()]


def read_ahead(paths: list[Path]) -> int:
    """Dosyaları baştan sona okur; okunan bayt sayısını döndürür."""
    buffer = bytearray(CHUNK_BYTES)
    total = 0
    for path in paths:
        try:
            with open(path, "rb", buffering=0) as handle:
                while count := handle.readinto(buffer):
                    total += count
        except OSError:
            continue
    return total


class Prefetch:
    """Arka planda süren okuma; bitti mi ve ne zaman bitti."""

    def __init__(self) -> None:
        self.finished_at: float | None = None
        self._thread = threading.Thread(target=self._run, args=(engine_files(),),
                                        name="engine-prefetch", daemon=True)
        self._thread.start()

    def _run(self, paths: list[Path]) -> None:
        try:
            read_ahead(paths)
        finally:
            self.finished_at = time.monotonic()

    @property
    def done(self) -> bool:
        return not self._thread.is_alive()

    def wait(self, seconds: float) -> None:
        self._thread.join(seconds)
