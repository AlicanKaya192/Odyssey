"""Çıkış penceresinin sahnesi: alacakaranlıkta el sallayan sentor.

Açılış animasyonu sabahın morunda başlıyor; çıkış akşamın morunda bitiyor.
Gökyüzü koyulaşmış, hilal doğmuş, yıldızlar parıldıyor. Sentor yayını
indirmiş, çeken elini başının üstüne kaldırıp sallıyor; arada bir ön
toynağıyla yeri eşeliyor. Başka hiçbir yerde olmayan bir duruş (Alican:
"farklı modelle").

Döngü kısa (`CYCLE`): kutu çoğu zaman birkaç saniye açık kalıyor, el
sallama ilk yarım saniyede başlıyor ki görülmeden kapanmasın.
"""

from __future__ import annotations

import math
import random
import time
from dataclasses import replace

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath, QPen, QRadialGradient
from PySide6.QtWidgets import QSizePolicy, QWidget

from ..widgets import centaur as C
from .intro import GROUND_OUT, HILL, INK, SPARK, STYLE
from .update_scene import _alpha, _meander

CYCLE = 5.2               # sn: el sallama + eşeleme + dinlenme
FIG_TOP = 128.0           # figürün en üstü (kalkık el), figür biriminde
FIG_CENTER = 330.0        # figürün yatay ortası, figür biriminde

# Akşam gökyüzü: tepede gece, ufukta uygulamanın morunun son ışığı.
SKY_TOP = QColor("#150F3A")
SKY_MID = QColor("#33278F")
SKY_LOW = QColor("#6A5BE6")
MOON = QColor("#F1EEFF")

# Kalkık ön toynak: diz katlanmış, toynak karnın altına doğru.
PAW_LEG = (26.0, 34.0, -98.0, -6.0, 8.0)


def _ease(t: float) -> float:
    return C.smoothstep(t)


