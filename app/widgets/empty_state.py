"""Boş durum kartı (ui-taslak.md B10).

Boş ekranlar düz bir cümleydi ("Henüz notun yok…"); sayfanın ortasında
kaybolup gidiyordu. Şimdi ortalanmış bir kart: ışıyan bir dairenin içinde
büyük simge (esneyerek belirir), başlık, bir cümle ve isteğe bağlı bir
düğme.
"""

from __future__ import annotations

from PySide6.QtCore import Property, QPointF, QSize, Qt, Signal
from PySide6.QtGui import QColor, QPainter, QRadialGradient
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from ..resources.icons import MODERN_FILL_HOVER, icon
from ..resources.theme.motion import bounce
from . import motion

BUBBLE = 96
ICON = 44


class _Bubble(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(BUBBLE, BUBBLE)
        self._icon = "notebook"
        self._color = QColor("#34D399")
        self._pop = 1.0

    def _get(self) -> float:
        return self._pop

    def _set(self, v: float) -> None:
        self._pop = v
        self.update()

    pop = Property(float, _get, _set)

    def set_icon(self, name: str, color: str) -> None:
        self._icon, self._color = name, QColor(color)
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        olcek = bounce(self._pop)
        if olcek <= 0.01:
            return
        m = QPointF(self.width() / 2, self.height() / 2)
        g.translate(m)
        g.scale(olcek, olcek)
        isik = QRadialGradient(QPointF(0, 0), BUBBLE / 2)
        c = QColor(self._color)
        c.setAlphaF(0.24)
        isik.setColorAt(0.0, c)
        c.setAlphaF(0.0)
        isik.setColorAt(0.68, c)
        g.setPen(Qt.PenStyle.NoPen)
        g.setBrush(isik)
        g.drawEllipse(QPointF(0, 0), BUBBLE / 2, BUBBLE / 2)
        pix = icon(self._icon, self._color.name(), ICON, fill_opacity=MODERN_FILL_HOVER).pixmap(ICON, ICON)
        g.drawPixmap(QPointF(-ICON / 2, -ICON / 2), pix)


class EmptyState(QWidget):
    action = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        # Zemin yok: bulunduğu kartın rengi görünsün (aramada koyu kutu kalıyordu).
        self.setProperty("role", "bare")
        dis = QVBoxLayout(self)
        dis.addStretch(1)
        ic = QWidget()
        ic.setProperty("role", "bare")
        # Prototip `.empty .in`: 360 piksellik sütun; daraltınca metin gereksiz sarılıyordu.
        ic.setFixedWidth(360)
        lay = QVBoxLayout(ic)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)
        self._bubble = _Bubble()
        lay.addWidget(self._bubble, 0, Qt.AlignmentFlag.AlignHCenter)
        self._title = QLabel()
        self._title.setProperty("role", "empty-title")
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self._title)
        self._text = QLabel()
        self._text.setProperty("role", "empty-text")
        self._text.setWordWrap(True)
        self._text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self._text)
        self._button = QPushButton()
        self._button.setProperty("variant", "primary")
        self._button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._button.clicked.connect(self.action)
        self._button.hide()
        lay.addSpacing(4)
        lay.addWidget(self._button, 0, Qt.AlignmentFlag.AlignHCenter)
        dis.addWidget(ic, 0, Qt.AlignmentFlag.AlignHCenter)
        dis.addStretch(1)

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(380, 260)

    def set_content(self, icon_name: str, color: str, title: str, text: str,
                    button: str = "", button_icon: str = "plus") -> None:
        self._bubble.set_icon(icon_name, color)
        self._title.setText(title)
        self._title.setVisible(bool(title))
        self._text.setText(text)
        self._button.setVisible(bool(button))
        if button:
            self._button.setText("  " + button)
            self._button.setIcon(icon(button_icon, "#FFFFFF", 16))

    def play(self) -> None:
        """Simge esneyerek belirir."""
        motion.animate_property(self._bubble, "pop", 1.0, "bounce", "linear", start=0.0)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        from .fade_stack import after_reveal
        if motion.enabled():
            self._bubble.pop = 0.0  # geçiş başlayana kadar görünmez
        after_reveal(self, self.play)
