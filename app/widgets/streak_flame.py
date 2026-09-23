"""Günlük serinin alevi: seri uzadıkça rengi ve boyu değişiyor.

Karşılama kartında "günlük seri" etiketinin yanında duruyor. Sabit bir 🔥
emojisi yedi günlük seriyle yetmiş günlük seriyi ayırt etmiyordu; Alican
serinin büyüdükçe görünür olmasını istedi. Aşamalar gerçek bir alevin
ısındıkça geçirdiği renklerden: sarı kıvılcım, turuncu alev, kırmızı ateş,
mavi alev, beyaz-sıcak alev; yüz günü geçen seriye altın alev.

Alev emoji değil, çiziliyor: emojinin rengi değiştirilemiyor ve her
Windows sürümünde farklı görünüyor.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QByteArray, QRectF, Qt
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer


@dataclass(frozen=True)
class FlameTier:
    """Bir aşama: kaç günde başladığı, adı (çeviri anahtarı) ve renkleri."""

    min_days: int
    key: str
    top: str      # alevin ucu
    bottom: str   # alevin dibi
    core: str     # içteki parlak çekirdek
    size: int     # piksel
    glow: int = 0  # arkadaki parıltının opaklığı (0-255); sıcak aşamalarda


# Boylar ve renkler mor zeminde ayırt edilecek kadar farklı seçildi: ilk
# denemede 14-19 piksellik alevler etiketin yanında seçilmiyordu, sarı ile
# turuncu ve iki mavi birbirine karışıyordu.
TIERS: tuple[FlameTier, ...] = (
    FlameTier(1, "spark", "#FEF9C3", "#FACC15", "#FFFFFF", 15),
    FlameTier(3, "flame", "#FDBA74", "#EA580C", "#FEF08A", 17),
    FlameTier(7, "fire", "#FCA5A5", "#B91C1C", "#FDE047", 19),
    FlameTier(14, "blue", "#BAE6FD", "#1D4ED8", "#FFFFFF", 21, 70),
    FlameTier(30, "white", "#FFFFFF", "#06B6D4", "#FFFFFF", 23, 110),
    FlameTier(100, "gold", "#FEF08A", "#B45309", "#FFFFFF", 25, 130),
)

# Lucide "flame" dış hattı (24x24). Çekirdek aynı şeklin küçültülmüşü.
_FLAME = (
    "M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 "
    "2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-"
    "2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"
)


def tier_for(days: int) -> FlameTier | None:
    """Serinin aşaması; seri yoksa None."""
    current = None
    for tier in TIERS:
        if days >= tier.min_days:
            current = tier
    return current


def next_tier(days: int) -> FlameTier | None:
    """Bir sonraki aşama; en üstteyse None."""
    for tier in TIERS:
        if days < tier.min_days:
            return tier
    return None


def _svg(tier: FlameTier | None) -> str:
    if tier is None:
        # Seri yok: soluk, içi boş bir alev. Tamamen gizlemek "seri diye
        # bir şey var" bilgisini de siliyordu.
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
            f'<path d="{_FLAME}" fill="none" stroke="#FFFFFF" stroke-opacity="0.55" '
            'stroke-width="2" stroke-linejoin="round"/></svg>'
        )
    glow = ""
    if tier.glow:
        # Sıcak aşamalarda alevin arkasında yumuşak bir hale.
        glow = (
            '<radialGradient id="h" cx="0.5" cy="0.62" r="0.5">'
            f'<stop offset="0" stop-color="{tier.top}" stop-opacity="{tier.glow / 255:.2f}"/>'
            f'<stop offset="1" stop-color="{tier.top}" stop-opacity="0"/>'
            "</radialGradient>"
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{tier.top}"/>'
        f'<stop offset="1" stop-color="{tier.bottom}"/>'
        f"</linearGradient>{glow}</defs>"
        + ('<circle cx="12" cy="14" r="12" fill="url(#h)"/>' if tier.glow else "")
        # Alev, parıltıya yer kalsın diye biraz küçültülmüş.
        + '<g transform="translate(12 13) scale(0.86) translate(-12 -13)">'
        f'<path d="{_FLAME}" fill="url(#g)"/>'
        # Çekirdek: alt ortadan küçültülmüş aynı şekil.
        f'<path d="{_FLAME}" fill="{tier.core}" fill-opacity="0.9" '
        'transform="translate(12 22) scale(0.45) translate(-12 -22)"/>'
        "</g></svg>"
    )


def flame_pixmap(days: int, device_ratio: float = 1.0) -> QPixmap:
    """Serinin alevini ekran ölçeğine uygun, net bir resim olarak verir."""
    tier = tier_for(days)
    size = tier.size if tier else 15
    edge = max(1, round(size * device_ratio))
    image = QPixmap(edge, edge)
    image.fill(Qt.GlobalColor.transparent)
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    QSvgRenderer(QByteArray(_svg(tier).encode("utf-8"))).render(
        painter, QRectF(0, 0, edge, edge)
    )
    painter.end()
    image.setDevicePixelRatio(device_ratio)
    return image
