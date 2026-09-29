"""Açılış animasyonu: sentor koşarak gelir, oku atar, ok hedefi tam ortadan vurur.

**Ayrı bir süreçte oynuyor.** Ana pencere kurulurken arayüz iş parçacığı
saniyelerce kilitli kalıyor (ölçüldü, sıcak açılışta: modüller 0,3 sn,
pencere 1,3 sn, tarayıcı bileşeni 1,1 sn; soğuk açılışta her biri 15 sn'yi
geçti). Aynı süreçte oynayan bir animasyon tam o anlarda donardı — eski
açılış ekranının çubuğu bu yüzden aşamalarla ilerliyordu. Program kendini
`--intro` ile bir kez daha başlatıyor; bu süreç yalnızca çiziyor, ana süreç
de bu sırada pencereyi kuruyor (`app/core/intro_link.py`).

Haberleşme standart giriş/çıkıştan, satır satır:
  ana → intro:  `ready`   pencere hazır
  intro → ana:  `shown`   animasyon ekranda (gelmezse ana süreç beklemez)
                `reveal`  geçişin sonu: pencereyi göster
Ana süreç kapanırsa giriş kapanıyor (okuma boş dönüyor) ve animasyon da
kapanıyor; ekranda sahipsiz bir pencere kalmıyor.

Sahne 1280 × 720'lik sanal bir alanda çiziliyor, pencere boyuna ölçekleniyor.
Her kare zamanın saf bir fonksiyonu (`IntroScene.paint(t)`): kare atlansa da
akış bozulmuyor, bir anı tek başına çizip denetlemek mümkün.

Akış (saniye):
  0,00–1,25  sentor dörtnala giriyor, kamera onu izliyor; rüzgâr ve toz.
             0,6'dan itibaren yayı geriyor.
  1,25       ok bırakılıyor, kiriş titriyor, el geriye savruluyor.
  1,25–2,20  kamera oku izliyor; sütunlar ve ağaçlar hızla geçiyor.
  2,20       ok hedefi tam ortadan vuruyor: sarsıntı, halka dalgası, kıymık.
  2,38–2,90  kamera hedefi sola alıyor, ODYSSEY harf harf beliriyor.
  3,20–      pencere hazırsa kamera hedefin merkezine dalıyor, program açılıyor
             (uygulama ~3,6'da beliriyor).
Tıklamak ya da bir tuşa basmak animasyonu yazının geldiği ana atlatıyor.
"""

from __future__ import annotations

import json
import math
import os
import random
import sys
import threading
import time

from PySide6.QtCore import QObject, QPointF, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetricsF,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QRadialGradient,
)
from PySide6.QtWidgets import QApplication, QWidget

from ..resources.theme.tokens import FONTS, PALETTES
from ..widgets import centaur as C

# --- zaman çizelgesi (saniye) ------------------------------------------------------------
# Alican: çift tıklamadan uygulamaya en fazla 4,5–5 sn. İlk sürümde geçiş
# 4,35'te başlıyordu ve uygulama ~5,9 sn'de görünüyordu; sahneler aynı,
# zaman çizelgesi sıkıştırıldı (uygulama ~4,3 sn'de görünüyor).
T_DRAW0, T_DRAW1 = 0.6, 1.1
T_RELEASE = 1.25
T_HIT = 2.2
T_TITLE = 2.38
T_MIN_END = 3.2       # hazır olsa bile geçiş bundan önce başlamıyor
TRANSITION = 0.55
T_REVEAL_AT = 0.8     # geçişin bu oranında ana pencere belirmeye başlıyor
T_SKIP_TO = T_TITLE - 0.02

VIEW_W, VIEW_H = 1280.0, 720.0
GROUND_Y = 560.0
FIG_SCALE = 1.18
SPEED = 560.0         # sentorun dünyadaki hızı (px/sn)
GALLOP_PERIOD = 0.42  # bir dörtnal döngüsü (sn)
ENTER_FROM = -720.0   # figürün başlangıçtaki yeri (ekranın solunda)
SETTLE_X = 40.0       # kamera izlemeye başladığında figürün ekrandaki yeri
FLIGHT = 1850.0       # okun uçacağı yol (hızı ilk sürümle aynı kalsın diye kısa)
TARGET_R = 66.0       # hedefin yarıçapı (figür biriminde)

# --- renkler ----------------------------------------------------------------------------
# Siyah figür, mor zemin. Zemin uygulamanın vurgu morundan: ortası açık,
# kenarlar koyu. Figür saf siyah değil, mora çalan bir siyah; kazıma
# çizgileri zeminin açık tonu (vazoda kazıma altındaki kili gösterir).
GROUND_IN = QColor("#9C95FF")
GROUND_MID = QColor("#7466EE")
GROUND_OUT = QColor("#4A3AC4")
INK = QColor("#0E0B1A")
INK_FAR = QColor("#2A2150")
INCISE = QColor("#A9A2FF")
RING_LIGHT = QColor("#B5AFFF")
HILL = QColor("#5646CF")
# Süsler figürden bir ton geride: aynı siyahta olunca figürle birleşip leke oluyordu.
PROP = QColor("#2B2168")
SPARK = QColor("#E4E1FF")

STYLE = C.Style(fig=INK, far=INK_FAR, incise=INCISE, string=INK, arrow=INK, tip=INK)


