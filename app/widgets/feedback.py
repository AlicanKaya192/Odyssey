"""Çalıştırma geri bildirimi (ui-taslak.md C6).

- `ButtonSpinner`: düğmenin simgesi dönen bir yaya dönüşür ("Çalışıyor…").
  Önce çalıştırırken düğme yalnızca devre dışı kalıyordu; bir şey olup
  olmadığı belli değildi.
- `EdgeFlash`: bir alanın (editör, cevap kutusu) çerçevesi kısa süre
  yeşil ya da kırmızı yanıp söner. Pencere ya da editör sallanmıyor;
  yalnızca kenar.
"""

from __future__ import annotations

import math

from PySide6.QtCore import QEvent, QObject, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QPushButton, QWidget

from . import motion


class ButtonSpinner(QObject):
    SIZE = 16

    def __init__(self, button: QPushButton, color: str = "#FFFFFF") -> None:
        super().__init__(button)
        self._button = button
        self._color = QColor(color)
        self._angle = 0.0
        self._saved_icon: QIcon | None = None
        self._timer = QTimer(self)
        self._timer.setInterval(16)
        self._timer.timeout.connect(self._tick)

    def start(self) -> None:
        if self._timer.isActive():
            return
        self._saved_icon = self._button.icon()
        self._angle = 0.0
        self._tick()
        self._timer.start()

    def stop(self) -> None:
        self._timer.stop()
        if self._saved_icon is not None:
            self._button.setIcon(self._saved_icon)
            self._saved_icon = None

    def _tick(self) -> None:
        # Tur 900 ms (prototip); animasyonlar kapalıyken yine döner ama
        # yavaş: bir şeyin çalıştığını anlatan tek işaret bu.
        self._angle = (self._angle + (6.4 if motion.enabled() else 2.0)) % 360
        oran = 2.0
        kenar = int(self.SIZE * oran)
        pix = QPixmap(kenar, kenar)
        pix.fill(Qt.GlobalColor.transparent)
        g = QPainter(pix)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(3, 3, kenar - 6, kenar - 6)
        iz = QColor(self._color)
        iz.setAlphaF(0.35)
        g.setPen(QPen(iz, 4))
        g.drawEllipse(r)
        g.setPen(QPen(self._color, 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        g.drawArc(r, int(-self._angle * 16), 100 * 16)
        g.end()
        pix.setDevicePixelRatio(oran)
        self._button.setIcon(QIcon(pix))


class EdgeFlash(QWidget):
    """Hedef widget'ın üstünde, çerçevesini kısa süre renklendiren katman."""

    def __init__(self, target: QWidget, radius: float = 12.0) -> None:
        super().__init__(target)
        self._target = target
        self._radius = radius
        self._color = QColor("#4ADE80")
        self._t = 0.0
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        target.installEventFilter(self)
        self.setGeometry(target.rect())
        self.hide()

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        if obj is self._target and event.type() == QEvent.Type.Resize:
            self.setGeometry(self._target.rect())
        return False

    def flash(self, color: str) -> None:
        """0 → 1 → 0, toplam 800 ms (en parlak an %35'te)."""
        if not motion.enabled():
            return
        self._color = QColor(color)
        self.setGeometry(self._target.rect())
        self.show()
        self.raise_()
        motion.animate(self, "t", 0.0, 1.0, self._set, 800, "linear", on_done=self.hide)

    def _set(self, v: float) -> None:
        self._t = v
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        k = self._t / 0.35 if self._t < 0.35 else (1 - self._t) / 0.65
        k = max(0.0, min(1.0, k))
        if k <= 0:
            return
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(self.rect()).adjusted(1.5, 1.5, -1.5, -1.5)
        halo = QColor(self._color)
        halo.setAlphaF(0.28 * k)
        g.setPen(QPen(halo, 6))
        g.setBrush(Qt.BrushStyle.NoBrush)
        g.drawRoundedRect(r.adjusted(2, 2, -2, -2), self._radius, self._radius)
        kenar = QColor(self._color)
        kenar.setAlphaF(k)
        g.setPen(QPen(kenar, 2))
        g.drawRoundedRect(r, self._radius, self._radius)
