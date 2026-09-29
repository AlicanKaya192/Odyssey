"""İlerleme çubuğu (ui-taslak.md B6).

`QProgressBar` QSS ile boyanıyordu ve değer değişince anında atlıyordu. Bu
çubuk kendisi çiziyor:

- dolu kısım rengin açık tonundan kendisine degrade;
- ekran açılınca **son görülen değerden** yeni değere doluyor (ilk görüşte
  0'dan); değer arttıysa dolunca ucunda kısa bir parlama geçiyor;
- son görülen değer `key` ile oturum boyunca bellekte tutuluyor,
  veritabanına yazılmıyor. Aynı ekrana dönünce değer değişmediyse hareket
  yok.
"""

from __future__ import annotations

from PySide6.QtCore import Property, QRectF, QSize, Qt
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath
from PySide6.QtWidgets import QSizePolicy, QWidget

from ..resources.theme.tokens import PALETTES, mix
from . import motion

# Oturum boyunca son gösterilen değerler (anahtar → yüzde).
_SHOWN: dict[str, float] = {}

HEIGHT = 7


class ProgressBar(QWidget):
    def __init__(self, key: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._key = key
        self._value = 0.0
        self._shine = 0.0
        self._color = QColor("#8B84FF")
        self._track = QColor("#272C36")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(HEIGHT)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(120, HEIGHT)

    # --- canlandırılan özellikler
    def _get_value(self) -> float:
        return self._value

    def _set_value(self, v: float) -> None:
        self._value = max(0.0, v)
        self.update()

    fill = Property(float, _get_value, _set_value)

    def _get_shine(self) -> float:
        return self._shine

    def _set_shine(self, v: float) -> None:
        self._shine = v
        self.update()

    shine = Property(float, _get_shine, _set_shine)

    # --- dışarıdan
    def set_key(self, key: str) -> None:
        self._key = key

    def set_color(self, color: str) -> None:
        self._color = QColor(color)
        self.update()

    def set_mode(self, mode: str) -> None:
        p = PALETTES.get(mode, PALETTES["dark"])
        self._track = QColor(p["surface_alt"] if mode == "dark" else p["border"])
        self.update()

    def set_percent(self, percent: float, animate: bool = True) -> None:
        """Yüzdeyi verir; `key` varsa son görülen değerden doldurur."""
        percent = max(0.0, min(100.0, float(percent)))
        onceki = _SHOWN.get(self._key, 0.0) if self._key else self._value
        if self._key:
            _SHOWN[self._key] = percent
        if not animate or not self.isVisible() and not self._key:
            motion.stop(self, "prop:fill")
            self._set_value(percent)
            return
        arti = percent > onceki and onceki > 0

        def parlama() -> None:
            if arti:
                motion.animate_property(self, "shine", 1.0, 700, "linear", start=0.0,
                                        on_done=lambda: self._set_shine(0.0))

        motion.animate_property(self, "fill", percent, "count", "out", start=onceki, on_done=parlama)

    def paintEvent(self, event) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(self.rect())
        yaricap = r.height() / 2
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(self._track)
        p.drawRoundedRect(r, yaricap, yaricap)
        genislik = r.width() * self._value / 100.0
        if genislik <= 0.5:
            return
        dolu = QRectF(r.left(), r.top(), max(genislik, r.height()), r.height())
        g = QLinearGradient(dolu.topLeft(), dolu.topRight())
        g.setColorAt(0.0, QColor(mix(self._color.name(), "#FFFFFF", 0.25)))
        g.setColorAt(1.0, self._color)
        yol = QPainterPath()
        yol.addRoundedRect(dolu, yaricap, yaricap)
        p.fillPath(yol, g)
        if 0.0 < self._shine < 1.0:
            # Ucun üstünden geçen beyaz ışık: önce parlıyor, sonra sönüyor.
            alfa = int(160 * (1 - abs(self._shine * 2 - 1)))
            isik = QLinearGradient(dolu.right() - 36, 0, dolu.right(), 0)
            isik.setColorAt(0.0, QColor(255, 255, 255, 0))
            isik.setColorAt(1.0, QColor(255, 255, 255, alfa))
            p.setClipPath(yol)
            p.fillRect(QRectF(dolu.right() - 36, dolu.top(), 36, dolu.height()), isik)
