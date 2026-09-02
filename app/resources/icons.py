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
    # --- tema ------------------------------------------------------------
    "sun": (
        '<circle cx="12" cy="12" r="4"/>'
        '<path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41'
        'M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>'
    ),
    "moon": (
        '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>'
    ),
    # --- rozet ikonları ---------------------------------------------
    "star": (
        '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>'
    ),
    "flag": (
        '<path d="M4 22V3"/>'
        '<path d="M4 4h12l-2.5 4.5L16 13H4"/>'
    ),
    "trophy": (
        '<path d="M6 9H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h2"/>'
        '<path d="M18 9h2a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2h-2"/>'
        '<path d="M6 3h12v7a6 6 0 0 1-12 0V3z"/>'
        '<path d="M12 16v4"/>'
        '<path d="M8 20h8"/>'
    ),
    "calendar": (
        '<rect x="3" y="4" width="18" height="18" rx="2"/>'
        '<path d="M16 2v4M8 2v4M3 10h18"/>'
        '<path d="m9 16 2 2 4-4"/>'
    ),
    "zap": (
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>'
    ),
    "target": (
        '<circle cx="12" cy="12" r="10"/>'
        '<circle cx="12" cy="12" r="6"/>'
        '<circle cx="12" cy="12" r="2"/>'
    ),
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
    "play": (
        '<circle cx="12" cy="12" r="10"/>'
        '<polygon points="10 8 16 12 10 16 10 8"/>'
    ),
    "check": (
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    "rotate": (
        '<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/>'
    ),
    "book": (
        '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
        '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>'
    ),
    "file-text": (
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<path d="M14 2v6h6"/><path d="M8 13h8"/><path d="M8 17h8"/>'
    ),
    "clipboard": (
        '<rect x="8" y="2" width="8" height="4" rx="1"/>'
        '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>'
    ),
    "code": (
        '<polyline points="16 18 22 12 16 6"/>'
        '<polyline points="8 6 2 12 8 18"/>'
        '<line x1="14" y1="4" x2="10" y2="20"/>'
    ),
    "lightbulb": (
        '<path d="M9 18h6"/><path d="M10 22h4"/>'
        '<path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/>'
    ),
    "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    "flame": (
        '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>'
    ),
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    "link": (
        '<path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/>'
        '<path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/>'
    ),
    "info": (
        '<circle cx="12" cy="12" r="9"/>'
        '<path d="M12 11v5"/><path d="M12 7.6v.1"/>'
    ),
    "layers": (
        '<polygon points="12 2 2 7 12 12 22 7 12 2"/>'
        '<polyline points="2 12 12 17 22 12"/>'
        '<polyline points="2 17 12 22 22 17"/>'
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


# İki tonlu çizim için doldurulan "gövde" yolları.
#
# Yalnız çizgiden oluşan ikonlar şeritte cansız duruyordu. Her ikonun asıl
# gövdesi kendi renginde, düşük saydamlıkta doldurulunca simge ekrandan
# ayrılıyor ama tek renkli kalıyor — tema neyse ikon o.
#
# Kural basit: **çekirdek şekil dolu, gerisi çizgi.** Evin gövdesi, kişinin
# başı, megafonun konisi, dişlinin göbeği, bilgi dairesinin diski. Buraya
# yolu yazılmayan ikon eskisi gibi yalnızca çizgiyle çiziliyor.
DUOTONE: dict[str, str] = {
    "home": '<path d="M3 9.5 12 3l9 6.5V20a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "user": '<circle cx="12" cy="8" r="4"/>',
    "megaphone": '<path d="m3 11 15-7v16L3 13z"/>',
    "info": '<circle cx="12" cy="12" r="9"/>',
    "settings": '<circle cx="12" cy="12" r="3"/>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/>',
    "scale": "",
}

# Dolgunun saydamlığı. Daha koyusu çizgiyi yutuyor, daha açığı fark
# edilmiyor; ikisi arasında ölçülerek seçildi.
DUOTONE_OPACITY = 0.24


def svg_markup(
    name: str,
    color: str,
    stroke: float = 2.0,
    filled: bool = False,
    duotone: bool = False,
) -> str:
    """İkonu tam bir SVG belgesine sarar."""
    path = PATHS.get(name, PATHS["chevron-right"])
    fill = color if filled else "none"

    taban = ""
    if duotone and not filled:
        govde = DUOTONE.get(name, "")
        if govde:
            taban = (
                f'<g fill="{color}" fill-opacity="{DUOTONE_OPACITY}" '
                f'stroke="none">{govde}</g>'
            )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
        f"{taban}"
        f'<g fill="{fill}" stroke="{color}" stroke-width="{stroke}" '
        f'stroke-linecap="round" stroke-linejoin="round">{path}</g>'
        f"</svg>"
    )


def icon(
    name: str,
    color: str = "#666F7D",
    size: int = 22,
    filled: bool = False,
    stroke: float = 2.0,
    duotone: bool = False,
) -> QIcon:
    """İkonu istenen renk, boyut ve çizgi kalınlığında bir QIcon olarak üretir."""
    renderer = QSvgRenderer(
        QByteArray(
            svg_markup(
                name, color, stroke=stroke, filled=filled, duotone=duotone
            ).encode("utf-8")
        )
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
