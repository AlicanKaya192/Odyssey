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
    # Megafon: gövde sola doğru açılan bir koni, altında tutamak. Önceki
    # çizim hoparlöre benziyordu; ses ikonuyla karışıyordu.
    "megaphone": (
        '<path d="m3 11 15-7v16L3 13z"/>'
        '<path d="M3 11H2.5A1.5 1.5 0 0 0 1 12.5v0A1.5 1.5 0 0 0 2.5 14H3z"/>'
        '<path d="M6 14v5a2 2 0 0 0 4 0v-3.6"/>'
        '<path d="M21 9v6"/>'
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
    "link": (
        '<path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/>'
        '<path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/>'
    ),
    "package": (
        '<path d="m12 2 9 5v10l-9 5-9-5V7z"/>'
        '<path d="m3 7 9 5 9-5"/><path d="M12 12v10"/>'
    ),
    # --- patika simgeleri -------------------------------------------------
    # Python: iki iç içe geçmiş kıvrım, dilin logosuna gönderme.
    "python": (
        '<path d="M12 3c-3 0-4 1.4-4 3v2h8v1H6c-1.7 0-3 1.4-3 3.5S4.3 16 6 16h1.5"/>'
        '<path d="M12 21c3 0 4-1.4 4-3v-2H8v-1h10c1.7 0 3-1.4 3-3.5S19.7 8 18 8h-1.5"/>'
        '<circle cx="10" cy="6" r=".6" fill="currentColor"/>'
        '<circle cx="14" cy="18" r=".6" fill="currentColor"/>'
    ),
    # Veri bilimi: sütun grafiği.
    "chart": (
        '<path d="M3 21h18"/><path d="M6 21V10"/>'
        '<path d="M11 21V4"/><path d="M16 21v-7"/><path d="M21 21v-3"/>'
    ),
    # Makine öğrenmesi: birbirine bağlı düğümler.
    "network": (
        '<circle cx="5" cy="7" r="2"/><circle cx="5" cy="17" r="2"/>'
        '<circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/>'
        '<path d="M7 8.2 10.2 11"/><path d="M7 15.8 10.2 13"/><path d="M14 12h3"/>'
    ),
    # SQL: veritabanı silindiri.
    "database": (
        '<ellipse cx="12" cy="5.5" rx="8" ry="3"/>'
        '<path d="M4 5.5v13c0 1.7 3.6 3 8 3s8-1.3 8-3v-13"/>'
        '<path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>'
    ),
    # Kilit: içeriği henüz olmayan patikalarda.
    "lock": (
        '<rect x="4" y="10" width="16" height="10" rx="2"/>'
        '<path d="M8 10V7a4 4 0 0 1 8 0v3"/>'
    ),

    "scale": (
        '<path d="M12 3v18"/><path d="M7 21h10"/><path d="M5 7h14"/>'
        '<path d="m5 7-3 7h6z"/><path d="m19 7-3 7h6z"/>'
    ),
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


def icon(
    name: str,
    color: str = "#666F7D",
    size: int = 22,
    filled: bool = False,
    stroke: float = 2.0,
) -> QIcon:
    """İkonu istenen renk, boyut ve çizgi kalınlığında bir QIcon olarak üretir."""
    renderer = QSvgRenderer(
        QByteArray(svg_markup(name, color, stroke=stroke, filled=filled).encode("utf-8"))
    )

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