def _ease_out_cubic(t: float) -> float:
    t = C.clamp01(t)
    return 1 - (1 - t) ** 3


def _ease_in_out_cubic(t: float) -> float:
    t = C.clamp01(t)
    return 4 * t * t * t if t < .5 else 1 - (-2 * t + 2) ** 3 / 2


def _ease_in_cubic(t: float) -> float:
    t = C.clamp01(t)
    return t * t * t


def _ease_out_back(t: float, s: float = 1.5) -> float:
    t = C.clamp01(t) - 1
    return 1 + (s + 1) * t * t * t + s * t * t


def _alpha(color: QColor, a: float) -> QColor:
    c = QColor(color)
    c.setAlphaF(max(0.0, min(1.0, c.alphaF() * a)))
    return c


class IntroScene:
    """Bütün sahne; `paint` verilen anı çiziyor."""

    def __init__(self, subtitle: str, version_line: str, preparing: str, final_bg: str) -> None:
        self.subtitle = subtitle
        self.version_line = version_line
        self.preparing = preparing
        self.final_bg = QColor(final_bg)
        self.transition_start: float | None = None

        # Okun bırakıldığı an figürün duruşu ve okun dünyadaki yeri: hedef
        # buna göre yerleşiyor, ok tam ortadan girsin.
        pose = self._pose(T_RELEASE - 1e-4)
        nock, u = C.arrow_line(pose)
        ox, oy = self._figure_origin(T_RELEASE)
        self.nock0 = (ox + nock[0] * FIG_SCALE, oy + nock[1] * FIG_SCALE)
        self.dir0 = u
        tip = C.ARROW_LENGTH * FIG_SCALE
        self.tip0 = (self.nock0[0] + u[0] * tip, self.nock0[1] + u[1] * tip)
        self.target = (self.tip0[0] + FLIGHT, self.tip0[1] + u[1] * FLIGHT * .02)

        # Kıymıklar ve rüzgâr çizgileri: sabit tohum, her açılış aynı.
        rnd = random.Random(7)
        self.chips = [(rnd.uniform(-2.6, -.4), rnd.uniform(-1.1, 1.1), rnd.uniform(3, 7)) for _ in range(9)]
        self.streaks = []
        s = .12
        while s < T_HIT + .1:
            flight = s > T_RELEASE
            self.streaks.append({
                "t": s,
                "y": rnd.uniform(-150, 150) if flight else rnd.uniform(120, 620),
                "x": rnd.uniform(0, 260),
                "speed": rnd.uniform(3000, 4200) if flight else rnd.uniform(2100, 3000),
                "len": rnd.uniform(110, 280),
                "w": rnd.uniform(1.2, 2.6),
                "light": rnd.random() < .32,
                "a": rnd.uniform(.16, .38),
            })
            s += .018 if flight else .026
        self.puffs = [(k * .065 + .2, rnd.uniform(-10, 14), rnd.uniform(.8, 1.3)) for k in range(26)]

        # Sahne süsleri: sütunlar, zeytin ve servi ağaçları. Hedefin
        # çevresi boş kalıyor, göz oraya gitsin.
        self.props = []
        x, kinds = 820.0, ("olive", "column", "cypress", "column", "olive", "broken")
        k = 0
        while x < self.target[0] + 900:
            # hedefin solu biraz, sağı (yazının yeri) tamamen boş
            if not self.target[0] - 420 < x < self.target[0] + 1100:
                self.props.append((kinds[k % len(kinds)], x, rnd.uniform(.9, 1.08)))
                k += 1
            x += rnd.uniform(430, 560)

        self._title_font = QFont(FONTS["display"].split(",")[0].strip().strip('"'))
        self._title_font.setPixelSize(98)
        self._title_font.setWeight(QFont.Weight.DemiBold)
        self._text_font = QFont(FONTS["ui"].split(",")[0].strip().strip('"'))
        self._text_font.setPixelSize(23)
        self._small_font = QFont(self._text_font)
        self._small_font.setPixelSize(15)
        # Değişmeyen katmanlar bir kez resme çiziliyor: zemin geçişi ve
        # menderes şeridi her karede baştan çizilince kare başına 8 ms
        # tutuyordu (ölçüldü; bütün kare 14 ms).
        self._cache: dict = {}

    # --- figür ----------------------------------------------------------------------------

    @staticmethod
    def _figure_x(t: float) -> float:
        return ENTER_FROM + SPEED * t

    @staticmethod
    def _screen_x(t: float) -> float:
        # Figür soldan hızla girip yerine oturuyor; oturdukça kamera onu
        # izlemeye başlıyor (zemin çizgileri ve süsler akmaya başlıyor).
        return ENTER_FROM + (SETTLE_X - ENTER_FROM) * _ease_out_cubic(t / 1.0)

    def _figure_origin(self, t: float):
        return self._figure_x(t), GROUND_Y - C.GROUND * FIG_SCALE

    def _pose(self, t: float) -> C.Pose:
        pose = C.gallop_pose(t / GALLOP_PERIOD)
        if t < T_RELEASE:
            pose.draw = .62 + .38 * _ease_in_out_cubic((t - T_DRAW0) / (T_DRAW1 - T_DRAW0))
        else:
            k = t - T_RELEASE
            pose.released = True
            pose.vib = 9 * math.exp(-k / .09) * math.cos(2 * math.pi * 26 * k)
            pose.follow = _ease_out_cubic(k / .22)
        return pose

    # --- kamera ---------------------------------------------------------------------------

    def _arrow(self, t: float):
        """Okun ucu ve yönü (dünyada)."""
        u = C.clamp01((t - T_RELEASE) / (T_HIT - T_RELEASE))
        # Hızlı çıkıp hafifçe yavaşlıyor; hedefe yine hızlı giriyor.
        f = .55 * u + .45 * (1 - (1 - u) ** 2)
        x = self.tip0[0] + (self.target[0] - self.tip0[0]) * f
        base_y = self.tip0[1] + (self.target[1] - self.tip0[1]) * f
        arc = 34.0
        y = base_y - arc * 4 * f * (1 - f)
        dy = (self.target[1] - self.tip0[1]) - arc * 4 * (1 - 2 * f)
        dx = self.target[0] - self.tip0[0]
        n = math.hypot(dx, dy)
        return (x, y), (dx / n, dy / n)

    def _camera(self, t: float):
        """Dünyada ekranın ortasına düşen nokta ve yakınlaştırma."""
        track = 640 + self._figure_x(t) - self._screen_x(t)
        cx, cy, zoom = track, 360.0, 1.0
        if t > T_RELEASE:
            (ax, _ay), _u = self._arrow(t)
            w = C.smoothstep((t - T_RELEASE) / .24)
            cx = C.lerp(track, ax + 180, w)
        if t > T_HIT:
            hit_cx = self.target[0] + 180
            k = _ease_in_out_cubic((t - T_TITLE) / .5)
            # Hedef sola, bullseye yazının hizasına.
            cx = C.lerp(hit_cx, self.target[0] + 240, k)
            cy = C.lerp(360.0, self.target[1] + 30, k)
        if self.transition_start is not None and t > self.transition_start:
            k = (t - self.transition_start) / TRANSITION
            e = _ease_in_out_cubic(k / .55)
            cx = C.lerp(cx, self.target[0], e)
            cy = C.lerp(cy, self.target[1], e)
            zoom = math.exp(math.log(16.0) * _ease_in_cubic(k))
        return cx, cy, zoom

    # --- çizim ----------------------------------------------------------------------------

    def paint(self, p: QPainter, t: float, width: float, height: float, ready: bool) -> None:
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        s = width / VIEW_W
        dpr = p.device().devicePixelRatioF() if p.device() else 1.0
        p.drawPixmap(QPointF(0, 0), self._layer("ground", width, VIEW_H * s, dpr, s, self._draw_ground))
        p.save()
        p.scale(s, s)  # pencere 16:9, sahne de

        cx, cy, zoom = self._camera(t)
        shake = (0.0, 0.0)
        if T_HIT < t < T_HIT + .4:
            k = t - T_HIT
            amp = 7 * math.exp(-k / .1)
            shake = (amp * math.sin(2 * math.pi * 31 * k), amp * .6 * math.cos(2 * math.pi * 23 * k))

        def to_screen(layer: float = 1.0):
            p.translate(640 + shake[0], 360 + shake[1])
            p.scale(zoom, zoom)
            p.translate(-cx * layer, -cy)

        # uzak tepeler (yavaş akıyor)
        p.save()
        to_screen(.35)
        self._paint_hills(p, cx * .35)
        p.restore()

        p.save()
        to_screen()
        self._paint_floor(p, cx, zoom)
        for kind, x, sc in self.props:
            if abs(x - cx) < 640 / zoom + 400:
                self._paint_prop(p, kind, x, sc)
        self._paint_target(p, t)
        self._paint_dust(p, t)
        self._paint_figure(p, t)
        self._paint_flying_arrow(p, t)
        self._paint_impact(p, t)
        p.restore()

        self._paint_bands(p, t, cx, zoom, s, dpr)
        self._paint_wind(p, t)
        self._paint_title(p, t, ready)

        if self.transition_start is not None and t > self.transition_start:
            # Hedefin siyah merkezi büyüyüp ekranı kaplıyor; rengi uygulamanın
            # zemini (koyu temada neredeyse aynı siyah), pencere onun altından
            # beliriyor.
            k = (t - self.transition_start) / TRANSITION
            sx = 640 + (self.target[0] - cx) * zoom
            sy = 360 + (self.target[1] - cy) * zoom
            base_r = 3.6 * FIG_SCALE * zoom  # merkezdeki nokta
            r = base_r + 900 * _ease_in_cubic((k - .28) / .6)
            iris = QPainterPath()
            iris.addEllipse(QPointF(sx, sy), r, r)
            p.fillPath(iris, self.final_bg)
        p.restore()

    def _layer(self, key: str, width: float, height: float, dpr: float, s: float, draw) -> QPixmap:
        """Sanal koordinatta çizilen sabit bir katmanın önbellekteki resmi."""
        ident = (key, round(width), round(height), dpr)
        pix = self._cache.get(ident)
        if pix is None:
            pix = QPixmap(max(1, round(width * dpr)), max(1, round(height * dpr)))
            pix.setDevicePixelRatio(dpr)
            pix.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pix)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.scale(s, s)
            draw(painter)
            painter.end()
            self._cache[ident] = pix
        return pix

    def _draw_ground(self, p: QPainter) -> None:
        g = QRadialGradient(QPointF(640, 300), 900)
        g.setColorAt(0.0, GROUND_IN)
        g.setColorAt(0.55, GROUND_MID)
        g.setColorAt(1.0, GROUND_OUT)
        p.fillRect(QRectF(0, 0, VIEW_W, VIEW_H), g)

    def _paint_hills(self, p: QPainter, x0: float) -> None:
        # Alçak, yumuşak tepeler: hız hissi için arkada yavaş akan bir katman.
        path = QPainterPath()
        start = x0 - 1400
        path.moveTo(start, GROUND_Y)
        x = start
        while x < x0 + 1400:
            path.cubicTo(x + 110, GROUND_Y - 58, x + 250, GROUND_Y - 64, x + 360, GROUND_Y - 14)
            path.cubicTo(x + 420, GROUND_Y - 4, x + 480, GROUND_Y - 36, x + 560, GROUND_Y - 30)
            path.cubicTo(x + 640, GROUND_Y - 24, x + 700, GROUND_Y - 6, x + 760, GROUND_Y)
            x += 760
        path.lineTo(x, GROUND_Y + 200)
        path.lineTo(start, GROUND_Y + 200)
        path.closeSubpath()
        p.fillPath(path, _alpha(HILL, .55))

    def _paint_floor(self, p: QPainter, cx: float, zoom: float) -> None:
        half = 640 / zoom + 60
        # zemin çizgisi ve altındaki koyu şerit
        p.fillRect(QRectF(cx - half, GROUND_Y, 2 * half, 180), _alpha(GROUND_OUT, .45))
        pen = QPen(INK, 2.6)
        p.setPen(pen)
        p.drawLine(QPointF(cx - half, GROUND_Y), QPointF(cx + half, GROUND_Y))
        # Zemindeki kısa kazıma çizgileri: kamera akınca hız bunlardan okunuyor.
        pen = QPen(_alpha(INK, .5), 1.6)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        step = 74.0
        x = math.floor((cx - half) / step) * step
        while x < cx + half:
            j = (int(x / step) * 37) % 23
            p.drawLine(QPointF(x + j, GROUND_Y + 12 + j % 9), QPointF(x + j + 18, GROUND_Y + 12 + j % 9))
            x += step
        p.setPen(Qt.PenStyle.NoPen)

    def _paint_prop(self, p: QPainter, kind: str, x: float, sc: float) -> None:
        p.save()
        p.translate(x, GROUND_Y)
        p.scale(sc * FIG_SCALE, sc * FIG_SCALE)
        p.setPen(Qt.PenStyle.NoPen)
        ink = PROP
        inc = QPen(_alpha(INCISE, .7), 1.3)
        inc.setCapStyle(Qt.PenCapStyle.RoundCap)
        if kind in ("column", "broken"):
            h = 196.0 if kind == "column" else 118.0
            path = QPainterPath()
            path.addRect(QRectF(-26, -8, 52, 8))           # basamak
            path.addRect(QRectF(-21, -14, 42, 6))
            p.fillPath(path, ink)
            shaft = QPainterPath()
            shaft.moveTo(-15, -14)
            shaft.lineTo(-12.5, -14 - h)
            shaft.lineTo(12.5, -14 - h)
            shaft.lineTo(15, -14)
            shaft.closeSubpath()
            p.fillPath(shaft, ink)
            if kind == "column":
                cap = QPainterPath()
                cap.moveTo(-13, -14 - h)
                cap.cubicTo(-22, -18 - h, -20, -26 - h, -18, -27 - h)
                cap.lineTo(18, -27 - h)
                cap.cubicTo(20, -26 - h, 22, -18 - h, 13, -14 - h)
                cap.closeSubpath()
                cap.addRect(QRectF(-21, -34 - h, 42, 7))
                p.fillPath(cap, ink)
            else:
                # kırık sütun: eğri kopuk üst
                broken = QPainterPath()
                broken.moveTo(-12.5, -14 - h)
                broken.lineTo(-4, -22 - h)
                broken.lineTo(3, -12 - h)
                broken.lineTo(12.5, -19 - h)
                broken.lineTo(12.5, -14 - h)
                broken.closeSubpath()
                p.fillPath(broken, ink)
            p.setPen(inc)
            for fx in (-6.5, 0.0, 6.5):
                p.drawLine(QPointF(fx, -20), QPointF(fx * .9, -8 - h))
        elif kind == "olive":
            trunk = QPainterPath()
            trunk.moveTo(-9, 0)
            trunk.cubicTo(-6, -30, -16, -52, -4, -84)
            trunk.lineTo(5, -84)
            trunk.cubicTo(-2, -56, 8, -32, 9, 0)
            trunk.closeSubpath()
            p.fillPath(trunk, ink)
            for ex, ey, rx, ry in ((-30, -104, 36, 22), (18, -112, 40, 24), (-8, -136, 42, 24),
                                   (34, -90, 26, 16), (-44, -84, 22, 14)):
                blob = QPainterPath()
                blob.addEllipse(QPointF(ex, ey), rx, ry)
                p.fillPath(blob, ink)
            p.setPen(inc)
            for ex, ey in ((-30, -104), (18, -112), (-8, -136)):
                p.drawLine(QPointF(ex - 14, ey + 3), QPointF(ex + 10, ey - 5))
        else:  # servi
            tree = QPainterPath()
            tree.moveTo(0, -226)
            tree.cubicTo(18, -170, 22, -80, 12, -14)
            tree.lineTo(-12, -14)
            tree.cubicTo(-22, -80, -18, -170, 0, -226)
            tree.closeSubpath()
            tree.addRect(QRectF(-4, -16, 8, 16))
            p.fillPath(tree, ink)
            p.setPen(inc)
            p.drawLine(QPointF(0, -196), QPointF(0, -40))
        p.restore()

    def _paint_target(self, p: QPainter, t: float) -> None:
        x, y = self.target
        recoil = 0.0
        if t > T_HIT:
            k = t - T_HIT
            recoil = 7 * math.exp(-k / .12) * math.cos(2 * math.pi * 7 * k)
        s = FIG_SCALE
        p.save()
        p.translate(x + recoil, y)
        # Üç ayaklı sehpa
        pen = QPen(INK_FAR, 7 * s)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        p.drawLine(QPointF(4 * s, 0), QPointF(10 * s, GROUND_Y - y))
        pen.setColor(INK)
        p.setPen(pen)
        p.drawLine(QPointF(0, 0), QPointF(-54 * s, GROUND_Y - y))
        p.drawLine(QPointF(0, 0), QPointF(48 * s, GROUND_Y - y))
        p.setPen(Qt.PenStyle.NoPen)
        # Halkalar: dıştan içe siyah / açık mor.
        rings = ((1.0, INK), (.82, RING_LIGHT), (.66, INK), (.48, RING_LIGHT), (.3, INK), (.14, RING_LIGHT))
        for r, color in rings:
            p.setBrush(color)
            p.drawEllipse(QPointF(0, 0), TARGET_R * s * r, TARGET_R * s * r)
        p.setBrush(INK)
        p.drawEllipse(QPointF(0, 0), 3.6 * s, 3.6 * s)
        # Dış halkada kazınmış noktalar ve iç çizgiler
        p.setBrush(INCISE)
        for k in range(36):
            a = k * 10 * C.R
            p.drawEllipse(QPointF(math.cos(a) * TARGET_R * s * .91, math.sin(a) * TARGET_R * s * .91), 1.5 * s, 1.5 * s)
        pen = QPen(INCISE, 1.3)
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        for r in (.58, .38):
            p.drawEllipse(QPointF(0, 0), TARGET_R * s * r, TARGET_R * s * r)
        p.restore()

    def _paint_dust(self, p: QPainter, t: float) -> None:
        # Arka toynakların kaldırdığı toz: dünyada kalıyor, figür uzaklaşıyor.
        for start, dx, size in self.puffs:
            k = (t - start) / .55
            if not 0 <= k <= 1:
                continue
            fx, _fy = self._figure_origin(start)
            x = fx + 232 * FIG_SCALE + dx - 40 * k
            r = (5 + 18 * _ease_out_cubic(k)) * size
            puff = QPainterPath()
            puff.addEllipse(QPointF(x, GROUND_Y - 4 - 12 * k), r, r * .72)
            p.fillPath(puff, _alpha(INK, .28 * (1 - k)))

    def _paint_figure(self, p: QPainter, t: float) -> None:
        ox, oy = self._figure_origin(t)
        p.save()
        p.translate(ox, oy)
        p.scale(FIG_SCALE, FIG_SCALE)
        C.draw_centaur(p, self._pose(t), STYLE)
        p.restore()

    def _paint_flying_arrow(self, p: QPainter, t: float) -> None:
        if t < T_RELEASE:
            return
        length = C.ARROW_LENGTH * FIG_SCALE
        if t < T_HIT:
            (x, y), u = self._arrow(t)
            # Okun arkasında hız izleri
            for k, (off, ln, a) in enumerate(((0, 230, .5), (-7, 150, .32), (7, 170, .28))):
                n = (-u[1], u[0])
                tail = (x - u[0] * (length + 6), y - u[1] * (length + 6))
                a0 = QPointF(tail[0] + n[0] * off, tail[1] + n[1] * off)
                a1 = QPointF(a0.x() - u[0] * ln, a0.y() - u[1] * ln)
                grad = QLinearGradient(a0, a1)
                grad.setColorAt(0, _alpha(SPARK if k else INK, a))
                grad.setColorAt(1, _alpha(SPARK if k else INK, 0))
                pen = QPen(grad, 2.2 if k == 0 else 1.4)
                pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                p.setPen(pen)
                p.drawLine(a0, a1)
            p.setPen(Qt.PenStyle.NoPen)
            p.save()
            p.translate(x, y)
            p.scale(FIG_SCALE * 1.25, FIG_SCALE * 1.25)  # uçarken okunsun diye biraz büyük
            nock = (-u[0] * C.ARROW_LENGTH, -u[1] * C.ARROW_LENGTH)
            C.draw_arrow(p, nock, u, C.ARROW_LENGTH, STYLE)
            p.restore()
            return
        # Saplandı: uç hedefin içinde, gövde titriyor.
        k = t - T_HIT
        q = 6 * math.exp(-k / .2) * math.sin(2 * math.pi * 13 * k)
        _, u = self._arrow(T_HIT)
        a = math.atan2(u[1], u[0]) + q * C.R
        u = (math.cos(a), math.sin(a))
        x, y = self.target
        recoil = 7 * math.exp(-k / .12) * math.cos(2 * math.pi * 7 * k)
        p.save()
        p.translate(x + recoil, y)
        p.scale(FIG_SCALE, FIG_SCALE)
        depth = 12.0  # ucun gömülen kısmı
        nock = (-u[0] * (C.ARROW_LENGTH - depth), -u[1] * (C.ARROW_LENGTH - depth))
        pen = QPen(INK, 3.0)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        p.drawLine(QPointF(*nock), QPointF(-u[0] * 2, -u[1] * 2))
        p.setPen(Qt.PenStyle.NoPen)
        C.draw_fletching(p, nock, u, INK)
        p.restore()

    def _paint_impact(self, p: QPainter, t: float) -> None:
        if t < T_HIT or t > T_HIT + .9:
            return
        k0 = t - T_HIT
        x, y = self.target
        # parlama
        if k0 < .18:
            g = QRadialGradient(QPointF(x, y), 150)
            g.setColorAt(0, _alpha(SPARK, .55 * (1 - k0 / .18)))
            g.setColorAt(1, _alpha(SPARK, 0))
            p.fillRect(QRectF(x - 160, y - 160, 320, 320), g)
        # halka dalgaları
        p.setBrush(Qt.BrushStyle.NoBrush)
        for delay in (0.0, .09, .18):
            k = (k0 - delay) / .55
            if 0 <= k <= 1:
                r = 14 + 170 * _ease_out_cubic(k)
                p.setPen(QPen(_alpha(SPARK, .8 * (1 - k)), 3.2 * (1 - k) + .8))
                p.drawEllipse(QPointF(x, y), r, r)
        # kıymıklar
        p.setPen(Qt.PenStyle.NoPen)
        k = k0 / .7
        if k <= 1:
            for vx, vy, size in self.chips:
                px = x + vx * 150 * k
                py = y + vy * 150 * k + 240 * k * k
                chip = QPainterPath()
                chip.moveTo(px, py - size)
                chip.lineTo(px + size * .8, py + size * .5)
                chip.lineTo(px - size * .7, py + size * .6)
                chip.closeSubpath()
                p.fillPath(chip, _alpha(INK, 1 - k))

    BAND_UNIT = 30.0

    def _draw_band(self, p: QPainter) -> None:
        """Bir menderes şeridi: üst ve alt çizgi, arada kesintisiz desen."""
        pen = QPen(INK, 2.6)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        p.setPen(pen)
        top, unit = 8.0, self.BAND_UNIT
        path = QPainterPath()
        x = 0.0
        while x < VIEW_W + 2 * unit:
            path.moveTo(x, top + 14)
            path.lineTo(x, top)
            path.lineTo(x + 22.5, top)
            path.lineTo(x + 22.5, top + 10.7)
            path.lineTo(x + 7.5, top + 10.7)
            path.lineTo(x + 7.5, top + 4.3)
            x += unit
        p.drawPath(path)
        p.drawLine(QPointF(0, top - 6), QPointF(VIEW_W + 2 * unit, top - 6))
        p.drawLine(QPointF(0, top + 20), QPointF(VIEW_W + 2 * unit, top + 20))

    def _paint_bands(self, p: QPainter, t: float, cx: float, zoom: float, s: float, dpr: float) -> None:
        """Üstte ve altta menderes bordür; kamerayla birlikte akıyor."""
        reveal = _ease_out_cubic((t - .05) / .6)
        if reveal <= 0:
            return
        fade = 1.0
        if self.transition_start is not None and t > self.transition_start:
            fade = 1 - C.clamp01((t - self.transition_start) / (TRANSITION * .4))
        if fade <= 0:
            return
        half = 640 * reveal
        unit = self.BAND_UNIT
        strip = self._layer("band", (VIEW_W + 2 * unit) * s, 32 * s, dpr, s, self._draw_band)
        shift = -((cx * zoom) % unit) - unit
        p.save()
        p.setClipRect(QRectF(640 - half, 0, 2 * half, VIEW_H))
        p.setOpacity(.88 * fade)
        p.scale(1 / s, 1 / s)
        for top in (30.0, VIEW_H - 50):
            p.drawPixmap(QPointF(shift * s, (top - 8) * s), strip)
        p.restore()

    def _paint_wind(self, p: QPainter, t: float) -> None:
        if t > T_HIT + .35:
            return
        envelope = C.smoothstep((t - .12) / .3)
        if t > T_HIT:
            envelope *= 1 - C.clamp01((t - T_HIT) / .3)
        flight_y = 360.0
        if t > T_RELEASE:
            (ax, ay), _u = self._arrow(min(t, T_HIT))
            cx, cy, zoom = self._camera(t)
            flight_y = 360 + (ay - cy) * zoom
        for st in self.streaks:
            k = t - st["t"]
            if not 0 <= k <= .34:
                continue
            x = VIEW_W + st["x"] - st["speed"] * k
            y = flight_y + st["y"] if st["t"] > T_RELEASE else st["y"]
            a = st["a"] * envelope * math.sin(math.pi * k / .34)
            color = SPARK if st["light"] else INK
            p0, p1 = QPointF(x, y), QPointF(x + st["len"], y)
            grad = QLinearGradient(p0, p1)
            grad.setColorAt(0, _alpha(color, a))
            grad.setColorAt(1, _alpha(color, 0))
            pen = QPen(grad, st["w"])
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            p.setPen(pen)
            p.drawLine(p0, p1)
        p.setPen(Qt.PenStyle.NoPen)

    def _paint_title(self, p: QPainter, t: float, ready: bool) -> None:
        out = 1.0
        if self.transition_start is not None and t > self.transition_start:
            out = 1 - C.clamp01((t - self.transition_start) / (TRANSITION * .3))

        # sürüm satırı: baştan beri sağ altta
        p.setFont(self._small_font)
        p.setPen(_alpha(INK, .62 * out * C.clamp01(t / .5)))
        p.drawText(QRectF(0, VIEW_H - 22, VIEW_W - 40, 18),
                   Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, self.version_line)
        if t < T_TITLE or out <= 0:
            return

        x0, base = 580.0, 376.0
        fm = QFontMetricsF(self._title_font)
        tracking = 18.0
        p.setFont(self._title_font)
        x = x0
        for i, ch in enumerate("ODYSSEY"):
            k = (t - T_TITLE - .05 * i) / .42
            if k > 0:
                a = C.clamp01(k * 1.6) * out
                dy = 30 * (1 - _ease_out_back(k, 1.2))
                p.setPen(_alpha(INK, a))
                p.drawText(QPointF(x, base + dy), ch)
            x += fm.horizontalAdvance(ch) + tracking
        width = x - tracking - x0

        # yazının altında menderes, soldan sağa açılıyor
        reveal = _ease_out_cubic((t - T_TITLE - .3) / .5)
        if reveal > 0:
            p.save()
            p.setClipRect(QRectF(x0 - 2, 0, width * reveal + 4, VIEW_H))
            pen = QPen(_alpha(INK, .9 * out), 2.2)
            pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
            p.setPen(pen)
            top, unit = base + 24, 26.0
            path = QPainterPath()
            xx = x0
            while xx < x0 + width - unit * .5:
                path.moveTo(xx, top + 11)
                path.lineTo(xx, top)
                path.lineTo(xx + 18, top)
                path.lineTo(xx + 18, top + 8.6)
                path.lineTo(xx + 6, top + 8.6)
                path.lineTo(xx + 6, top + 3.4)
                xx += unit
            p.drawPath(path)
            p.restore()

        k = C.clamp01((t - T_TITLE - .42) / .4)
        if k > 0:
            p.setFont(self._text_font)
            p.setPen(_alpha(INK, .8 * _ease_out_cubic(k) * out))
            p.drawText(QPointF(x0 + 2, base + 78 + 8 * (1 - _ease_out_cubic(k))), self.subtitle)

        # Pencere hâlâ hazır değilse (soğuk açılış) sessiz bir bekleme yazısı.
        if not ready and t > T_MIN_END:
            k = C.clamp01((t - T_MIN_END) / .4)
            dots = "." * (1 + int((t * 2.5) % 3))
            p.setFont(self._small_font)
            p.setPen(_alpha(INK, .6 * k * out))
            p.drawText(QPointF(x0 + 2, base + 118), self.preparing.rstrip(".…") + dots)


