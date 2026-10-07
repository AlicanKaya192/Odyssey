"""Patika logoları.

Her patikanın kendi logosu var: degradeli, köşeleri yuvarlatılmış bir
kutucuğun içinde kendi işareti. Kutucuğun zemini patikanın renginden
(açık → koyu) üretiliyor, üstte hafif bir parlama ve ince bir iç çerçeve
var. Python'un logosu kendi mavi-sarı renkleriyle çiziliyor.

Çizimler yalnızca QSvgRenderer'ın desteklediği öğelerle yazıldı (path,
rect, circle, ellipse, linearGradient, opacity); filtre ya da maske yok.
Kilitli patikanın logosu gri zeminde ve soluk.
"""

from __future__ import annotations

import hashlib

from functools import lru_cache

from PySide6.QtCore import QByteArray, QRectF, Qt
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

from .theme.tokens import mix

# İşaretler 24'lük ızgarada; kutucuğun ortasına 1.12 büyütülerek konuyor.
# `bg` verilmişse zemin o iki renk (Python'un koyu zemini gibi).
GLYPHS: dict[str, dict[str, object]] = {
    "python": {
        "bg": ("#2B3A55", "#141B2B"),
        "defs": (
            '<linearGradient id="pyB" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#5A9FD4"/><stop offset="1" stop-color="#306998"/></linearGradient>'
            '<linearGradient id="pyY" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#FFE873"/><stop offset="1" stop-color="#FFD43B"/></linearGradient>'
        ),
        "svg": (
            '<path fill="url(#pyB)" d="M11.9 2C6.9 2 7.2 4.2 7.2 4.2v2.2h4.9v.7H5.3S2 6.7 2 12s2.9 5.1 2.9 5.1h1.8v-2.5'
            's-.1-2.9 2.9-2.9h4.9s2.8 0 2.8-2.7V4.5S17.7 2 11.9 2zm-2.7 1.5a.9.9 0 1 1 0 1.8.9.9 0 0 1 0-1.8z"/>'
            '<path fill="url(#pyY)" d="M12.1 22c5 0 4.7-2.2 4.7-2.2v-2.2h-4.9v-.7h6.8S22 17.3 22 12s-2.9-5.1-2.9-5.1h-1.8v2.5'
            's.1 2.9-2.9 2.9H9.5s-2.8 0-2.8 2.7v4.5S6.3 22 12.1 22zm2.7-1.5a.9.9 0 1 1 0-1.8.9.9 0 0 1 0 1.8z"/>'
        ),
    },
    "data": {"svg": (
        '<rect x="4" y="13" width="3.4" height="7" rx="1.2" fill="#fff" opacity=".75"/>'
        '<rect x="10.3" y="9.5" width="3.4" height="10.5" rx="1.2" fill="#fff" opacity=".85"/>'
        '<rect x="16.6" y="6" width="3.4" height="14" rx="1.2" fill="#fff"/>'
        '<path d="M3.5 10.5 8.5 6l4 2.5 7.5-5.5" fill="none" stroke="#fff" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
    )},
    "ml": {"svg": (
        '<g stroke="#fff" stroke-opacity=".55" stroke-width="1.3" fill="none">'
        '<path d="M5 7 12 4.5M5 7l7 7.5M5 17l7-12.5M5 17l7-2.5M5 17l7 3M12 4.5 19 12M12 14.5 19 12M12 20 19 12M5 7l7 13"/></g>'
        '<g fill="#fff"><circle cx="5" cy="7" r="2.2"/><circle cx="5" cy="17" r="2.2"/><circle cx="12" cy="4.5" r="2.2"/>'
        '<circle cx="12" cy="14.5" r="2.2"/><circle cx="12" cy="20" r="1.8" opacity=".8"/><circle cx="19" cy="12" r="2.6"/></g>'
    )},
    "sql": {"svg": (
        '<path d="M4.5 6v12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3V6" fill="#fff" fill-opacity=".22" stroke="#fff" stroke-width="1.8"/>'
        '<path d="M4.5 12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3" fill="none" stroke="#fff" stroke-width="1.8"/>'
        '<ellipse cx="12" cy="6" rx="7.5" ry="3" fill="#fff"/>'
    )},
    "math": {"svg": (
        '<path d="M17 5H7.5l5 7-5 7H17" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" '
        'stroke-linejoin="round"/><circle cx="18.5" cy="12" r="1.6" fill="#fff" opacity=".7"/>'
    )},
    "math1": {"svg": (
        '<path d="M5 8h14M9 8c0 5-.5 8.5-2 11M15 8v8.5c0 1.5.8 2.5 2.5 2.5" fill="none" stroke="#fff" '
        'stroke-width="2.2" stroke-linecap="round"/>'
    )},
    "math2": {"svg": (
        '<path d="M15.5 4.5c-1.8-1.2-3.8 0-4 2.3L10.5 17c-.2 2.4-2.2 3.5-4 2.4" fill="none" stroke="#fff" '
        'stroke-width="2.2" stroke-linecap="round"/>'
        '<path d="M15 13.5l4 4M19 13.5l-4 4" stroke="#fff" stroke-width="1.6" stroke-linecap="round" opacity=".75"/>'
    )},
    "api": {"svg": (
        '<path d="M8 4.5c-2 0-2.6 1-2.6 2.6v2.2c0 1.3-.8 2.1-2 2.7 1.2.6 2 1.4 2 2.7v2.2c0 1.6.6 2.6 2.6 2.6'
        'M16 4.5c2 0 2.6 1 2.6 2.6v2.2c0 1.3.8 2.1 2 2.7-1.2.6-2 1.4-2 2.7v2.2c0 1.6-.6 2.6-2.6 2.6" '
        'fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>'
        '<circle cx="9.3" cy="12" r="1.3" fill="#fff"/><circle cx="12" cy="12" r="1.3" fill="#fff"/>'
        '<circle cx="14.7" cy="12" r="1.3" fill="#fff"/>'
    )},
    "docker": {"svg": (
        '<g fill="#fff"><rect x="4.6" y="9.4" width="2.6" height="2.4" rx=".4"/><rect x="7.7" y="9.4" width="2.6" height="2.4" rx=".4"/>'
        '<rect x="10.8" y="9.4" width="2.6" height="2.4" rx=".4"/><rect x="13.9" y="9.4" width="2.6" height="2.4" rx=".4"/>'
        '<rect x="7.7" y="6.5" width="2.6" height="2.4" rx=".4"/><rect x="10.8" y="6.5" width="2.6" height="2.4" rx=".4"/>'
        '<rect x="13.9" y="6.5" width="2.6" height="2.4" rx=".4" opacity=".8"/><rect x="10.8" y="3.6" width="2.6" height="2.4" rx=".4"/>'
        '<path d="M2.4 12.6h16.9c.7-1.5 2.1-2 2.9-1.7-.2 1-1 1.8-1.9 2.1-1.4 4.2-5 6.8-10 6.8-4.6 0-7.4-2.6-7.9-7.2z"/></g>'
        '<circle cx="7" cy="15.3" r=".8" fill="#1D63ED"/>'
    )},
    "git": {"svg": (
        '<path d="M7 5v10.4" stroke="#fff" stroke-width="2.1" stroke-linecap="round"/>'
        '<path d="M17 9.3c0 4.4-3.5 7-8 7.4" fill="none" stroke="#fff" stroke-width="2.1" stroke-linecap="round"/>'
        '<circle cx="17" cy="6.6" r="2.6" fill="#fff"/><circle cx="7" cy="17.8" r="2.6" fill="#fff"/>'
        '<circle cx="7" cy="4.4" r="1.7" fill="#fff" fill-opacity=".8"/>'
    )},
    "time": {"svg": (
        '<path d="M3 20h18" stroke="#fff" stroke-opacity=".5" stroke-width="1.5" stroke-linecap="round"/>'
        '<path d="M3 15.5 7 11l3.5 3 4-7 3 4L21 8" fill="none" stroke="#fff" stroke-width="2.1" '
        'stroke-linecap="round" stroke-linejoin="round"/><circle cx="14.5" cy="7" r="1.8" fill="#fff"/>'
    )},
    "nlp": {"svg": (
        '<path d="M4 5.5A1.5 1.5 0 0 1 5.5 4h13A1.5 1.5 0 0 1 20 5.5v9a1.5 1.5 0 0 1-1.5 1.5H10l-4.5 4v-4'
        'A1.5 1.5 0 0 1 4 14.5z" fill="#fff" fill-opacity=".22" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"/>'
        '<path d="M8 8.5h8M8 12h5" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>'
    )},
    "genai": {"svg": (
        '<path fill="#fff" d="M10.5 3c.7 4 2.5 5.8 6.5 6.5-4 .7-5.8 2.5-6.5 6.5-.7-4-2.5-5.8-6.5-6.5 4-.7 5.8-2.5 6.5-6.5z"/>'
        '<path fill="#fff" opacity=".8" d="M18 13.5c.3 1.9 1.2 2.8 3 3.1-1.8.3-2.7 1.2-3 3.1-.3-1.9-1.2-2.8-3-3.1 1.8-.3 2.7-1.2 3-3.1z"/>'
    )},
    "big": {"svg": (
        '<path d="M12 3 21 7.5 12 12 3 7.5z" fill="#fff"/>'
        '<path d="M4.6 11.2 3 12l9 4.5 9-4.5-1.6-.8L12 14.9z" fill="#fff" opacity=".8"/>'
        '<path d="M4.6 15.7 3 16.5 12 21l9-4.5-1.6-.8L12 19.4z" fill="#fff" opacity=".6"/>'
    )},
    "algo": {"svg": (
        '<g stroke="#fff" stroke-opacity=".6" stroke-width="1.6" fill="none">'
        '<path d="M12 5 6.5 12M12 5l5.5 7M6.5 12 3.8 19M6.5 12l2.7 7M17.5 12l-2.7 7"/></g>'
        '<g fill="#fff"><circle cx="12" cy="5" r="2.4"/><circle cx="6.5" cy="12" r="2.2"/><circle cx="17.5" cy="12" r="2.2"/>'
        '<circle cx="3.8" cy="19" r="1.9"/><circle cx="9.2" cy="19" r="1.9"/><circle cx="14.8" cy="19" r="1.9"/></g>'
    )},
    "lib": {"svg": (
        '<rect x="3.5" y="4" width="4.2" height="16" rx="1.2" fill="#fff"/>'
        '<rect x="9" y="6" width="4.2" height="14" rx="1.2" fill="#fff" opacity=".8"/>'
        '<path d="m14.6 7.4 4-1.1 3.7 13.4-4 1.1z" fill="#fff" opacity=".65"/>'
        '<path d="M3.5 8h4.2M9 10h4.2" stroke="#000" stroke-opacity=".18" stroke-width="1.2"/>'
    )},
    "sys": {"svg": (
        '<path d="M8 8.5c-2 0-3.5 1.6-3.5 3.5s1.5 3.5 3.5 3.5c3 0 5-7 8-7 2 0 3.5 1.6 3.5 3.5S18 15.5 16 15.5'
        'c-3 0-5-7-8-7z" fill="none" stroke="#fff" stroke-width="2.2" stroke-linejoin="round"/>'
        '<path d="m17.5 6.5 1.5 2-2.3.6" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" '
        'stroke-linejoin="round"/>'
    )},
}

