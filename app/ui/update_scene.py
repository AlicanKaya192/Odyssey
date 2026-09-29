"""Güncelleme pencerelerinin sahnesi: sentor ve hedefi.

Açılış animasyonunun dili (`app/ui/intro.py`) güncellemede de sürüyor:

- **idle** — yeni sürüm kutusunda sentor nişan alıp bekliyor.
- **run** — indirme sürerken dörtnala koşuyor; zemin, tepeler ve rüzgâr
  akıyor. Koşu, işin sürdüğünü donmuş bir pencereden ayırıyor.
- **shoot** — indirme ve denetim bitince yayı gerip atıyor, ok hedefi tam
  ortadan vuruyor; sahne `finished` yayıyor ve kurulum başlıyor. Yeni
  sürüm açılış animasyonuyla açılıyor: hikâye oradan devam ediyor.

Sahne kendi boyutuna göre ölçekleniyor; figürün boyu yüksekliğe bağlı.
Görünmezken ve pencere küçültülmüşken zamanlayıcı duruyor.
"""

from __future__ import annotations

import math
import random
import time
from dataclasses import replace

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath, QPen, QRadialGradient
from PySide6.QtWidgets import QSizePolicy, QWidget

from ..widgets import centaur as C
from .intro import GROUND_IN, GROUND_MID, GROUND_OUT, HILL, INCISE, INK, INK_FAR, RING_LIGHT, SPARK, STYLE

GALLOP_PERIOD = 0.42
RUN_SPEED = 520.0         # figür biriminde zeminin akış hızı (px/sn)
DRAW_TIME, FLIGHT_TIME = 0.35, 0.4
SETTLE_TIME = 0.65        # vuruştan sonra sahnenin durulması
FIG_TOP = 136.0           # figürün en üstü (yay ucu), figür biriminde
ARROW_Y = 211.8           # okun yüksekliği, figür biriminde
FIG_LEFT, FIG_RIGHT = 155.0, 528.0
TARGET_R = 54.0           # hedefin yarıçapı, figür biriminde


def _ease_out(t: float) -> float:
    t = C.clamp01(t)
    return 1 - (1 - t) ** 3


def _alpha(color: QColor, a: float) -> QColor:
    c = QColor(color)
    c.setAlphaF(max(0.0, min(1.0, a)))
    return c


def _meander(p: QPainter, x0: float, top: float, width: float, unit: float, height: float,
             color: QColor) -> None:
    """Menderes şeridi (açılıştaki bordürün küçüğü): kancalar ve taban çizgisi."""
    kalem = QPen(color, 1.6)
    kalem.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
    p.setPen(kalem)
    p.setBrush(Qt.BrushStyle.NoBrush)
    yol = QPainterPath()
    x = x0
    while x < x0 + width:
        yol.moveTo(x, top + height)
        yol.lineTo(x, top)
        yol.lineTo(x + unit * .75, top)
        yol.lineTo(x + unit * .75, top + height * .72)
        yol.lineTo(x + unit * .3, top + height * .72)
        yol.lineTo(x + unit * .3, top + height * .36)
        x += unit
    yol.moveTo(x0, top + height)
    yol.lineTo(x0 + width, top + height)
    p.drawPath(yol)