class _StdinReader(QObject):
    """Ana süreçten gelen satırları arayüz iş parçacığına taşır."""

    line = Signal(str)
    closed = Signal()

    def start(self) -> None:
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self) -> None:
        buffer = b""
        while True:
            try:
                chunk = os.read(0, 256)
            except OSError:
                chunk = b""
            if not chunk:
                self.closed.emit()
                return
            buffer += chunk
            while b"\n" in buffer:
                raw, buffer = buffer.split(b"\n", 1)
                self.line.emit(raw.decode("utf-8", "replace").strip())


def _send(message: str) -> None:
    try:
        os.write(1, (message + "\n").encode())
    except OSError:
        pass


class IntroWindow(QWidget):
    """Animasyonun oynadığı çerçevesiz pencere."""

    def __init__(self, scene: IntroScene, parent_pid: int, sound: bool = False) -> None:
        super().__init__(None)
        self._scene = scene
        self._parent_pid = parent_pid
        self._sound = sound
        self._ready = False
        self._offset = 0.0
        self._revealed = False
        self._closing = False
        self._began = time.monotonic()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.SplashScreen
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        screen = QApplication.primaryScreen()
        area = screen.availableGeometry() if screen else None
        width = 1100
        if area is not None:
            width = int(max(860, min(1180, area.width() * .66)))
        self.setFixedSize(width, int(width * VIEW_H / VIEW_W))
        if area is not None:
            self.move(area.center().x() - self.width() // 2, area.center().y() - self.height() // 2)

        self._timer = QTimer(self)
        self._timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._timer.setInterval(15)
        self._timer.timeout.connect(self._tick)

        self._reader = _StdinReader()
        self._reader.line.connect(self._on_line)
        self._reader.closed.connect(self._on_parent_gone)

    def start(self) -> None:
        self.setWindowOpacity(0.0)
        self.show()
        self._round_corners()
        self._allow_parent_foreground()
        self._began = time.monotonic()
        self._play("intro")
        self._timer.start()
        self._reader.start()
        _send("shown")

    def now(self) -> float:
        return time.monotonic() - self._began + self._offset

    def _tick(self) -> None:
        t = self.now()
        # açılış: pencere 0,25 sn'de belirginleşiyor
        if not self._closing:
            self.setWindowOpacity(_ease_out_cubic(t / .25))
        scene = self._scene
        if self._ready and scene.transition_start is None and t >= T_MIN_END:
            self._begin_transition(t)
        if scene.transition_start is not None:
            k = (t - scene.transition_start) / TRANSITION
            if k >= T_REVEAL_AT and not self._revealed:
                self._revealed = True
                _send("reveal")
            if k >= 1 and not self._closing:
                self._closing = True
                self._fade_out()
        # Ana süreç 2 dakikada hazır olmadıysa takılmış demektir; beklemeyi bırak.
        if t > 120 and not self._ready:
            QApplication.quit()
        self.update()

    def _fade_out(self) -> None:
        start = time.monotonic()

        def step() -> None:
            k = (time.monotonic() - start) / .2
            self.setWindowOpacity(max(0.0, 1 - k))
            if k >= 1:
                QApplication.quit()
            else:
                QTimer.singleShot(12, step)

        QTimer.singleShot(60, step)

    def _on_line(self, line: str) -> None:
        if line == "ready":
            self._ready = True

    def _on_parent_gone(self) -> None:
        # Ana süreç kapandı ya da çöktü: animasyonun ekranda kalmasının anlamı yok.
        QApplication.quit()

    def _skip(self) -> None:
        t = self.now()
        if t < T_SKIP_TO:
            self._offset += T_SKIP_TO - t
            # Sahne yazıya sıçradı; koşunun ve okun sesi susmalı.
            self._play(None)
        elif self._ready and self._scene.transition_start is None:
            self._begin_transition(t)

    def _begin_transition(self, t: float) -> None:
        self._scene.transition_start = t

    def _play(self, name: str | None) -> None:
        """Sahnenin sesi (`tools/make_intro_sounds.py`); `None` susturur.

        Tek kayıt: nallar, okun rüzgârı ve hedefe saplanma. `winsound` aynı
        anda tek ses çalıyor. Ayar kutlama sesiyle ortak (Ayarlar ›
        Bildirimler › Sesler).
        """
        if not self._sound or sys.platform != "win32":
            return
        try:
            import winsound

            if name is None:
                winsound.PlaySound(None, winsound.SND_PURGE)
                return
            from ..paths import install_root

            path = install_root() / "app" / "resources" / "sounds" / f"{name}.wav"
            if path.exists():
                winsound.PlaySound(str(path), winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
        except (RuntimeError, OSError):
            pass

    def mousePressEvent(self, event) -> None:  # noqa: N802 (Qt adlandırması)
        if event.button() == Qt.MouseButton.LeftButton:
            self._skip()

    def keyPressEvent(self, event) -> None:  # noqa: N802
        if event.key() in (Qt.Key.Key_Escape, Qt.Key.Key_Space, Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._skip()

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        self._scene.paint(painter, self.now(), self.width(), self.height(), self._ready)
        painter.end()

    def _round_corners(self) -> None:
        """Windows 11'de köşeleri yuvarlatır (DWM); eski sürümde köşe düz kalır."""
        if sys.platform != "win32":
            return
        try:
            import ctypes
            from ctypes import wintypes

            dwm = ctypes.windll.dwmapi
            dwm.DwmSetWindowAttribute.argtypes = [wintypes.HWND, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD]
            dwm.DwmSetWindowAttribute.restype = ctypes.c_long
            preference = ctypes.c_int(2)  # DWMWCP_ROUND
            dwm.DwmSetWindowAttribute(wintypes.HWND(int(self.winId())), 33,
                                      ctypes.byref(preference), ctypes.sizeof(preference))
        except (OSError, AttributeError):
            pass

    def _allow_parent_foreground(self) -> None:
        """Ana sürecin, animasyon bitince kendi penceresini öne alabilmesi için.

        Kullanıcı animasyona tıklarsa ön plan bu sürece geçiyor; Windows başka
        bir sürecin pencereyi öne almasını ancak izinle kabul ediyor.
        """
        if sys.platform != "win32" or not self._parent_pid:
            return
        try:
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.windll.user32
            user32.AllowSetForegroundWindow.argtypes = [wintypes.DWORD]
            user32.AllowSetForegroundWindow.restype = wintypes.BOOL
            user32.AllowSetForegroundWindow(self._parent_pid)
        except (OSError, AttributeError):
            pass


def build_scene(settings: dict) -> IntroScene:
    """Ayarlardan sahneyi kurar (dil, tema, sürüm)."""
    from ..core.language import LanguageManager, system_language
    from ..core.theme import resolve_mode
    from ..version import APP_VERSION

    language = LanguageManager(settings.get("lang") or system_language())
    mode = resolve_mode(settings.get("theme") or "dark")
    palette = PALETTES.get(mode, PALETTES["dark"])
    return IntroScene(
        subtitle=language.t("app.subtitle"),
        version_line=f"v{APP_VERSION} · {language.t('splash.beta')}",
        preparing=language.t("intro.preparing"),
        final_bg=palette["bg"],
    )


def run(payload: str) -> int:
    """`--intro` ile başlatılan sürecin girişi."""
    try:
        settings = json.loads(payload)
    except ValueError:
        settings = {}
    app = QApplication.instance() or QApplication(sys.argv[:1])
    window = IntroWindow(build_scene(settings), int(settings.get("pid") or 0), bool(settings.get("sound")))
    window.start()
    return app.exec()
