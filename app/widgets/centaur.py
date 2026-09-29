"""Uygulamanın maskotu: yay tutan sentor, eklemli çizim.

Figür resim değil, bir iskelet: dört bacak (her biri beş parçalık zincir),
kuyruk ve belden yukarısı ayrı ayrı dönüyor. Açılış animasyonu dörtnal
döngüsünü, yayı germeyi ve oku bırakmayı buradan hesaplıyor; aynı figür
ileride logo ve çıkış penceresinde de kullanılacak.

Üslup Antik Yunan "siyah figür" vazo resmi: düz siyah figür, kas ve kıl
çizgileri zemine **kazınmış** gibi zemin renginde. Zemin terrakota değil,
uygulamanın moru (Alican istedi).

Koordinatlar figürün kendi biriminde (zemin çizgisi `GROUND` = 446, figür
kabaca 150–520 arası); çizen taraf ölçeği ve konumu kendisi veriyor.

Açı kuralı: 0 = kemik dümdüz aşağı, + = ileri (sağa); dizideki açılar bir
önceki parçaya göre. QPainter'ın `rotate` yönü (saat yönü) bunun tersi,
çizerken işaret çevriliyor.

Oranlar baş boyuna göre (tepe → çene ≈ 38 birim): tepe → bel 3,25 baş,
omuz genişliği ~2,5 baş, yay kolu omuzdan yumruğa ~2,4 baş. İlk sürümde
boyun uzun, omuzlar dar, kollar kısaydı ve baş gövdeye oturmuyordu.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field, replace
from functools import lru_cache

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen

R = math.pi / 180
GROUND = 446.0
UPPER = 0.84  # belden yukarısının ölçeği (insan gövdesi / at yüksekliği)


# --- SVG yol metni -------------------------------------------------------------------
# Çizimler tasarım dosyasından geliyor; yalnızca mutlak M, L, C ve Z kullanıyor.

_TOKEN = re.compile(r"[MLCZ]|-?\d*\.?\d+(?:e-?\d+)?")


@lru_cache(maxsize=None)
def svg_path(d: str) -> QPainterPath:
    path = QPainterPath()
    tokens = _TOKEN.findall(d)
    i, cmd = 0, "M"
    while i < len(tokens):
        tok = tokens[i]
        if tok in "MLCZ":
            cmd = tok
            i += 1
            if cmd == "Z":
                path.closeSubpath()
            continue
        if cmd == "M":
            path.moveTo(float(tokens[i]), float(tokens[i + 1]))
            i += 2
            cmd = "L"  # M'den sonraki çiftler L sayılır
        elif cmd == "L":
            path.lineTo(float(tokens[i]), float(tokens[i + 1]))
            i += 2
        elif cmd == "C":
            v = [float(t) for t in tokens[i:i + 6]]
            path.cubicTo(v[0], v[1], v[2], v[3], v[4], v[5])
            i += 6
        else:
            i += 1
    return path


def circle(x: float, y: float, r: float) -> QPainterPath:
    path = QPainterPath()
    path.addEllipse(QPointF(x, y), r, r)
    return path


# --- figürün sabit parçaları ---------------------------------------------------------

BODY = """M350,284 C330,290 300,293 280,289 C266,286 252,279 238,279 C226,279 216,284 211,292
    C204,300 201,310 203,322 C205,338 212,354 224,365 C236,360 250,357 262,355
    C282,362 304,372 332,372 C350,372 364,369 374,363 C386,356 398,344 402,326
    C404,306 400,292 396,284 Z"""
TAIL = """M214,292 C197,288 181,296 173,312 C163,334 167,362 157,390 C153,398 161,400 165,394
    C171,380 175,366 177,352 C177,370 175,386 181,402 C187,406 189,398 187,392 C185,372 189,350 195,332
    C199,318 207,304 215,298 Z"""
TORSO = """M363,204 C355,206 346,207 339,209 C329,212 325,222 327,233 C329,240 333,244 338,246
    C341,258 346,272 350,284 L396,284 C398,272 403,258 406,246 C411,244 415,240 417,233
    C419,222 415,212 405,209 C398,207 390,206 385,204 Z"""
NECK = "M364,186 L384,186 L386,207 L362,207 Z"
# Profil baş: düz Yunan burnu, kısa sakal, arkaya toplanmış saç.
HEAD = """M370,160 C382,159 391,165 393,174 L392.5,178 L400,188.5 L395,190.5
    C396.5,191.5 396.5,193 395.4,194.2 L397,197 C397.4,202 394.4,206 388.6,207.2 C383.6,207.6 379.6,205.6 377.4,202.4
    L366,200 L360,198.6 C354,196.6 352,188.6 353,182 C354,170 360,161 370,160 Z"""
HOOF = "M-4.8,-0.6 L4.6,-0.6 L10,10.4 C4.4,11.6 -3.6,11.6 -6.2,10.4Z"

# Kazıma çizgileri: az ve anlamlı (vazo ressamı gibi), ızgara değil.
BODY_LINES = (
    "M378,300 C384,316 388,330 386,344",
    "M268,300 C276,316 276,336 268,352 M290,302 C298,318 298,338 290,354 M312,302 C318,318 318,336 312,350",
    "M216,300 C230,300 240,306 246,318",
)
TORSO_LINES = (
    ("M365,211 C356,212 347,213 338,216 M383,211 C392,212 400,213 408,216", 1.0),
    ("M346,223 C343,235 352,243 371,241 M398,223 C401,235 392,243 373,241", 1.0),
    ("M372,217 L372,270", 0.75),
    ("M362,253 C366,255 378,255 382,253 M363,264 C367,266 377,266 381,264", 0.8),
    ("M370,275 C371,277 373,277 374,275", 1.0),
    ("M353,261 C357,271 361,279 365,285 M391,261 C387,271 383,279 379,285", 1.0),
    ("M341,214 C334,222 335,233 341,241 M403,214 C410,222 409,233 403,241", 1.0),
    ("M422,213 C434,209 444,209 452,211 M462,207.5 L486,203", 1.0),
    ("M350,286 C360,290 386,290 396,286", 1.0),
)
HEAD_LINES = (
    ("M383.5,173.6 C386.5,172.4 389.6,172.4 392.4,173.2", 1.0),
    ("M392.6,167.6 C384,163 366,165 356.4,176.4 M391.6,171.2 C382.6,167 367,169 357.6,180", 1.0),
    ("M370.6,182.6 C374.6,180.8 376.8,185.8 373.8,189.8 C372.6,190.8 371.4,189.8 371.2,188.8", 1.0),
    ("M372.4,186 C374,195 382,200.4 392.4,194.2 M390,192 L395.6,191.2", 1.0),
    ("M382.6,201.6 L381.4,205.6 M387.6,201.8 L387.8,206.4", 1.0),
    ("M357.6,185 C356,190.6 357.2,195 360.4,198 M362.4,183 C361,189 362,194.6 364.8,198.4", 0.75),
)
EYE = "M385.5,177.4 C387.6,175.4 390.4,175.2 392,177 C390.2,178.6 387.8,178.8 385.5,177.4Z"

BOW_HAND = (500.0, 203.0)
ANCHOR = (386.0, 198.0)       # tam gerilmişken kirişin yüzdeki yeri (çene altı)
REST = (500.0, 196.5)         # ok yumruğun üstünden geçiyor
STRING_REST = (492.0, 200.0)  # gevşek kirişin ortası
SHOULDER_DRAW = (336.0, 220.0)
ARROW_LENGTH = 142.0


def _bow_path() -> str:
    bx, by = BOW_HAND
    # İskit yayı: düz tutamak, öne kıvrılan kollar, geri dönen uçlar.
    return (
        f"M{bx - 4},{by - 91} C{bx - 11},{by - 95} {bx - 13},{by - 88} {bx - 8},{by - 84} "
        f"C{bx + 7},{by - 72} {bx + 15},{by - 42} {bx + 10},{by - 14} C{bx + 8},{by - 7} {bx + 4},{by - 3} {bx + 4},{by} "
        f"C{bx + 4},{by + 3} {bx + 8},{by + 7} {bx + 10},{by + 14} C{bx + 15},{by + 42} {bx + 7},{by + 72} {bx - 8},{by + 84} "
        f"C{bx - 13},{by + 88} {bx - 11},{by + 95} {bx - 4},{by + 91}"
    )


BOW = _bow_path()


# --- bacaklar ------------------------------------------------------------------------

FRONT = (30.0, 42.0, 40.0, 12.0, 0.0)   # parça boyları: kol, ön kol, incik, bilek, toynak
HIND = (52.0, 46.0, 42.0, 12.0, 0.0)    # but, baldır, incik, bilek, toynak
ATTACH = {"fn": (382.0, 320.0), "ff": (370.0, 320.0), "hn": (236.0, 296.0), "hf": (247.0, 300.0)}
SOLE = (2.0, 11.0)  # toynağın taban ortası (toynağın kendi biriminde)

# Tek parça bacak konturu: her örnek (parça, oran, arka kalınlık, ön kalınlık).
# Eklemlerde top yok; kas, diz ve bilek çıkıntısı kalınlıktan geliyor.
PROFILE = {
    "f": ((0, 0, 17, 15), (0, .7, 14, 13), (1, .08, 11.5, 11), (1, .45, 8.5, 8), (1, .9, 6.6, 6.4),
          (2, .06, 7, 6.8), (2, .22, 5, 4.8), (2, .8, 4.8, 4.6), (2, .97, 7, 5.6), (3, .45, 3.9, 3.9), (3, 1, 4.6, 4.6)),
    "h": ((0, 0, 26, 20), (0, .55, 24, 16), (0, .95, 26, 12), (1, .18, 25, 10), (1, .55, 16.5, 7.4), (1, .88, 10.5, 6),
          (2, .04, 10.5, 5.8), (2, .16, 6.6, 5.2), (2, .8, 5, 4.7), (2, .97, 7, 5.6), (3, .45, 3.9, 3.9), (3, 1, 4.6, 4.6)),
}
# Bacak kazımaları: (parça, oran başı, oran sonu, yan −1 arka / +1 ön, kalınlığın oranı)
LEG_LINES = {
    "f": ((1, .12, .8, -1, .45), (2, .25, .85, -1, .35)),
    "h": ((0, .25, .95, 1, .55), (1, .25, .85, 1, .3), (2, .2, .85, -1, .35)),
}


@dataclass
class Body:
    dy: float = 0.0     # gövdenin inip kalkması
    pitch: float = 0.0  # öne/arkaya yatma (derece, saat yönü)


@dataclass
class Pose:
    legs: dict
    body: Body = field(default_factory=Body)
    tail: float = 0.0
    lean: float = 0.0
    draw: float = 1.0        # yayın gerilmesi: 0 gevşek, 1 tam
    released: bool = False   # ok bırakıldı mı
    vib: float = 0.0         # bırakınca kirişin titreşimi (birim)
    follow: float = 0.0      # bırakınca elin geriye savrulması (0–1)


@dataclass(frozen=True)
class Style:
    fig: QColor
    far: QColor          # uzaktaki bacaklar: bir ton açık, derinlik için
    incise: QColor | None
    string: QColor
    arrow: QColor
    tip: QColor


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def clamp01(t: float) -> float:
    return 0.0 if t < 0 else 1.0 if t > 1 else t


def smoothstep(t: float) -> float:
    t = clamp01(t)
    return t * t * (3 - 2 * t)


def _body_xf(body: Body):
    c, s = math.cos(body.pitch * R), math.sin(body.pitch * R)

    def f(p):
        dx, dy = p[0] - 300, p[1] - 320
        return (300 + dx * c - dy * s, 320 + dx * s + dy * c + body.dy)

    return f


def _sole(ax, ay, chain, ang):
    x, y, a = ax, ay, 0.0
    for i, length in enumerate(chain):
        a += ang[i]
        if i < len(chain) - 1:
            x += math.sin(a * R) * length
            y += math.cos(a * R) * length
    c, s = math.cos(a * R), math.sin(a * R)
    return (x + SOLE[0] * c + SOLE[1] * s, y - SOLE[0] * s + SOLE[1] * c)


def plant(key: str, base, body: Body):
    """Ayağı zemine bastırır: bükümü ayarlar, toynağı düz yere koyar.

    Ön bacak omuz–dirsekten, arka bacak diz ekleminden bükülüyor (atın
    gerçekten büküldüğü yerler). Büküm arttıkça bacak kısalıyor, taban
    yükseliyor; ikiye bölerek aranıyor.
    """
    front = key[0] == "f"
    chain, (ax, ay), xf = (FRONT if front else HIND), ATTACH[key], _body_xf(body)

    def make(b):
        a = list(base)
        if front:
            a[0] -= b
            a[1] += b
        else:
            a[1] -= b
            a[2] += b
        a[4] = body.pitch - (a[0] + a[1] + a[2] + a[3])
        return a

    lo, hi = -60.0, 60.0
    for _ in range(32):
        m = (lo + hi) / 2
        if xf(_sole(ax, ay, chain, make(m)))[1] - GROUND > 0:
            lo = m
        else:
            hi = m
    return make((lo + hi) / 2)


# --- dörtnal ---------------------------------------------------------------------------
# Her bacak dört eşit aralıklı anahtar kare; döngüsel Catmull-Rom ile ara açılar.
CYCLE = {
    "f": ((-4, 12, -6, 32, -34),      # basış: dikey, geriye akıyor
          (-30, 8, 6, 44, -8),        # itiş: geride, parmak ucu kalkıyor
          (16, 30, -112, -8, -8),     # katlanma: diz bükük, toynak karnın altında
          (32, 30, -14, 26, 10)),     # uzanma: öne açılıyor
    "h": ((40, -80, 58, 34, -52),     # uzanma: karnın altından öne
          (22, -70, 48, 30, -30),     # basış
          (-30, -30, 14, -24, -20),   # itiş: geride açılıyor
          (46, -112, 64, 40, 8)),     # katlanma
}
# Döngüde basış penceresi (bacağın kendi evresi): içinde ayak zemine bastırılıyor.
STANCE = {"f": (-.14, .2), "h": (.1, .46)}
# Dörtnalda basış sırası: arka uzak, arka yakın, ön uzak, ön yakın; sonra havada.
OFFSET = {"hf": .2, "hn": .1, "ff": .62, "fn": .52}


def _cyc(frames, p):
    n = len(frames)
    k = (p % 1.0) * n
    i = int(math.floor(k))
    t = k - i
    p0, p1, p2, p3 = (frames[(i - 1) % n], frames[i % n], frames[(i + 1) % n], frames[(i + 2) % n])
    out = []
    for m in range(len(p1)):
        a, b, c, d = p0[m], p1[m], p2[m], p3[m]
        out.append(0.5 * ((2 * b) + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t * t
                          + (-a + 3 * b - 3 * c + d) * t * t * t))
    return out


def _stance_weight(kind, p):
    s0, s1 = STANCE[kind]
    length = s1 - s0
    d = (p - s0) % 1.0
    if d > length:
        return 0.0
    e = .05
    return smoothstep(min(d / e, (length - d) / e, 1.0))


def gallop_pose(g: float) -> Pose:
    """Dörtnal döngüsünün `g` evresindeki duruş (g'nin tam kısmı döngü sayısı)."""
    body = Body(dy=6 * math.cos(2 * math.pi * (g - .3)), pitch=-2.4 * math.cos(2 * math.pi * (g - .12)))
    legs = {}
    for key in ("fn", "ff", "hn", "hf"):
        kind = "f" if key[0] == "f" else "h"
        p = (g + OFFSET[key]) % 1.0
        free = _cyc(CYCLE[kind], p)
        w = _stance_weight(kind, p)
        if w > 0:
            planted = plant(key, free, body)
            free = [lerp(a, b, w) for a, b in zip(free, planted)]
        legs[key] = free
    return Pose(legs=legs, body=body, tail=30 + 8 * math.sin(2 * math.pi * (g + .2)),
                lean=8 - body.pitch * .6)


def aim_pose() -> Pose:
    """Durarak nişan alma: dört ayak yerde."""
    body = Body()
    legs = {
        "fn": plant("fn", (-18, 22, 0, 34, 0), body),
        "ff": plant("ff", (-30, 26, 0, 30, 0), body),
        "hn": plant("hn", (22, -70, 48, 30, 0), body),
        "hf": plant("hf", (30, -72, 44, 30, 0), body),
    }
    return Pose(legs=legs, body=body)


def with_bow(pose: Pose, **kw) -> Pose:
    return replace(pose, **kw)


# --- yol üretimi -------------------------------------------------------------------------

def _frames(ax, ay, chain, ang):
    out, x, y, a = [], ax, ay, 0.0
    for i, length in enumerate(chain):
        a += ang[i]
        out.append((x, y, a, length))
        x += math.sin(a * R) * length
        y += math.cos(a * R) * length
    return out


def _along(frames, seg, t, side, w):
    s, tt = seg, t
    while tt > 1 and s < len(frames) - 1:
        tt -= 1
        s += 1
    x, y, a0, length = frames[s]
    nx, ny = x + math.sin(a0 * R) * length * tt, y + math.cos(a0 * R) * length * tt
    nxt, prv = frames[min(s + 1, len(frames) - 1)], frames[max(s - 1, 0)]

    def fark(p, q):
        return ((q - p + 540) % 360) - 180

    # Eklemin iki yanında yön komşu parçanınkiyle yarı yarıya karışıyor: kırılma yok.
    a = a0
    if tt > .75:
        a += fark(a0, nxt[2]) * (tt - .75) / .25 * .5
    elif tt < .25:
        a += fark(a0, prv[2]) * (.25 - tt) / .25 * .5
    return (nx + math.cos(a * R) * w * side, ny - math.sin(a * R) * w * side)


def _smooth(points, closed: bool) -> QPainterPath:
    """Noktalardan geçen yumuşak eğri (Catmull-Rom → kübik Bezier)."""
    if closed:
        pts = [points[-1], *points, points[0], points[1]]
    else:
        pts = [points[0], *points, points[-1]]
    path = QPainterPath()
    path.moveTo(*points[0])
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        path.cubicTo(
            p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
            p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6,
            p2[0], p2[1],
        )
    if closed:
        path.closeSubpath()
    return path


def _width_at(prof, g, side):
    col = 2 if side < 0 else 3
    for i in range(len(prof) - 1):
        g0, g1 = prof[i][0] + prof[i][1], prof[i + 1][0] + prof[i + 1][1]
        if g0 <= g <= g1:
            u = (g - g0) / ((g1 - g0) or 1)
            return prof[i][col] + (prof[i + 1][col] - prof[i][col]) * u
    return 6.0


def _tapered(points):
    """Kalınlığı değişen, uçları yuvarlak kol: dörtgenler ve eklem daireleri.

    Her parça ayrı dolduruluyor; aynı yolda yönleri çakışınca delik açılıyordu.
    """
    shapes = []
    for (x0, y0, w0), (x1, y1, w1) in zip(points, points[1:]):
        length = math.hypot(x1 - x0, y1 - y0) or 1.0
        nx, ny = -(y1 - y0) / length, (x1 - x0) / length
        quad = QPainterPath()
        quad.moveTo(x0 + nx * w0 / 2, y0 + ny * w0 / 2)
        quad.lineTo(x1 + nx * w1 / 2, y1 + ny * w1 / 2)
        quad.lineTo(x1 - nx * w1 / 2, y1 - ny * w1 / 2)
        quad.lineTo(x0 - nx * w0 / 2, y0 - ny * w0 / 2)
        quad.closeSubpath()
        shapes.append(quad)
        shapes.append(circle(x1, y1, w1 / 2))
    shapes.append(circle(points[0][0], points[0][1], points[0][2] / 2))
    return shapes


def _ik(shoulder, wrist, lu, lf):
    """İki kemikli kol, dirsek yukarıda."""
    dx, dy = wrist[0] - shoulder[0], wrist[1] - shoulder[1]
    d = math.hypot(dx, dy) or 1.0
    max_d = lu + lf - .5
    if d > max_d:
        dx, dy, d = dx * max_d / d, dy * max_d / d, max_d
    cos_a = max(-1.0, min(1.0, (lu * lu + d * d - lf * lf) / (2 * lu * d)))
    base = math.atan2(dy, dx) - math.acos(cos_a)
    elbow = (shoulder[0] + math.cos(base) * lu, shoulder[1] + math.sin(base) * lu)
    return elbow, (shoulder[0] + dx, shoulder[1] + dy)


def string_point(pose: Pose):
    return (lerp(STRING_REST[0], ANCHOR[0], pose.draw), lerp(STRING_REST[1], ANCHOR[1], pose.draw))


def upper_xf(pose: Pose):
    """Belden yukarısındaki bir noktanın figür koordinatındaki yeri."""
    bx = _body_xf(pose.body)
    c, s = math.cos(pose.lean * R), math.sin(pose.lean * R)

    def f(p):
        sx, sy = 372 + (p[0] - 372) * UPPER, 284 + (p[1] - 284) * UPPER
        dx, dy = sx - 372, sy - 284
        return bx((372 + dx * c - dy * s, 284 + dx * s + dy * c))

    return f


def arrow_line(pose: Pose):
    """Okun kertiği ve yönü, figür koordinatında (bırakılınca sahne kullanıyor)."""
    xf = upper_xf(pose)
    sp = string_point(pose)
    nock, rest = xf(sp), xf(REST)
    dx, dy = rest[0] - nock[0], rest[1] - nock[1]
    length = math.hypot(dx, dy) or 1.0
    return nock, (dx / length, dy / length)


# --- çizim --------------------------------------------------------------------------------

def _pen(color: QColor, width: float) -> QPen:
    pen = QPen(color, width)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    return pen


def _stroke(painter: QPainter, d: str, color: QColor, width: float, opacity: float = 1.0) -> None:
    c = QColor(color)
    c.setAlphaF(c.alphaF() * opacity)
    painter.strokePath(svg_path(d), _pen(c, width))


def draw_arrow(painter: QPainter, nock, u, length: float, style: Style) -> None:
    """Ok: gövde çizgisi, yaprak biçimli uç, iki tüy. `u` birim yön."""
    n = (-u[1], u[0])
    tip = (nock[0] + u[0] * length, nock[1] + u[1] * length)

    def pt(p, a, b):
        return QPointF(p[0] + u[0] * a + n[0] * b, p[1] + u[1] * a + n[1] * b)

    painter.setPen(_pen(style.arrow, 3.0))
    painter.drawLine(QPointF(*nock), pt(tip, -2, 0))
    painter.setPen(Qt.PenStyle.NoPen)
    head = QPainterPath(pt(tip, 16, 0))
    head.cubicTo(pt(tip, 8, -5), pt(tip, 0, -5), pt(tip, -2, -1))
    head.lineTo(pt(tip, -2, 1))
    head.cubicTo(pt(tip, 0, 5), pt(tip, 8, 5), pt(tip, 16, 0))
    painter.fillPath(head, style.tip)
    draw_fletching(painter, nock, u, style.arrow)


def draw_fletching(painter: QPainter, nock, u, color: QColor) -> None:
    """Okun arkasındaki iki tüy (saplanmış okta yalnızca bunlar ve gövde görünüyor)."""
    n = (-u[1], u[0])

    def pt(p, a, b):
        return QPointF(p[0] + u[0] * a + n[0] * b, p[1] + u[1] * a + n[1] * b)

    fletch = QPainterPath(pt(nock, 2, 0))
    fletch.lineTo(pt(nock, 16, -1))
    fletch.lineTo(pt(nock, 6, -8))
    fletch.closeSubpath()
    fletch.moveTo(pt(nock, 2, 0))
    fletch.lineTo(pt(nock, 16, 1))
    fletch.lineTo(pt(nock, 6, 8))
    fletch.closeSubpath()
    painter.fillPath(fletch, color)


def _leg(painter: QPainter, key: str, ang, fill: QColor, incise: QColor | None) -> None:
    kind = "f" if key[0] == "f" else "h"
    chain = FRONT if kind == "f" else HIND
    frames = _frames(*ATTACH[key], chain, ang)
    prof = PROFILE[kind]
    front = [_along(frames, s, t, 1, f) for s, t, _b, f in prof]
    back = [_along(frames, s, t, -1, b) for s, t, b, _f in prof]
    painter.fillPath(_smooth(front + back[::-1], True), fill)

    x, y, a, _ = frames[-1]
    painter.save()
    painter.translate(x, y)
    painter.rotate(-a)
    painter.fillPath(svg_path(HOOF), fill)
    if incise is not None:
        painter.setPen(_pen(incise, 1.3))
        painter.drawLine(QPointF(-4.6, 4.6), QPointF(7.6, 4.6))
    painter.restore()

    if incise is None:
        return
    pen = _pen(incise, 1.3)
    for s, t0, t1, side, r in LEG_LINES[kind]:
        pts = []
        for q in (0, .25, .5, .75, 1):
            t = t0 + (t1 - t0) * q
            pts.append(_along(frames, s, t, side, _width_at(prof, s + t, side) * r))
        painter.strokePath(_smooth(pts, False), pen)


def draw_centaur(painter: QPainter, pose: Pose, style: Style) -> None:
    """Figürü kendi koordinatında çizer (ölçek ve konum çizenin işi)."""
    fig, far, inc = style.fig, style.far, style.incise
    painter.save()
    painter.setPen(Qt.PenStyle.NoPen)
    painter.translate(0, pose.body.dy)
    painter.translate(300, 320)
    painter.rotate(pose.body.pitch)
    painter.translate(-300, -320)

    _leg(painter, "ff", pose.legs["ff"], far, None)
    _leg(painter, "hf", pose.legs["hf"], far, None)

    painter.save()
    painter.translate(214, 292)
    painter.rotate(pose.tail)
    painter.translate(-214, -292)
    painter.fillPath(svg_path(TAIL), fig)
    painter.restore()

    painter.fillPath(svg_path(BODY), fig)
    if inc is not None:
        for d in BODY_LINES:
            _stroke(painter, d, inc, 1.5)
    _leg(painter, "hn", pose.legs["hn"], fig, inc)
    _leg(painter, "fn", pose.legs["fn"], fig, inc)

    # belden yukarısı
    painter.save()
    painter.translate(372, 284)
    painter.rotate(pose.lean)
    painter.scale(UPPER, UPPER)
    painter.translate(-372, -284)
    for d in (TORSO, NECK, HEAD):
        painter.fillPath(svg_path(d), fig)
    for shape in _tapered(((410, 220, 17), (455, 212, 12.5), (491, 204.5, 10))):
        painter.fillPath(shape, fig)
    painter.fillPath(circle(*BOW_HAND, 7.6), fig)
    if inc is not None:
        for d, op in TORSO_LINES + HEAD_LINES:
            _stroke(painter, d, inc, 1.5, op)
        painter.fillPath(svg_path(EYE), inc)

    bx, by = BOW_HAND
    painter.strokePath(svg_path(BOW), _pen(fig, 6.4))

    # kiriş, ok ve çeken kol
    sp = string_point(pose)
    string = (STRING_REST[0] + pose.vib, STRING_REST[1]) if pose.released else sp
    string_path = QPainterPath(QPointF(bx - 8, by - 84))
    string_path.lineTo(*string)
    string_path.lineTo(bx - 8, by + 84)
    painter.strokePath(string_path, _pen(style.string, 1.4))

    if not pose.released:
        dx, dy = REST[0] - sp[0], REST[1] - sp[1]
        length = math.hypot(dx, dy) or 1.0
        u = (dx / length, dy / length)
        draw_arrow(painter, (sp[0] - u[0] * 4, sp[1] - u[1] * 4), u, ARROW_LENGTH, style)
        painter.setPen(Qt.PenStyle.NoPen)

    # Bırakınca el geriye, kulağa doğru savruluyor.
    if pose.released:
        hand = (ANCHOR[0] - 16 * pose.follow, ANCHOR[1] - 5 * pose.follow)
    else:
        hand = (sp[0] - 5, sp[1] + .5)
    elbow, wrist = _ik(SHOULDER_DRAW, (hand[0] - 8, hand[1]), 30, 57)
    for shape in _tapered(((*SHOULDER_DRAW, 16), (*elbow, 13), (*wrist, 10))):
        painter.fillPath(shape, fig)
    painter.fillPath(circle(*hand, 7), fig)
    if inc is not None:
        # Çeken kol boynun ve sakalın önünden geçiyor: siyah üstünde siyah,
        # kenarı kazınıyor ki kol okunsun.
        dx, dy = wrist[0] - elbow[0], wrist[1] - elbow[1]
        length = math.hypot(dx, dy) or 1.0
        u, n = (dx / length, dy / length), (-dy / length, dx / length)

        def e(p, a, b):
            return QPointF(p[0] + u[0] * a + n[0] * b, p[1] + u[1] * a + n[1] * b)

        pen = _pen(inc, 1.5)
        painter.setPen(pen)
        painter.drawLine(e(elbow, 2, -6), e(wrist, -2, -4.8))
        painter.drawLine(e(elbow, 4, 6), e(wrist, -2, 4.8))
        painter.drawLine(QPointF(hand[0] + 2.4, hand[1] - 5.2), QPointF(hand[0] + 2.4, hand[1] + 5.2))
        painter.setPen(Qt.PenStyle.NoPen)
    painter.restore()  # belden yukarısı
    painter.restore()
