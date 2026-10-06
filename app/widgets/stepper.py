"""Alıştırma ilerleme şeridi (ui-taslak.md C6, F4).

Numaralar tek tek kutu olarak duruyordu (`1 ✓  2  3`). Şimdi aralarında
çizgi olan yuvarlak adımlar: çözülen adım patika renginde dolu ve içinde
onay, açık olan halkalı, aradaki çizgi iki uç da çözüldüyse dolu.

Bir adım yeni çözüldüğünde onay esneyerek (`bounce`) beliriyor ve sonraki
adıma giden çizgi dolarak uzuyor. Hangisinin yeni olduğu bir önceki çizimle
karşılaştırılarak bulunuyor.
"""

from __future__ import annotations

from PySide6.QtCore import Property, QPointF, QRectF, QSize, Qt, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from ..resources.theme.motion import bounce
from ..resources.theme.tokens import mix
from . import motion, tips
from .effects import theme_palette

DOT = 34
GAP = 28


class Stepper(QWidget):
    clicked = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._done: list[bool] = []
        self._current = 0
        self._tips: list[str] = []
        self._color = QColor("#8B84FF")
        self._fresh = -1
        self._pop = 1.0
        self._hover = -1
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def _get_pop(self) -> float:
        return self._pop

    def _set_pop(self, v: float) -> None:
        self._pop = v
        self.update()

    pop = Property(float, _get_pop, _set_pop)

    def set_color(self, color: str) -> None:
        self._color = QColor(color)
        self.update()

    def reset(self) -> None:
        """Başka bir bölüme geçilince: önceki durum karşılaştırılmasın."""
        self._done = []
        self._fresh = -1

    def set_steps(self, done: list[bool], current: int, tips: list[str] | None = None) -> None:
        onceki = self._done
        yeni = -1
        if len(onceki) == len(done):
            for i, (a, b) in enumerate(zip(onceki, done)):
                if b and not a:
                    yeni = i
        self._done = list(done)
        self._current = current
        self._tips = tips or []
        self.setFixedSize(self.sizeHint())
        if yeni >= 0:
            self._fresh = yeni
            motion.animate_property(self, "pop", 1.0, "bounce", "linear", start=0.0,
                                    on_done=lambda: setattr(self, "_fresh", -1))
        self.update()

    def sizeHint(self) -> QSize:  # noqa: N802
        n = max(1, len(self._done))
        return QSize(n * DOT + (n - 1) * GAP + 8, DOT + 8)

    def _center(self, i: int) -> QPointF:
        return QPointF(4 + DOT / 2 + i * (DOT + GAP), 4 + DOT / 2)

    def _index_at(self, pos) -> int:
        for i in range(len(self._done)):
            if (QPointF(pos) - self._center(i)).manhattanLength() < DOT * 0.7:
                return i
        return -1

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        i = self._index_at(event.position())
        if i != self._hover:
            self._hover = i
            self.update()
            if 0 <= i < len(self._tips):
                tips.show_text(event.globalPosition().toPoint(), self._tips[i], self)

    def leaveEvent(self, event) -> None:  # noqa: N802
        self._hover = -1
        self.update()

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        i = self._index_at(event.position())
        if i >= 0 and event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(i)

    def paintEvent(self, event) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        renk = theme_palette()
        bos = QColor(renk["surface_alt"])
        vurgu = QColor(renk["accent"])
        n = len(self._done)
        # Çizgiler: iki ucu da çözülmüşse dolu. Yeni çözülende dolarak uzuyor.
        for i in range(n - 1):
            a, b = self._center(i), self._center(i + 1)
            x0, x1 = a.x() + DOT / 2 + 2, b.x() - DOT / 2 - 2
            p.setPen(QPen(bos, 2))
            p.drawLine(QPointF(x0, a.y()), QPointF(x1, a.y()))
            if self._done[i] and self._done[i + 1]:
                oran = 1.0
                if self._fresh in (i, i + 1):
                    oran = max(0.0, min(1.0, self._pop))
                p.setPen(QPen(self._color, 2))
                p.drawLine(QPointF(x0, a.y()), QPointF(x0 + (x1 - x0) * oran, a.y()))
        f = QFont(self.font())
        f.setPixelSize(13)
        f.setWeight(QFont.Weight.Bold)
        p.setFont(f)
        for i in range(n):
            c = self._center(i)
            r = DOT / 2
            if self._hover == i:
                r += 1.5
            daire = QRectF(c.x() - r, c.y() - r, 2 * r, 2 * r)
            if self._done[i]:
                if i == self._current:
                    halka = QColor(self._color)
                    halka.setAlphaF(0.35)
                    p.setPen(QPen(halka, 3))
                    p.setBrush(Qt.BrushStyle.NoBrush)
                    p.drawEllipse(daire.adjusted(-3, -3, 3, 3))
                p.setPen(Qt.PenStyle.NoPen)
                p.setBrush(self._color)
                p.drawEllipse(daire)
                olcek = bounce(self._pop) if i == self._fresh else 1.0
                p.save()
                p.translate(c)
                p.scale(olcek, olcek)
                p.setPen(QPen(QColor("#FFFFFF"), 2.6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                              Qt.PenJoinStyle.RoundJoin))
                p.drawPolyline([QPointF(-5.5, 0.5), QPointF(-1.5, 4.5), QPointF(6, -4)])
                p.restore()
            elif i == self._current:
                p.setPen(QPen(vurgu, 2))
                p.setBrush(QColor(mix(renk["bg"], renk["accent"], 0.16)))
                p.drawEllipse(daire.adjusted(1, 1, -1, -1))
                p.setPen(vurgu)
                p.drawText(daire, Qt.AlignmentFlag.AlignCenter, str(i + 1))
            else:
                p.setPen(Qt.PenStyle.NoPen)
                p.setBrush(bos)
                p.drawEllipse(daire)
                p.setPen(QColor(renk["text_muted"]))
                p.drawText(daire, Qt.AlignmentFlag.AlignCenter, str(i + 1))