# `tracks.json` ve `chapter.json` içindeki `icon` adından logo anahtarına.
ICON_TO_LOGO = {
    "python": "python", "chart": "data", "network": "ml", "database": "sql",
    "calculator": "math", "link": "api", "package": "docker", "clock": "time", "git-branch": "git",
    "message": "nlp", "sparkles": "genai", "cpu": "algo", "library": "lib",
    "server": "sys", "layers": "big",
}

# Matematik patikasının iki modülü kendi işaretini taşıyor.
CHAPTER_LOGO = {"04-temel-matematik": "math1", "05-ileri-matematik": "math2"}

LOCKED_BG = ("#4B5563", "#1F2937")


def logo_key(icon_name: str, owner_id: str = "") -> str:
    """Patika ya da modülün `icon` adından logo anahtarını verir."""
    return CHAPTER_LOGO.get(owner_id) or ICON_TO_LOGO.get(icon_name, "lib")


def logo_svg(key: str, color: str, locked: bool = False) -> str:
    """Logoyu tam bir SVG belgesi olarak üretir (48x48 tuval)."""
    glyph = GLYPHS.get(key, GLYPHS["lib"])
    if locked:
        bg = LOCKED_BG
    else:
        bg = glyph.get("bg") or (mix(color, "#FFFFFF", 0.28), mix(color, "#000000", 0.28))
    isaret = str(glyph["svg"])
    # Geçişin kimliği logoya özel: aynı HTML sayfasına gömülen SVG'ler tek
    # kimlik uzayını paylaşıyor ve hepsi `bg` deyince ilk logonun rengini
    # alıyordu (Rotalar'da bütün logolar Python'un koyu zemininde çıktı).
    gid = "lg" + hashlib.md5(f"{key}|{color}|{locked}".encode()).hexdigest()[:10]
    if locked:
        isaret = f'<g opacity=".55">{isaret}</g>'
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><defs>'
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{bg[0]}"/>'
        f'<stop offset="1" stop-color="{bg[1]}"/></linearGradient>{glyph.get("defs", "")}</defs>'
        f'<rect x="1" y="1" width="46" height="46" rx="14" fill="url(#{gid})"/>'
        '<path d="M15 1h18a14 14 0 0 1 14 14v1C38 12 10 12 1 16v-1A14 14 0 0 1 15 1z" fill="#fff" fill-opacity=".13"/>'
        '<rect x="1.5" y="1.5" width="45" height="45" rx="13.5" fill="none" stroke="#fff" stroke-opacity=".14"/>'
        f'<g transform="translate(24 24) scale(1.12) translate(-12 -12)">{isaret}</g></svg>'
    )


@lru_cache(maxsize=256)
def logo_pixmap(key: str, color: str, size: int, locked: bool = False, ratio: float = 2.0) -> QPixmap:
    """Logoyu `size` piksel (mantıksal) boyutunda keskin bir pixmap olarak verir."""
    renderer = QSvgRenderer(QByteArray(logo_svg(key, color, locked).encode("utf-8")))
    kenar = max(1, round(size * ratio))
    pix = QPixmap(kenar, kenar)
    pix.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    renderer.render(painter, QRectF(0, 0, kenar, kenar))
    painter.end()
    pix.setDevicePixelRatio(ratio)
    return pix
