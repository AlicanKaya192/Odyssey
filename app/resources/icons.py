"""Arayüz ikonları.

İkonlar SVG yolu olarak gömülü tutuluyor: dosya bağımlılığı yok, internetten
bir şey çekilmiyor ve renk temaya göre çalışma anında değiştirilebiliyor.

Emoji kullanmıyoruz; emoji her Windows sürümünde farklı çiziliyor ve boyutu
kontrol edilemiyor.

Yol verileri Lucide ikon setinden (ISC lisansı, ticari kullanıma açık).
"""

from __future__ import annotations

from PySide6.QtCore import QByteArray, QSize, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

# Her ikon 24x24 tuval üzerine çizilmiş yollardan oluşuyor.
PATHS: dict[str, str] = {
    "home": (
        '<path d="M3 9.5 12 3l9 6.5V20a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>'
    ),
    "user": (
        '<circle cx="12" cy="8" r="4"/>'
        '<path d="M4 21c0-4 3.6-6 8-6s8 2 8 6"/>'
    ),
    "megaphone": (
        '<path d="M3 11v2a1 1 0 0 0 1 1h2l4 4V6L6 10H4a1 1 0 0 0-1 1z"/>'
        '<path d="M14 8a5 5 0 0 1 0 8"/>'
        '<path d="M17 5a9 9 0 0 1 0 14"/>'
    ),
    "settings": (
        '<circle cx="12" cy="12" r="3"/>'
        '<path d="M19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-1.8-.3'
        '1.6 1.6 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1A1.6 1.6 0 0 0 9 19.4a1.6 1.6 0 0 0-1.8.3l-.1.1'
        'a2 2 0 1 1-2.8-2.8l.1-.1a1.6 1.6 0 0 0 .3-1.8 1.6 1.6 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1'
        'A1.6 1.6 0 0 0 4.6 9a1.6 1.6 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.6 1.6 0 0 0 1.8.3'
        'H9a1.6 1.6 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.6 1.6 0 0 0 1 1.5 1.6 1.6 0 0 0 1.8-.3l.1-.1'
        'a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0-.3 1.8V9a1.6 1.6 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1'
        'a1.6 1.6 0 0 0-1.5 1z"/>'
    ),
    "arrow-left": '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "play": '<path d="M6 4l14 8-14 8z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "rotate": (
        '<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/>'
    ),
    "book": (
        '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>'
        '<path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>'
    ),
    "file-text": (
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<path d="M14 2v6h6"/><path d="M8 13h8"/><path d="M8 17h8"/>'
    ),
    "clipboard": (
        '<rect x="8" y="2" width="8" height="4" rx="1"/>'
        '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>'
    ),
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    "lightbulb": (
        '<path d="M9 18h6"/><path d="M10 22h4"/>'
        '<path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/>'
    ),
    "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    "flame": (
        '<path d="M12 2c1 4-2 5-2 8a4 4 0 0 0 8 0c0-1-.5-2-1-3 2 2 3 4 3 6a8 8 0 0 1-16 0'
        'c0-4 3-6 5-8 1-1 3-2 3-3z"/>'
    ),
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
}


def svg_markup(name: str, color: str, stroke: float = 2.0, filled: bool = False) -> str:
    """İkonu tam bir SVG belgesine sarar."""
    path = PATHS.get(name, PATHS["chevron-right"])
    fill = color if filled else "none"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
        f'fill="{fill}" stroke="{color}" stroke-width="{stroke}" '
        f'stroke-linecap="round" stroke-linejoin="round">{path}</svg>'
    )


def icon(name: str, color: str = "#666F7D", size: int = 22, filled: bool = False) -> QIcon:
    """İkonu istenen renk ve boyutta bir QIcon olarak üretir."""
    renderer = QSvgRenderer(QByteArray(svg_markup(name, color, filled=filled).encode("utf-8")))

    # Yüksek DPI ekranlarda bulanık görünmemesi için iki katı çözünürlükte
    # çizip ölçekliyoruz.
    pixmap = QPixmap(QSize(size * 2, size * 2))
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter)
    painter.end()

    pixmap.setDevicePixelRatio(2.0)
    return QIcon(pixmap)


def pixmap(name: str, color: str = "#666F7D", size: int = 22, filled: bool = False) -> QPixmap:
    """İkonu doğrudan QPixmap olarak verir (QLabel içinde kullanmak için)."""
    return icon(name, color, size, filled).pixmap(QSize(size, size))
