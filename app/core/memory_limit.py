"""Alıştırma sürecine bellek sınırı: Windows Job Object.

Kullanıcının kodu ayrı bir süreçte, zaman aşımıyla çalışıyor ama bellek
için bir sınır yoktu. Ölçüldü (M12, 15 Eylül 2026): büyük parçalarla
büyüyen bir kod saniyede ~2,2 GB, sıradan bir sonsuz liste ~400 MB
yiyor. On saniyelik zaman aşımı dolmadan boş belleğin tamamı bitip makine
sayfa dosyasına düşebiliyordu.

Süreç **askıda** başlatılıyor, bir işe (job) atanıyor, sonra
uyandırılıyor. Askıda başlatmak şart: alıştırma ortamındaki `python.exe`
asıl yorumlayıcıyı alt süreç olarak açan bir başlatıcı (ölçüldü: işte üç
süreç). Atama uyandırmadan sonra yapılsaydı alt süreç işe girmeden
kaçabilirdi; işe girdikten sonra açılan her alt süreç kendiliğinden işte.

İşin toplam belleği sınırı aşınca Python `MemoryError` veriyor (numpy da
"Unable to allocate") ve denetleyici sonucu yine yazıyor — ölçüldü. İş
kapatılınca içindeki her süreç ölüyor (`KILL_ON_JOB_CLOSE`), kullanıcının
açtığı alt süreçler arkada kalmıyor.

Her Windows çağrısının `argtypes` ve `restype`'ı bildiriliyor:
bildirilmezse ctypes 64 bitlik tanıtıcıyı 32 bite kırpıyor
(`discord_presence.py` ile aynı kural).
"""

from __future__ import annotations

import ctypes
import subprocess
import sys

# İşteki bütün süreçlerin toplam bellek sınırı. Ölçüm (M12): iş parçacığı
# ve işçi sayısı sabitlendikten sonra (runner.py) 257 alıştırma çözümünün
# en ağırı 226 MB; notların öğrettiği `n_jobs=-1` ile GridSearchCV 928 MB.
# Sınır bunların üç katından fazla pay bırakıyor, kaçak bir kod ise ona
# iki saniyede varıyor.
MEMORY_LIMIT_MB = 3072

# Tepe bellek sınırın bu oranına ulaştıysa çalıştırma sınıra çarpmış
# sayılıyor. Ölçümde işin tepesi sınırı birkaç on MB aşıyordu (2 GB
# sınırda 2068-2163 MB); gerçek alıştırmalar ise sınırın yarısının
# altında kalıyor.
LIMIT_HIT_RATIO = 0.95

CREATE_SUSPENDED = 0x00000004

_JOB_OBJECT_LIMIT_JOB_MEMORY = 0x00000200
_JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
_JOB_OBJECT_EXTENDED_LIMIT_INFORMATION = 9
_MB = 1024 * 1024


if sys.platform == "win32":
    from ctypes import wintypes

    _SIZE_T = ctypes.c_size_t

    class _BasicLimit(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_int64),
            ("PerJobUserTimeLimit", ctypes.c_int64),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", _SIZE_T),
            ("MaximumWorkingSetSize", _SIZE_T),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", _SIZE_T),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        ]

    class _IoCounters(ctypes.Structure):
        _fields_ = [
            (name, ctypes.c_ulonglong)
            for name in (
                "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
                "ReadTransferCount", "WriteTransferCount", "OtherTransferCount",
            )
        ]

    class _ExtendedLimit(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", _BasicLimit),
            ("IoInfo", _IoCounters),
            ("ProcessMemoryLimit", _SIZE_T),
            ("JobMemoryLimit", _SIZE_T),
            ("PeakProcessMemoryUsed", _SIZE_T),
            ("PeakJobMemoryUsed", _SIZE_T),
        ]

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _ntdll = ctypes.WinDLL("ntdll")

    _kernel32.CreateJobObjectW.argtypes = [wintypes.LPVOID, wintypes.LPCWSTR]
    _kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    _kernel32.SetInformationJobObject.argtypes = [
        wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD,
    ]
    _kernel32.SetInformationJobObject.restype = wintypes.BOOL
    _kernel32.QueryInformationJobObject.argtypes = [
        wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    ]
    _kernel32.QueryInformationJobObject.restype = wintypes.BOOL
    _kernel32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    _kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    _kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    _kernel32.CloseHandle.restype = wintypes.BOOL
    # Askıdaki sürecin bütün iş parçacıklarını uyandırıyor; subprocess
    # bir iş parçacığı tanıtıcısı vermediği için ResumeThread yerine bu.
    _ntdll.NtResumeProcess.argtypes = [wintypes.HANDLE]
    _ntdll.NtResumeProcess.restype = ctypes.c_long


class MemoryJob:
    """Bir çalıştırmanın süreçlerini tek bir bellek sınırı altında tutar.

    Kullanım: `create()` ile kur, süreci `CREATE_SUSPENDED` ile başlat,
    `attach()` ile işe ata ve uyandır, bittikten sonra `peak_mb()` /
    `limit_hit()` ile oku, `close()` ile kapat. Windows dışında `create()`
    `None` döndürüyor ve çalıştırma eskisi gibi sınırsız sürüyor.
    """

    def __init__(self, handle: int, limit_mb: int) -> None:
        self._handle = handle
        self.limit_mb = limit_mb

    @classmethod
    def create(cls, limit_mb: int = MEMORY_LIMIT_MB) -> MemoryJob | None:
        if sys.platform != "win32":
            return None
        handle = _kernel32.CreateJobObjectW(None, None)
        if not handle:
            return None
        info = _ExtendedLimit()
        info.BasicLimitInformation.LimitFlags = (
            _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE | _JOB_OBJECT_LIMIT_JOB_MEMORY
        )
        info.JobMemoryLimit = limit_mb * _MB
        if not _kernel32.SetInformationJobObject(
            handle, _JOB_OBJECT_EXTENDED_LIMIT_INFORMATION,
            ctypes.byref(info), ctypes.sizeof(info),
        ):
            _kernel32.CloseHandle(handle)
            return None
        return cls(handle, limit_mb)

    def attach(self, process: subprocess.Popen) -> bool:
        """Askıda başlatılmış süreci işe atar ve **her durumda** uyandırır.

        Atama başarısız olursa süreç yine uyandırılıyor: sınırsız ama
        çalışan bir kod, hiç uyanmayıp zaman aşımına düşen bir koddan iyi.
        """
        process_handle = int(process._handle)  # noqa: SLF001 — Popen'in Windows tanıtıcısı
        assigned = bool(_kernel32.AssignProcessToJobObject(self._handle, process_handle))
        _ntdll.NtResumeProcess(process_handle)
        return assigned

    def peak_mb(self) -> int:
        """İşteki süreçlerin toplamda ulaştığı en yüksek bellek (MB)."""
        if not self._handle:
            return 0
        info = _ExtendedLimit()
        if not _kernel32.QueryInformationJobObject(
            self._handle, _JOB_OBJECT_EXTENDED_LIMIT_INFORMATION,
            ctypes.byref(info), ctypes.sizeof(info), None,
        ):
            return 0
        return int(info.PeakJobMemoryUsed // _MB)

    def limit_hit(self) -> bool:
        return self.peak_mb() >= self.limit_mb * LIMIT_HIT_RATIO

    def close(self) -> None:
        """İşi kapatır; içinde kalan her süreç ölüyor."""
        if self._handle:
            _kernel32.CloseHandle(self._handle)
            self._handle = 0
