"""macOS'ta matplotlib'in yazı tipi önbelleğini önceden kurmak.

matplotlib ilk içe aktarıldığında sistemdeki yazı tiplerini tarayıp
önbelleğini (`~/.matplotlib/fontlist-*.json`) yazıyor. Yeni bir Mac'te bu
~55–60 sn sürdü (GitHub Actions macOS ölçümü, 13 Kasım) ve kişinin ilk
grafik alıştırması tam bu yüzden zaman aşımına düştü. Önbellek kalıcı: bir
kez kurulunca sonraki alıştırmalar beklemiyor.

Program açıldıktan sonra arka planda, alıştırmaların çalıştığı denetleyicide
bir kez kuruluyor (aynı matplotlib, aynı önbellek klasörü). Windows'ta
tarama kısa sürdüğü için yapılmıyor.
"""

from __future__ import annotations

import sys
import tempfile
import time
from pathlib import Path

from . import log

# Önbelleği kurmak uzun sürebiliyor; alıştırma süresine bağlı değil.
WARM_TIMEOUT_SEC = 300

WARM_CODE = (
    "import matplotlib\n"
    "matplotlib.use('Agg')\n"
    "import matplotlib.font_manager\n"
)


def _cache_dir() -> Path:
    # macOS'ta matplotlib'in varsayılan yapılandırma ve önbellek klasörü.
    return Path.home() / ".matplotlib"


def needed() -> bool:
    """Yalnızca macOS'ta ve önbellek henüz yoksa."""
    if sys.platform != "darwin":
        return False
    return not any(_cache_dir().glob("fontlist-*.json"))


def warm_if_needed() -> float | None:
    """Gerekiyorsa önbelleği kurar; geçen süreyi (sn) ya da None döndürür.

    Hata dışarı çıkmıyor: kurulamazsa ilk grafik alıştırması eskisi gibi
    önbelleği kendisi kurar.
    """
    if not needed():
        return None
    from . import runner

    started = time.monotonic()
    try:
        with tempfile.TemporaryDirectory() as folder:
            result = runner.run_code(WARM_CODE, [], WARM_TIMEOUT_SEC, Path(folder))
    except Exception:
        log.get(__name__).exception("matplotlib önbelleği kurulamadı")
        return None
    elapsed = time.monotonic() - started
    log.get(__name__).info("matplotlib önbelleği: %s, %.1f sn", result.status, elapsed)
    return elapsed
