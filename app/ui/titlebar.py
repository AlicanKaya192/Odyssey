"""Windows başlık çubuğunu uygulamanın paletine boyar.

Pencerenin üstündeki şerit Windows'un kendi çizdiği alan; Qt oraya
karışamıyor. Koyu temada uygulama koyu, çubuk açık kalıyordu ve pencere
ikiye bölünmüş gibi duruyordu.

**Çubuk kaldırılıp elle çizilmedi.** Kaldırmak demek sürüklemeyi, kenardan
boyutlandırmayı, çift tıklayıp büyütmeyi, Snap düzenlerini (Win+Z), sistem
menüsünü ve çift ekran davranışını elle yazmak demek. Bunların hepsi ince
davranışlar ve elle yazılınca yerlisinden kötü çalışıyor. Burada yalnızca
**renk** değiştiriliyor; davranışın tamamı Windows'ta kalıyor.

Gereken: Windows 11 (derleme 22000+). Daha eskisinde çağrı başarısız dönüyor
ve çubuk olduğu gibi kalıyor — uygulama yine açılıyor.
"""

from __future__ import annotations

import sys

from ..resources.theme.tokens import PALETTES

# DwmSetWindowAttribute'un kullandığımız alanları.
DWMWA_USE_IMMERSIVE_DARK_MODE = 20
DWMWA_BORDER_COLOR = 34
DWMWA_CAPTION_COLOR = 35
DWMWA_TEXT_COLOR = 36


def _colorref(hex_color: str) -> int:
    """`#RRGGBB` metnini Windows'un beklediği `0x00BBGGRR` sayısına çevirir.

    Windows renk baytlarını ters sırada istiyor; doğrudan geçirilirse
    kırmızıyla mavi yer değiştiriyor.
    """
    value = hex_color.lstrip("#")
    r, g, b = int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)
    return (b << 16) | (g << 8) | r


def apply(window, mode: str) -> bool:
    """Başlık çubuğunu seçili temaya boyar.

    Başarılıysa True döner. Windows dışında veya API yoksa sessizce False
    dönüyor: bu bir görsel iyileştirme, olmaması uygulamayı bozmuyor.
    """
    if sys.platform != "win32":
        return False

    try:
        import ctypes
        from ctypes import wintypes
    except ImportError:
        return False

    handle = int(window.winId())
    palette = PALETTES.get(mode, PALETTES["light"])

    try:
        dwm = ctypes.windll.dwmapi
    except (AttributeError, OSError):
        return False

    def gonder(attribute: int, value: int) -> bool:
        sayı = ctypes.c_int(value)
        sonuc = dwm.DwmSetWindowAttribute(
            wintypes.HWND(handle),
            wintypes.DWORD(attribute),
            ctypes.byref(sayı),
            ctypes.sizeof(sayı),
        )
        return sonuc == 0

    # Karanlık kip önce: düğmelerin (küçült, büyüt, kapat) rengini bu
    # belirliyor. Zemin koyuyken açık kip bırakılırsa düğmeler görünmüyor.
    tamam = gonder(DWMWA_USE_IMMERSIVE_DARK_MODE, 1 if mode == "dark" else 0)

    tamam &= gonder(DWMWA_CAPTION_COLOR, _colorref(palette["surface"]))
    tamam &= gonder(DWMWA_TEXT_COLOR, _colorref(palette["text"]))
    tamam &= gonder(DWMWA_BORDER_COLOR, _colorref(palette["border"]))

    return bool(tamam)
