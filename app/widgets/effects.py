"""Qt stil dosyalarının veremediği görsel etkiler.

QSS `box-shadow` desteklemiyor. Maketteki kart gölgelerini elde etmek için
`QGraphicsDropShadowEffect` kullanılıyor; renkler yine `tokens.py`'den
geliyor ki tema değişince gölge de değişsin.
"""

from __future__ import annotations

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QWidget

from ..resources.theme.tokens import shadow_color


def apply_shadow(
    widget: QWidget,
    mode: str = "light",
    strong: bool = False,
    blur: int | None = None,
    offset_y: int | None = None,
) -> QGraphicsDropShadowEffect:
    """Bir widget'a yumuşak gölge verir.

    `strong=True` öne çıkan kartlar için (karşılama kartı, açılır pencere),
    varsayılan ise sıradan kartlar için.
    """
    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(blur if blur is not None else (40 if strong else 24))
    effect.setXOffset(0)
    effect.setYOffset(offset_y if offset_y is not None else (12 if strong else 6))
    effect.setColor(QColor(*shadow_color(mode, strong)))
    widget.setGraphicsEffect(effect)
    return effect


def refresh_shadow(widget: QWidget, mode: str, strong: bool = False) -> None:
    """Tema değiştiğinde gölge rengini günceller."""
    effect = widget.graphicsEffect()
    if isinstance(effect, QGraphicsDropShadowEffect):
        effect.setColor(QColor(*shadow_color(mode, strong)))


def repolish(widget: QWidget) -> None:
    """Qt özelliği (property) değişince stilin yeniden uygulanmasını sağlar.

    `setProperty` tek başına görünümü değiştirmiyor; stil motorunun widget'ı
    yeniden değerlendirmesi gerekiyor.
    """
    style = widget.style()
    style.unpolish(widget)
    style.polish(widget)
    widget.update()