class FarewellScene(QWidget):
    """El sallayan sentor, hilal ve yıldızlar."""

    def __init__(self, radius: float = 18.0, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._radius = radius
        self._t = 0.0
        self._base = replace(C.aim_pose(), draw=0.0, hand_rest=1.0, bow_lower=38.0)
        rnd = random.Random(11)
        # (x oranı, y oranı, boy, evre, hız): yıldızlar gökyüzünün üst üçte ikisinde.
        self._stars = [(rnd.uniform(.02, .98), rnd.uniform(.05, .55), rnd.uniform(.7, 1.7),
                        rnd.uniform(0, 2 * math.pi), rnd.uniform(.8, 1.9)) for _ in range(26)]
        self.setMinimumHeight(150)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._last = time.monotonic()
        self._timer = QTimer(self)
        self._timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._timer.setInterval(16)
        self._timer.timeout.connect(self._tick)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        self._last = time.monotonic()
        self._timer.start()

    def hideEvent(self, event) -> None:  # noqa: N802
        super().hideEvent(event)
        self._timer.stop()

    def _tick(self) -> None:
        simdi = time.monotonic()
        self._t += min(0.05, simdi - self._last)
        self._last = simdi
        self.update()

    # --- duruş ---------------------------------------------------------------------------

    def pose(self, t: float) -> C.Pose:
        """`t` anındaki duruş (test ve görüntü için dışarıdan da çağrılıyor)."""
        k = t % CYCLE

        def ara(a: float, b: float) -> float:
            return _ease((k - a) / (b - a))

        # El: 0,15'te kalkıyor, 2,5'e kadar sallanıyor, 3,0'da iniyor.
        wave = ara(.15, .6) - ara(2.5, 3.0)
        swing = math.sin((k - .45) * 2 * math.pi * 1.6) if .45 < k < 2.8 else 0.0
        # Ön toynak: 3,4–4,4 arası kalkıp iki kez eşeliyor.
        paw = ara(3.4, 3.65) - ara(4.2, 4.5)
        eselme = 6 * math.sin((k - 3.65) * 2 * math.pi * 2.2) if 3.65 < k < 4.2 else 0.0
        legs = dict(self._base.legs)
        if paw > 0:
            yere = legs["fn"]
            kalkik = list(PAW_LEG)
            kalkik[0] += eselme
            legs["fn"] = [C.lerp(a, b, paw) for a, b in zip(yere, kalkik)]
        return replace(
            self._base,
            legs=legs,
            wave=wave,
            wave_swing=swing * min(1.0, wave * 1.4),
            head_tilt=-3 * wave + 2 * paw,
            lean=0.8 * math.sin(t * 2 * math.pi / 4.4) - 1.5 * wave,
            tail=4 * math.sin(t * 2 * math.pi / 3.1) + 2 + 5 * paw,
        )

    # --- çizim ---------------------------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802
        self.paint_at(QPainter(self), self._t, self.width(), self.height())

    def paint_at(self, p: QPainter, t: float, w: float, h: float) -> None:
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        shape = QPainterPath()
        shape.addRoundedRect(QRectF(0, 0, w, h), self._radius, self._radius)
        p.setClipPath(shape)
        ground = h - 30.0
        s = (ground - 10.0) / (C.GROUND - FIG_TOP)

        sky = QLinearGradient(QPointF(0, 0), QPointF(0, ground))
        sky.setColorAt(0.0, SKY_TOP)
        sky.setColorAt(0.6, SKY_MID)
        sky.setColorAt(1.0, SKY_LOW)
        p.fillRect(QRectF(0, 0, w, h), sky)

        self._paint_stars(p, t, w, ground)
        self._paint_moon(p, QPointF(w * .8, h * .3), h * .15)

        # uzak ve yakın tepeler
        for oran, yuk, renk in ((.55, 34, _alpha(HILL, .55)), (.8, 20, _alpha(INK, .35))):
            yol = QPainterPath(QPointF(0, ground))
            adim = w * oran
            x = -adim * .3
            while x < w + adim:
                yol.cubicTo(x + adim * .2, ground - yuk, x + adim * .4, ground - yuk * 1.1, x + adim * .55, ground - yuk * .3)
                yol.cubicTo(x + adim * .7, ground, x + adim * .85, ground - yuk * .6, x + adim, ground)
                x += adim
            yol.lineTo(w, ground + 2)
            yol.lineTo(0, ground + 2)
            yol.closeSubpath()
            p.fillPath(yol, renk)

        p.fillRect(QRectF(0, ground, w, h - ground), _alpha(GROUND_OUT, .55))
        p.setPen(QPen(INK, 2.2))
        p.drawLine(QPointF(0, ground), QPointF(w, ground))
        _meander(p, 4, h - 16, w, 24.0, 9, _alpha(INK, .8))

        pose = self.pose(t)
        fig_x = w * .36 - FIG_CENTER * s
        # Figürün altında ay ışığı: siyah figür koyu gökte kaybolmasın.
        isik = QRadialGradient(QPointF(fig_x + FIG_CENTER * s, ground - 90 * s), 230 * s)
        isik.setColorAt(0, _alpha(SKY_LOW, .55))
        isik.setColorAt(1, _alpha(SKY_LOW, 0))
        p.fillRect(QRectF(0, 0, w, ground), isik)

        p.save()
        p.translate(fig_x, ground - C.GROUND * s)
        p.scale(s, s)
        C.draw_centaur(p, pose, STYLE)
        p.restore()
        p.end()

    def _paint_stars(self, p: QPainter, t: float, w: float, ground: float) -> None:
        p.setPen(Qt.PenStyle.NoPen)
        for xo, yo, boy, evre, hiz in self._stars:
            parilti = .45 + .55 * (.5 + .5 * math.sin(t * hiz * 2.2 + evre))
            p.setBrush(_alpha(SPARK, .85 * parilti))
            merkez = QPointF(xo * w, yo * ground)
            p.drawEllipse(merkez, boy, boy)
            if boy > 1.4:
                # iri yıldızlarda ince bir haç parıltısı
                p.setPen(QPen(_alpha(SPARK, .35 * parilti), .8))
                p.drawLine(merkez + QPointF(-boy * 3, 0), merkez + QPointF(boy * 3, 0))
                p.drawLine(merkez + QPointF(0, -boy * 3), merkez + QPointF(0, boy * 3))
                p.setPen(Qt.PenStyle.NoPen)

    def _paint_moon(self, p: QPainter, c: QPointF, r: float) -> None:
        hale = QRadialGradient(c, r * 3.2)
        hale.setColorAt(0, _alpha(MOON, .28))
        hale.setColorAt(1, _alpha(MOON, 0))
        p.fillRect(QRectF(c.x() - r * 3.2, c.y() - r * 3.2, r * 6.4, r * 6.4), hale)
        dolu = QPainterPath()
        dolu.addEllipse(c, r, r)
        golge = QPainterPath()
        golge.addEllipse(c + QPointF(r * .45, -r * .2), r * .92, r * .92)
        p.fillPath(dolu.subtracted(golge), MOON)
