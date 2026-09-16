"""Bir düğmenin üstünde açılan küçük pencere (bildirimler, kısayollar).

Çerçevesi, aşağı bakan oku, gölgesi ve dışarı tıklanınca kapanması burada;
içini dolduran panel kendi işine bakıyor. İki panel bunu paylaşıyor: aynı
çizim iki yere kopyalansaydı biri düzeltilip öbürü unutulurdu.

Pencere `Qt.Popup`: açıkken fare ve klavye onda, dışarı tıklamak ve Esc
kendiliğinden kapatıyor.
"""

from __future__ import annotations

from PySide6.QtCore import QPoint, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QVBoxLayout, QWidget

from ..resources.theme.tokens import PALETTES, RADIUS

# Gölgenin pencere kenarlarında kapladığı saydam pay.
SHADOW_MARGIN = 24
# Okun içeriğin sağ kenarına uzaklığı ve ölçüleri.
ARROW_RIGHT = 16
ARROW_HEIGHT = 10
ARROW_WIDTH = 16


class PopoverBody(QWidget):
    """İçeriği taşıyan katman: yuvarlak kutu, aşağı bakan ok, gölge."""

    def __init__(self, mode: str = "dark", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._mode = mode
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.apply_shadow()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.apply_shadow()
        self.update()

    def apply_shadow(self) -> None:
        from ..resources.theme.tokens import shadow_color

        r, g, b, a = shadow_color(self._mode, strong=True)
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(24)
        effect.setOffset(0, 4)
        effect.setColor(QColor(r, g, b, a))
        self.setGraphicsEffect(effect)

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)

        p = PALETTES.get(self._mode, PALETTES["dark"])
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        radius = RADIUS.get("md", 8)
        rect = QRectF(self.rect())
        rect.setHeight(rect.height() - ARROW_HEIGHT)
        # Kenarlık çizilirken köşeler kesilmesin diye yarım piksel pay.
        rect.adjust(0.5, 0.5, -0.5, -0.5)

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        # Okun ucu düğmenin ortasına geliyor; hizalamayı `Popover.show_above`
        # yapıyor, burada yeri sabit.
        merkez = rect.width() - ARROW_RIGHT
        ok = QPainterPath()
        # Üçgenin üst kenarı kutunun bir piksel içinden başlıyor: birleşince
        # aralarında çizgi kalmıyor, tek parça görünüyor.
        ok.moveTo(merkez - ARROW_WIDTH / 2, rect.bottom() - 1)
        ok.lineTo(merkez, rect.bottom() + ARROW_HEIGHT)
        ok.lineTo(merkez + ARROW_WIDTH / 2, rect.bottom() - 1)
        ok.closeSubpath()

        painter.setBrush(QColor(p["surface"]))
        painter.setPen(QPen(QColor(p["border"]), 1.0))
        painter.drawPath(path.united(ok))
        painter.end()


class Popover(QFrame):
    """Düğmenin üstünde açılan pencerenin ortak iskeleti.

    İçerik `self.content` düzenine ekleniyor; yüksekliği panel kendisi
    biliyor ve `fit_height` ile bildiriyor.
    """

    def __init__(self, width: int, parent: QWidget | None = None) -> None:
        super().__init__(
            parent,
            Qt.WindowType.Popup
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.NoDropShadowWindowHint,
        )
        self._mode = "dark"
        self._width = width
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFixedWidth(width + 2 * SHADOW_MARGIN)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(SHADOW_MARGIN, SHADOW_MARGIN, SHADOW_MARGIN, SHADOW_MARGIN)
        outer.setSpacing(0)

        self.body = PopoverBody(self._mode)
        outer.addWidget(self.body)

        self.content = QVBoxLayout(self.body)
        # Altta oka yer.
        self.content.setContentsMargins(0, 0, 0, ARROW_HEIGHT)
        self.content.setSpacing(0)

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.body.set_mode(mode)

    def fit_height(self, content_height: int) -> None:
        """Pencereyi içeriğin boyuna kilitler (ok ve gölge payları dahil).

        Esnek bırakılınca önceki açılıştan kalan yükseklik içeriği ortaya
        itiyordu.
        """
        self.setFixedHeight(content_height + ARROW_HEIGHT + 2 * SHADOW_MARGIN)

    def show_above(self, anchor: QWidget) -> None:
        """Pencereyi verilen düğmenin hemen üstünde açar."""
        nokta = anchor.mapToGlobal(QPoint(0, 0))
        # Okun ucu düğmenin ortasına gelsin: ok içeriğin sağından
        # ARROW_RIGHT, içerik de pencerenin kenarından SHADOW_MARGIN içeride.
        x = nokta.x() + anchor.width() // 2 + SHADOW_MARGIN + ARROW_RIGHT - self.width()
        y = nokta.y() - self.height() + SHADOW_MARGIN - 4
        self.move(x, y)
        self.show()

    def mousePressEvent(self, event) -> None:  # noqa: N802
        """Gölge payına (içeriğin dışına) tıklamak da kapatıyor."""
        if not self.body.geometry().contains(event.pos()):
            self.close()
        else:
            super().mousePressEvent(event)
