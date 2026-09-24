"""Tutamağı görünen ayırıcı.

Alıştırmada yönerge ile editör, editör ile terminal arasındaki ayırıcı
sürüklenerek büyütülüp küçültülebiliyordu ama bunu gösteren hiçbir şey
yoktu; kişi imleci tam o çizginin üstüne getirmedikçe fark etmiyordu
(Alican bildirdi). Qt'nin varsayılan tutamağı boş bir şerit.

Burada tutamağın ortasında iki kısa paralel çizgili küçük bir hap
çiziliyor (yatay ayırıcıda dikey `||`, dikey ayırıcıda yatay `=`). Üzerine
gelince vurgu rengine dönüyor. Boyunca ince bir çizgi paneli ayırıyor.
"""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QSplitter, QSplitterHandle

from ..resources.theme.tokens import PALETTES

HANDLE_WIDTH = 9
PILL_LONG = 30
PILL_SHORT = 9


class GripHandle(QSplitterHandle):
    def __init__(self, orientation, parent) -> None:
        super().__init__(orientation, parent)
        self._hover = False
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

    def enterEvent(self, event) -> None:  # noqa: N802
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event) -> None:  # noqa: N802
        p = self.splitter().palette_tokens()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        yatay = self.orientation() == Qt.Orientation.Horizontal
        w, h = self.width(), self.height()

        # Boyunca ince ayırma çizgisi.
        cizgi = QColor(p["accent"] if self._hover else p["border"])
        painter.setPen(QPen(cizgi, 1))
        if yatay:
            painter.drawLine(QPointF(w / 2, 0), QPointF(w / 2, h))
        else:
            painter.drawLine(QPointF(0, h / 2), QPointF(w, h / 2))

        # Ortada tutamak hapı.
        if yatay:
            hap = QRectF((w - PILL_SHORT) / 2, (h - PILL_LONG) / 2, PILL_SHORT, PILL_LONG)
        else:
            hap = QRectF((w - PILL_LONG) / 2, (h - PILL_SHORT) / 2, PILL_LONG, PILL_SHORT)
        yol = QPainterPath()
        yol.addRoundedRect(hap, PILL_SHORT / 2, PILL_SHORT / 2)
        painter.fillPath(yol, QColor(p["accent_soft"] if self._hover else p["surface_alt"]))
        painter.setPen(QPen(QColor(p["accent"] if self._hover else p["border_strong"]), 1))
        painter.drawPath(yol)

        isaret = QPen(QColor(p["accent"] if self._hover else p["text_muted"]), 1.4)
        isaret.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(isaret)
        c = hap.center()
        for kay in (-1.6, 1.6):
            if yatay:
                painter.drawLine(QPointF(c.x() + kay, c.y() - 7), QPointF(c.x() + kay, c.y() + 7))
            else:
                painter.drawLine(QPointF(c.x() - 7, c.y() + kay), QPointF(c.x() + 7, c.y() + kay))
        painter.end()


class GripSplitter(QSplitter):
    """Tutamağı çizilen `QSplitter`; renkler temadan (`set_mode`)."""

    def __init__(self, orientation, parent=None) -> None:
        super().__init__(orientation, parent)
        self._mode = "light"
        self.setHandleWidth(HANDLE_WIDTH)
        self.setChildrenCollapsible(False)

    def createHandle(self):  # noqa: N802 (Qt adlandırması)
        return GripHandle(self.orientation(), self)

    def palette_tokens(self) -> dict:
        return PALETTES.get(self._mode, PALETTES["light"])

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        for index in range(1, self.count()):
            self.handle(index).update()