class UpdateScene(QWidget):
    """Sentorun koştuğu, nişan aldığı ve vurduğu küçük sahne."""

    finished = Signal()  # atış bitti (ok saplandı, sahne duruldu)

    def __init__(self, mode: str = "idle", radius: float = 18.0, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._mode = mode
        self._radius = radius
        self._t = 0.0
        self._phase = 0.0          # dörtnal evresi (döngü sayısı)
        self._scroll = 0.0         # zeminin akışı (figür biriminde)
        self._speed = 1.0          # koşunun hızı (atıştan sonra yavaşlıyor)
        self._shoot_at: float | None = None
        self._release: tuple | None = None  # (kertik, uç) ekranda
        self._done = False
        self._aim = C.aim_pose()
        rnd = random.Random(3)
        self._streaks = [(rnd.uniform(.15, .8), rnd.uniform(0, 1), rnd.uniform(.7, 1.3), rnd.uniform(60, 150),
                          rnd.random() < .35) for _ in range(12)]
        self.setMinimumHeight(150)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        self._last = time.monotonic()
        self._timer = QTimer(self)
        self._timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._timer.setInterval(16)
        self._timer.timeout.connect(self._tick)

    # --- durum -------------------------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.update()

    def shoot(self) -> None:
        """Koşarken yayı gerip atar; ok hedefe saplanınca `finished`."""
        if self._shoot_at is None:
            if self._mode != "run":
                self._mode = "run"
            self._shoot_at = self._t

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        self._last = time.monotonic()
        self._timer.start()

    def hideEvent(self, event) -> None:  # noqa: N802
        super().hideEvent(event)
        self._timer.stop()

    def _tick(self) -> None:
        simdi = time.monotonic()
        dt = min(0.05, simdi - self._last)
        self._last = simdi
        # Küçültülmüşken çizim yok; ama atış başladıysa zaman akıyor, yoksa
        # ok hiç saplanmaz ve kurulum başlamazdı.
        pencere = self.window()
        if pencere is not None and pencere.isMinimized() and self._shoot_at is None:
            return
        self._t += dt
        if self._mode == "run":
            if self._shoot_at is not None:
                k = self._t - self._shoot_at - DRAW_TIME - FLIGHT_TIME
                self._speed = 1 - C.smoothstep(k / SETTLE_TIME) * 0.85
                if k > SETTLE_TIME and not self._done:
                    self._done = True
                    self.finished.emit()
            self._phase += dt / GALLOP_PERIOD * self._speed
            self._scroll += dt * RUN_SPEED * self._speed
        self.update()

    # --- yerleşim ----------------------------------------------------------------------

    def _layout(self):
        w, h = self.width(), self.height()
        ground = h - 30.0
        s = (ground - 12.0) / (C.GROUND - FIG_TOP)
        fig_x = w * 0.08 - FIG_LEFT * s
        target = QPointF(w - 30 - TARGET_R * s, ground - (C.GROUND - ARROW_Y) * s)
        return w, h, ground, s, fig_x, target

    def _pose(self) -> C.Pose:
        if self._mode == "idle":
            t = self._t
            return replace(self._aim, lean=0.7 * math.sin(t * 2 * math.pi / 4.2),
                           tail=4 * math.sin(t * 2 * math.pi / 3.1) + 2)
        pose = C.gallop_pose(self._phase)
        pose.draw = 0.62
        if self._shoot_at is not None:
            k = self._t - self._shoot_at
            if k < DRAW_TIME:
                pose.draw = 0.62 + 0.38 * C.smoothstep(k / DRAW_TIME)
            else:
                r = k - DRAW_TIME
                pose.released = True
                pose.vib = 8 * math.exp(-r / .09) * math.cos(2 * math.pi * 26 * r)
                pose.follow = _ease_out(r / .22)
        return pose

    # --- çizim -------------------------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h, ground, s, fig_x, target = self._layout()
        shape = QPainterPath()
        shape.addRoundedRect(QRectF(self.rect()), self._radius, self._radius)
        p.setClipPath(shape)

        g = QRadialGradient(QPointF(w * .45, h * .3), w * .75)
        g.setColorAt(0.0, GROUND_IN)
        g.setColorAt(0.55, GROUND_MID)
        g.setColorAt(1.0, GROUND_OUT)
        p.fillRect(QRectF(0, 0, w, h), g)

        akis = self._scroll * s
        self._paint_hills(p, w, ground, s, akis * .35)
        p.fillRect(QRectF(0, ground, w, h - ground), _alpha(GROUND_OUT, .45))
        p.setPen(QPen(INK, 2.2))
        p.drawLine(QPointF(0, ground), QPointF(w, ground))
        kalem = QPen(_alpha(INK, .5), 1.4)
        kalem.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(kalem)
        adim = 64.0
        x = -(akis % adim)
        while x < w:
            j = (int((x + akis) / adim) * 37) % 17
            p.drawLine(QPointF(x + j, ground + 9 + j % 7), QPointF(x + j + 15, ground + 9 + j % 7))
            x += adim
        # alt kenarda menderes, zeminle birlikte akıyor
        p.save()
        p.translate(-(akis % 24.0), 0)
        _meander(p, 4, h - 16, w + 48, 24.0, 9, _alpha(INK, .8))
        p.restore()

        self._paint_target(p, target, ground, s)
        if self._mode == "run":
            self._paint_wind(p, w, h)
            self._paint_dust(p, fig_x, ground, s, akis)

        pose = self._pose()
        p.save()
        p.translate(fig_x, ground - C.GROUND * s)
        p.scale(s, s)
        C.draw_centaur(p, pose, STYLE)
        p.restore()
        self._paint_arrow(p, pose, fig_x, ground, s, target)
        p.end()

    def _paint_hills(self, p: QPainter, w: float, ground: float, s: float, shift: float) -> None:
        path = QPainterPath()
        per = 520 * s
        x = -(shift % per) - per
        path.moveTo(x, ground)
        while x < w + per:
            path.cubicTo(x + per * .15, ground - 40 * s, x + per * .33, ground - 44 * s, x + per * .47, ground - 10 * s)
            path.cubicTo(x + per * .6, ground - 2 * s, x + per * .75, ground - 26 * s, x + per, ground)
            x += per
        path.lineTo(x, ground + 4)
        path.lineTo(-per * 2, ground + 4)
        path.closeSubpath()
        p.fillPath(path, _alpha(HILL, .5))

    def _paint_wind(self, p: QPainter, w: float, h: float) -> None:
        guc = self._speed
        for yk, faz, hiz, boy, acik in self._streaks:
            yol = w + boy + 60
            x = w + 30 - ((self._t * 900 * hiz + faz * yol) % yol)
            y = h * yk
            renk = SPARK if acik else INK
            a0, a1 = QPointF(x, y), QPointF(x + boy, y)
            grad = QLinearGradient(a0, a1)
            grad.setColorAt(0, _alpha(renk, .28 * guc))
            grad.setColorAt(1, _alpha(renk, 0))
            kalem = QPen(grad, 1.6)
            kalem.setCapStyle(Qt.PenCapStyle.RoundCap)
            p.setPen(kalem)
            p.drawLine(a0, a1)
        p.setPen(Qt.PenStyle.NoPen)

    def _paint_dust(self, p: QPainter, fig_x: float, ground: float, s: float, akis: float) -> None:
        p.setPen(Qt.PenStyle.NoPen)
        for i in range(6):
            k = ((self._t * 1.6 + i / 6) % 1.0)
            x = fig_x + 232 * s - k * 70 * s
            r = (3 + 12 * k) * s * 1.6
            p.setBrush(_alpha(INK, .22 * (1 - k) * self._speed))
            p.drawEllipse(QPointF(x, ground - 3 - 8 * k * s), r, r * .7)

    def _paint_target(self, p: QPainter, c: QPointF, ground: float, s: float) -> None:
        r = TARGET_R * s
        geri = 0.0
        hit = self._hit_time()
        if hit is not None:
            k = self._t - hit
            geri = 5 * math.exp(-k / .12) * math.cos(2 * math.pi * 7 * k)
        cx, cy = c.x() + geri, c.y()
        kalem = QPen(INK_FAR, 5 * s * 1.6)
        kalem.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(kalem)
        p.drawLine(QPointF(cx + 3, cy), QPointF(cx + 7, ground))
        kalem.setColor(INK)
        p.setPen(kalem)
        p.drawLine(QPointF(cx, cy), QPointF(cx - r * .8, ground))
        p.drawLine(QPointF(cx, cy), QPointF(cx + r * .72, ground))
        p.setPen(Qt.PenStyle.NoPen)
        for oran, renk in ((1.0, INK), (.82, RING_LIGHT), (.66, INK), (.48, RING_LIGHT), (.3, INK), (.14, RING_LIGHT)):
            p.setBrush(renk)
            p.drawEllipse(QPointF(cx, cy), r * oran, r * oran)
        p.setBrush(INK)
        p.drawEllipse(QPointF(cx, cy), max(1.5, r * .055), max(1.5, r * .055))
        p.setBrush(INCISE)
        for k in range(28):
            a = k * 2 * math.pi / 28
            p.drawEllipse(QPointF(cx + math.cos(a) * r * .91, cy + math.sin(a) * r * .91), 1.1, 1.1)
        if hit is not None:
            k = self._t - hit
            p.setBrush(Qt.BrushStyle.NoBrush)
            for gecikme in (0.0, .1):
                q = (k - gecikme) / .55
                if 0 <= q <= 1:
                    p.setPen(QPen(_alpha(SPARK, .8 * (1 - q)), 2.6 * (1 - q) + .6))
                    yaricap = r * .3 + r * 2.2 * _ease_out(q)
                    p.drawEllipse(QPointF(cx, cy), yaricap, yaricap)
            if k < .16:
                parlama = QRadialGradient(QPointF(cx, cy), r * 2.4)
                parlama.setColorAt(0, _alpha(SPARK, .5 * (1 - k / .16)))
                parlama.setColorAt(1, _alpha(SPARK, 0))
                p.fillRect(QRectF(cx - r * 2.5, cy - r * 2.5, r * 5, r * 5), parlama)

    def _hit_time(self) -> float | None:
        if self._shoot_at is None:
            return None
        at = self._shoot_at + DRAW_TIME + FLIGHT_TIME
        return at if self._t >= at else None

    def _paint_arrow(self, p: QPainter, pose: C.Pose, fig_x: float, ground: float, s: float, target: QPointF) -> None:
        """Bırakılan ok: kertikten hedefin merkezine; saplanınca titriyor."""
        if self._shoot_at is None or not pose.released:
            self._release = None
            return
        oy = ground - C.GROUND * s
        if self._release is None:
            nock, u = C.arrow_line(pose)
            bas = (fig_x + nock[0] * s + u[0] * C.ARROW_LENGTH * s, oy + nock[1] * s + u[1] * C.ARROW_LENGTH * s)
            self._release = bas
        bx, by = self._release
        k = (self._t - self._shoot_at - DRAW_TIME) / FLIGHT_TIME
        titreme = 0.0
        if k < 1:
            f = 0.6 * k + 0.4 * (1 - (1 - k) ** 2)
            x = bx + (target.x() - bx) * f
            y = by + (target.y() - by) * f - 10 * s * 4 * f * (1 - f)
            dy = (target.y() - by) - 10 * s * 4 * (1 - 2 * f)
            dx = target.x() - bx
        else:
            x, y = target.x(), target.y()
            dx, dy = target.x() - bx, target.y() - by
            r = self._t - (self._shoot_at + DRAW_TIME + FLIGHT_TIME)
            titreme = 6 * math.exp(-r / .2) * math.sin(2 * math.pi * 13 * r)
        a = math.atan2(dy, dx) + math.radians(titreme)
        u = (math.cos(a), math.sin(a))
        p.save()
        p.translate(x, y)
        p.scale(s, s)
        derin = 10.0 if k >= 1 else 0.0
        nock = (-u[0] * (C.ARROW_LENGTH - derin), -u[1] * (C.ARROW_LENGTH - derin))
        if k >= 1:
            kalem = QPen(INK, 3.0)
            kalem.setCapStyle(Qt.PenCapStyle.RoundCap)
            p.setPen(kalem)
            p.drawLine(QPointF(*nock), QPointF(-u[0] * 2, -u[1] * 2))
            p.setPen(Qt.PenStyle.NoPen)
            C.draw_fletching(p, nock, u, INK)
        else:
            C.draw_arrow(p, nock, u, C.ARROW_LENGTH, STYLE)
        p.restore()
