"""Kutlama kartlarının sesi: bölüm bitince, rozet kazanılınca ve seviye atlayınca.

Sesler `app/resources/sounds/` altında (`tools/make_sounds.py` üretiyor).
Çalma Windows'un kendi `winsound` modülüyle, arka planda (`SND_ASYNC`):
ek kütüphane yok, arayüz beklemiyor. Başka bir sistemde ses çalınmıyor;
ayar da orada gösterilmiyor (Bildirimler sayfası zaten Windows'a özgü).

Aynı anda birden fazla kart geliyor (bölüm kartı ve onunla kazanılan
rozetler): `winsound` yeni sesi başlatınca öncekini kesiyor, üst üste
çalan sesler de gürültü oluyor. Bu yüzden bir kart grubu için **tek ses**
çalınıyor; grupta seviye atlama varsa onun sesi, yoksa rozet varsa rozet
sesi. Grubu toplamak çağıranın işi
(`MainWindow`), burada yalnızca kısa aralıkla gelen ikinci çağrı yutuluyor.
"""

from __future__ import annotations

import sys
import time

from ..paths import install_root

SETTING_KEY = "celebration_sound"
KINDS = ("section", "badge", "level", "timer")
# Bu süreden kısa aralıkla gelen ikinci ses çalınmıyor (en uzun ses ~1,5 sn).
MIN_GAP = 1.0


def supported() -> bool:
    return sys.platform == "win32"


def enabled(store) -> bool:
    """Ayar açık mı? Varsayılan **açık**."""
    return store.setting(SETTING_KEY, "1") != "0"


def set_enabled(store, value: bool) -> None:
    store.set_setting(SETTING_KEY, "1" if value else "0")


def sound_path(kind: str):
    return install_root() / "app" / "resources" / "sounds" / f"{kind}.wav"


class CelebrationSound:
    """Sesi çalan nesne; son çalma zamanını tutuyor."""

    def __init__(self, store) -> None:
        self._store = store
        self._last = 0.0

    def play(self, kind: str) -> bool:
        """Sesi çalar; çaldıysa True. Kapalıysa, desteklenmiyorsa, dosya
        yoksa ya da az önce bir ses çaldıysa sessizce hiçbir şey yapmaz."""
        if kind not in KINDS or not supported() or not enabled(self._store):
            return False
        simdi = time.monotonic()
        if simdi - self._last < MIN_GAP:
            return False
        path = sound_path(kind)
        if not path.exists():
            return False
        try:
            import winsound

            winsound.PlaySound(
                str(path),
                winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT,
            )
        except (RuntimeError, OSError):
            # Ses aygıtı yoksa ya da meşgulse kutlama sessiz geçer; kart
            # yine de çıkıyor.
            return False
        self._last = simdi
        return True
