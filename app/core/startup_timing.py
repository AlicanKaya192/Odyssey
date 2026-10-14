"""Açılış sürelerini günlüğe tek satırla yazmak için.

Açılışın yavaşlığı en çok bilgisayar yeni açıldığında (dosyalar henüz
Windows'un belleğinde değilken) görünüyor ve geliştirme sırasında art arda
yapılan ölçümler bunu yakalamıyor (14 Ekim). Her açılışta süreler
`odyssey.log`'a yazılıyor; kişisel veri değil, yalnızca saniyeler.

Süreler sürecin başladığı andan ölçülüyor: Python'un kendisini ve
modülleri yüklemesi de dahil.
"""

from __future__ import annotations

import time

_100NS_PER_SECOND = 10_000_000


def process_age() -> float:
    """Bu sürecin başlamasından bu yana geçen saniye; bilinmiyorsa 0."""
    try:
        import ctypes
        from ctypes import wintypes

        # Kendi kopyası: ortak `windll.kernel32`'nin argüman tiplerini değiştirmesin.
        kernel32 = ctypes.WinDLL("kernel32")
        filetime = wintypes.FILETIME
        kernel32.GetCurrentProcess.argtypes = []
        kernel32.GetCurrentProcess.restype = wintypes.HANDLE
        kernel32.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(filetime)] * 4
        kernel32.GetProcessTimes.restype = wintypes.BOOL
        kernel32.GetSystemTimeAsFileTime.argtypes = [ctypes.POINTER(filetime)]
        kernel32.GetSystemTimeAsFileTime.restype = None

        created, exited, kernel, user, now = (filetime() for _ in range(5))
        if not kernel32.GetProcessTimes(kernel32.GetCurrentProcess(), ctypes.byref(created),
                                        ctypes.byref(exited), ctypes.byref(kernel), ctypes.byref(user)):
            return 0.0
        kernel32.GetSystemTimeAsFileTime(ctypes.byref(now))
    except (AttributeError, OSError):  # Windows dışı
        return 0.0

    def ticks(value) -> int:
        return (value.dwHighDateTime << 32) | value.dwLowDateTime

    return max(0.0, (ticks(now) - ticks(created)) / _100NS_PER_SECOND)


class StartupTimes:
    """Açılışın adımlarını sürecin başlangıcına göre saniye olarak toplar."""

    def __init__(self) -> None:
        self._origin = time.monotonic() - process_age()
        self._marks: dict[str, float] = {}

    def mark(self, name: str, at: float | None = None) -> None:
        """Adımın zamanı; `at` verilmezse şimdi (`time.monotonic` değeri)."""
        self._marks[name] = (time.monotonic() if at is None else at) - self._origin

    def summary(self) -> str:
        sirali = sorted(self._marks.items(), key=lambda item: item[1])
        return ", ".join(f"{name} {seconds:.2f}" for name, seconds in sirali)
