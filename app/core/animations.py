"""Animasyonlar ayarı (Ayarlar › Görünüm › Animasyonlar).

Açıkken ekran geçişleri, kart hareketleri ve kutlamalar oynuyor; kapalıyken
her şey doğrudan son hâline geliyor. Hiçbir bilgi yalnızca hareketle
verilmediği için kapatmak bir şey eksiltmiyor.

**Varsayılan Windows'tan geliyor.** Kullanıcı Windows'ta "Animasyon
efektleri"ni kapatmışsa (Erişilebilirlik › Görsel efektler) ilk açılışta
burası da kapalı başlıyor. Ayarı bir kez değiştirince kendi seçimi geçerli.

Kural burada; çağıran yerler anahtarı kendisi okumuyor.
"""

from __future__ import annotations

import sys

SETTING_KEY = "animations"


def _windows_animations_on() -> bool:
    """Windows'un istemci alanı animasyonları açık mı? Bilinmiyorsa açık."""
    if sys.platform != "win32":
        return True
    try:
        import ctypes
        from ctypes import wintypes

        SPI_GETCLIENTAREAANIMATION = 0x1042
        spi = ctypes.windll.user32.SystemParametersInfoW
        spi.argtypes = [wintypes.UINT, wintypes.UINT, ctypes.c_void_p, wintypes.UINT]
        spi.restype = wintypes.BOOL
        deger = wintypes.BOOL(True)
        if not spi(SPI_GETCLIENTAREAANIMATION, 0, ctypes.byref(deger), 0):
            return True
        return bool(deger.value)
    except (OSError, AttributeError):
        return True


def enabled(store) -> bool:
    """Animasyonlar açık mı? Kayıt yoksa Windows'un tercihi."""
    kayit = store.setting(SETTING_KEY, "")
    if kayit in ("0", "1"):
        return kayit == "1"
    return _windows_animations_on()


def set_enabled(store, value: bool) -> None:
    store.set_setting(SETTING_KEY, "1" if value else "0")
