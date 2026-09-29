"""Patika logosu (ui-taslak.md E2) ve üzerine gelince küçük hareketi.

Kartın üzerine gelince logo hafifçe döner (−6°) ve büyür (%8); yayla
oturduğu için canlı duruyor. Kilitli patikada logo gri ve hareketsiz.
"""

from __future__ import annotations

from PySide6.QtCore import Property, QPointF, QSize, Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from ..resources.logos import logo_pixmap
from . import motion


class LogoMark(QWidget):
    def __init__(self, key: str, color: str, size: int = 48, locked: bool = False,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._key, self._color, self._size, self._locked = key, color, size, locked
        self._hover = 0.0
        # Döndürülünce köşeler taşmasın diye biraz pay.
        pay = round(size * 0.12)
        self._pad = pay
        self.setFixedSize(size + 2 * pay, size + 2 * pay)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def sizeHint(self) -> QSize:  # noqa: N802
        return self.size()

    def _get_hover(self) -> float:
        return self._hover

    def _set_hover(self, v: float) -> None:
        self._hover = v
        self.update()

    hover = Property(float, _get_hover, _set_hover)

    def set_hovered(self, on: bool) -> None:
        if self._locked:
            return
        if on:
            motion.animate_property(self, "hover", 1.0, "spring", "spring")
        else:
            motion.animate_property(self, "hover", 0.0, "base", "out")

    def set_logo(self, key: str, color: str, locked: bool = False) -> None:
        self._key, self._color, self._locked = key, color, locked
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        merkez = QPointF(self.width() / 2, self.height() / 2)
        p.translate(merkez)
        p.rotate(-6 * self._hover)
        olcek = 1 + 0.08 * self._hover
        p.scale(olcek, olcek)
        pix = logo_pixmap(self._key, self._color, self._size, self._locked,
                          max(2.0, self.devicePixelRatioF() * 1.5))
        p.drawPixmap(QPointF(-self._size / 2, -self._size / 2), pix)
