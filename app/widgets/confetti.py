"""Konfeti (ui-taslak.md D2).

Yalnızca **büyük dönüm noktasında**: bir patikanın tamamı bitince (patika
ustalığı rozeti). Pencerenin üst ortasından bir kez patlar, 1,6 saniyede
düşüp söner; katman fareyi geçirir ve bitince kendini siler. En fazla 90
parça. Animasyonlar kapalıyken hiç çizilmez (kutlama kartı yine çıkar).
"""

from __future__ import annotations

import math
import random

from PySide6.QtCore import QElapsedTimer, QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget

from . import motion

DURATION_MS = 1600
COUNT = 90


class Confetti(QWidget):
    def __init__(self, parent: QWidget, colors: list[str]) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(parent.rect())
        rnd = random.Random()
        genislik = self.width()
        self._parts = [
            {
                "x": genislik / 2 + rnd.uniform(-40, 40), "y": 70.0,
                "vx": rnd.uniform(-8, 8), "vy": rnd.uniform(-9, -4),
                "r": rnd.uniform(0, math.tau), "vr": rnd.uniform(-0.18, 0.18),
                "s": rnd.uniform(5, 11), "c": QColor(rnd.choice(colors)),
                "kare": rnd.random() < 0.65,
            }
            for _ in range(COUNT)
        ]
        self._clock = QElapsedTimer()
        self._timer = QTimer(self)
        self._timer.setInterval(16)
        self._timer.timeout.connect(self._tick)

    def burst(self) -> None:
        if not motion.enabled():
            self.deleteLater()
            return
        self.show()
        self.raise_()
        self._clock.start()
        self._timer.start()

    def _tick(self) -> None:
        if self._clock.elapsed() >= DURATION_MS:
            self._timer.stop()
            self.hide()
            self.deleteLater()
            return
        for p in self._parts:
            p["vy"] += 0.32
            p["vx"] *= 0.985
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["r"] += p["vr"]
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        k = self._clock.elapsed() / DURATION_MS if self._clock.isValid() else 0.0
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        g.setOpacity(max(0.0, 1 - k * k))
        g.setPen(Qt.PenStyle.NoPen)
        for p in self._parts:
            g.save()
            g.translate(QPointF(p["x"], p["y"]))
            g.rotate(math.degrees(p["r"]))
            g.setBrush(p["c"])
            s = p["s"]
            if p["kare"]:
                g.drawRect(QRectF(-s / 2, -s / 4, s, s / 2))
            else:
                g.drawEllipse(QPointF(0, 0), s / 3, s / 3)
            g.restore()
