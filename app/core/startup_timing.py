"""Açılış sürelerini günlüğe tek satırla yazmak için.

Açılışın yavaşlığı en çok bilgisayar yeni açıldığında (dosyalar henüz
Windows'un belleğinde değilken) görünüyor ve geliştirme sırasında art arda
yapılan ölçümler bunu yakalamıyor (14 Ekim). Her açılışta süreler
`odyssey.log`'a yazılıyor; kişisel veri değil, yalnızca saniyeler.

Süreler sürecin başladığı andan ölçülüyor: Python'un kendisini ve
modülleri yüklemesi de dahil.

Yalnızca süre, yavaşlığın sebebini söylemiyor (20 Ekim: iki yavaş açılış
bilgisayar başka işle meşgulken oldu). Yanına açılışın koşulları da
yazılıyor: bilgisayarın işlemci yükü, bu sürecin aldığı işlemci süresi ve
boş bellek. Yük yüksekse bilgisayar meşguldü; yük düşük ama süreç az
işlemci aldıysa beklenen şey disk.
"""

from __future__ import annotations

import time

_100NS_PER_SECOND = 10_000_000
_BYTES_PER_GB = 1024 ** 3


def _kernel32():
    """Kendi kopyası: ortak `windll.kernel32`'nin argüman tiplerini değiştirmesin."""
    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32")
    filetime_p = ctypes.POINTER(wintypes.FILETIME)
    kernel32.GetCurrentProcess.argtypes = []
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    kernel32.GetProcessTimes.argtypes = [wintypes.HANDLE] + [filetime_p] * 4
    kernel32.GetProcessTimes.restype = wintypes.BOOL
    kernel32.GetSystemTimeAsFileTime.argtypes = [filetime_p]
    kernel32.GetSystemTimeAsFileTime.restype = None
    kernel32.GetSystemTimes.argtypes = [filetime_p] * 3
    kernel32.GetSystemTimes.restype = wintypes.BOOL
    return kernel32


def _ticks(value) -> int:
    return (value.dwHighDateTime << 32) | value.dwLowDateTime


def _process_times() -> tuple[float, float] | None:
    """(sürecin yaşı, harcadığı işlemci süresi) saniye; Windows dışında None."""
    try:
        import ctypes
        from ctypes import wintypes

        kernel32 = _kernel32()
        created, exited, kernel, user, now = (wintypes.FILETIME() for _ in range(5))
        if not kernel32.GetProcessTimes(kernel32.GetCurrentProcess(), ctypes.byref(created),
                                        ctypes.byref(exited), ctypes.byref(kernel), ctypes.byref(user)):
            return None
        kernel32.GetSystemTimeAsFileTime(ctypes.byref(now))
    except (AttributeError, OSError):  # Windows dışı
        return None
    age = max(0.0, (_ticks(now) - _ticks(created)) / _100NS_PER_SECOND)
    return age, (_ticks(kernel) + _ticks(user)) / _100NS_PER_SECOND


def _system_times() -> tuple[int, int] | None:
    """Bütün çekirdeklerin toplam (boşta, toplam) süresi; Windows dışında None."""
    try:
        import ctypes
        from ctypes import wintypes

        idle, kernel, user = (wintypes.FILETIME() for _ in range(3))
        if not _kernel32().GetSystemTimes(ctypes.byref(idle), ctypes.byref(kernel), ctypes.byref(user)):
            return None
    except (AttributeError, OSError):
        return None
    # Çekirdek süresi boşta geçeni de içeriyor.
    return _ticks(idle), _ticks(kernel) + _ticks(user)


def _free_memory_gb() -> float | None:
    try:
        import ctypes
        from ctypes import wintypes

        class MemoryStatus(ctypes.Structure):
            _fields_ = [("dwLength", wintypes.DWORD), ("dwMemoryLoad", wintypes.DWORD),
                        ("ullTotalPhys", ctypes.c_uint64), ("ullAvailPhys", ctypes.c_uint64),
                        ("ullTotalPageFile", ctypes.c_uint64), ("ullAvailPageFile", ctypes.c_uint64),
                        ("ullTotalVirtual", ctypes.c_uint64), ("ullAvailVirtual", ctypes.c_uint64),
                        ("ullAvailExtendedVirtual", ctypes.c_uint64)]

        kernel32 = ctypes.WinDLL("kernel32")
        kernel32.GlobalMemoryStatusEx.argtypes = [ctypes.POINTER(MemoryStatus)]
        kernel32.GlobalMemoryStatusEx.restype = wintypes.BOOL
        status = MemoryStatus()
        status.dwLength = ctypes.sizeof(MemoryStatus)
        if not kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return None
    except (AttributeError, OSError):
        return None
    return status.ullAvailPhys / _BYTES_PER_GB


def process_age() -> float:
    """Bu sürecin başlamasından bu yana geçen saniye; bilinmiyorsa 0."""
    times = _process_times()
    return times[0] if times else 0.0


class StartupTimes:
    """Açılışın adımlarını sürecin başlangıcına göre saniye olarak toplar."""

    def __init__(self) -> None:
        self._origin = time.monotonic() - process_age()
        self._marks: dict[str, float] = {}
        self._system_start = _system_times()
        self._free_memory = _free_memory_gb()

    def mark(self, name: str, at: float | None = None) -> None:
        """Adımın zamanı; `at` verilmezse şimdi (`time.monotonic` değeri)."""
        self._marks[name] = (time.monotonic() if at is None else at) - self._origin

    def summary(self) -> str:
        sirali = sorted(self._marks.items(), key=lambda item: item[1])
        return ", ".join(f"{name} {seconds:.2f}" for name, seconds in sirali)

    def conditions(self) -> str:
        """Açılış boyunca bilgisayarın yükü, sürecin işlemcisi ve boş bellek.

        Yük, nesnenin kurulduğu andan şimdiye kadar bütün çekirdeklerin dolu
        geçen payı; boş bellek kurulduğu andaki. Ölçülemeyen değer yazılmıyor.
        """
        parts = []
        now = _system_times()
        if self._system_start and now and now[1] > self._system_start[1]:
            idle = now[0] - self._system_start[0]
            total = now[1] - self._system_start[1]
            parts.append(f"islemci_yuku %{round(100 * (1 - idle / total))}")
        process = _process_times()
        if process:
            parts.append(f"surec_islemci {process[1]:.2f} sn / {process[0]:.2f} sn")
        if self._free_memory is not None:
            parts.append(f"bos_bellek {self._free_memory:.1f} GB")
        return ", ".join(parts)
