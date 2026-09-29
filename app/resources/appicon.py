"""Uygulamanın kendi simgesi ve Discord görselleri.

Pencere başlığında, görev çubuğunda, paketlenmiş `.exe` dosyasında ve
Windows bildiriminde görünen simge (`tools/build_icon.py` bunları dosyaya
yazıyor).

**Tasarım (29 Eylül, Alican: "maskotumuz var artık onu içeren bir
görsel"):** açılış animasyonunun dili. Uygulamanın morunda yuvarlak kare,
arkada soluk bir ay diski, önünde siyah figür üslubunda yayını germiş
sentor; ayakları zemin çizgisinde, altında menderes şeridi (vazo bordürü).
Önceki simge yükselen bir yol ve yıldızdı.

**Küçük boyutlarda sadeleşiyor.** 16–32 pikselde kazıma çizgileri ve
menderes birer gürültü lekesine dönüşüyor; orada figür büyüyor, yalnızca
siluet ve zemin kalıyor. Sentor 16 pikselde bile kuyruğu, gövdesi ve
yayıyla okunuyor.

Figür `widgets/centaur.py` ile çiziliyor (QPainter); renkler açılışınkiler.
"""

from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QRadialGradient

# Simge kare tuvalde 512 birim üzerinden yerleştiriliyor.
CANVAS = 512.0

# Figürün kendi birimindeki görünen sınırları (kuyruk – ok ucu, yay ucu – toynak).
FIG_LEFT, FIG_RIGHT = 150.0, 530.0
FIG_TOP, FIG_BOTTOM = 128.0, 458.0

# Bu boyuttan küçükte ayrıntı (kazıma, menderes, ay hâlesi) çizilmiyor.
DETAIL_MIN = 64


def _alpha(color: QColor, a: float) -> QColor:
    c = QColor(color)
    c.setAlphaF(max(0.0, min(1.0, a)))
    return c


def _colors():
    # Renkler açılış sahnesinden; içe aktarma burada, çünkü `ui.intro`
    # arayüz modüllerini de yüklüyor ve simge onlardan önce gerekebiliyor.
    from ..ui import intro as I

    return I


def _meander(p: QPainter, x0: float, top: float, width: float, unit: float, height: float,
             color: QColor, pen: float) -> None:
    kalem = QPen(color, pen)
    kalem.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
    p.setPen(kalem)
    p.setBrush(Qt.BrushStyle.NoBrush)
    yol = QPainterPath()
    x = x0
    while x + unit * .75 <= x0 + width:
        yol.moveTo(x, top + height)
        yol.lineTo(x, top)
        yol.lineTo(x + unit * .75, top)
        yol.lineTo(x + unit * .75, top + height * .72)
        yol.lineTo(x + unit * .3, top + height * .72)
        yol.lineTo(x + unit * .3, top + height * .36)
        x += unit
    p.drawPath(yol)


def _figure(p: QPainter, x: float, ground: float, scale: float, detail: bool, line: float = 1.0) -> None:
    """Nişan almış sentoru, sol-üst köşesi değil **toynak hizası** `ground` olacak şekilde çizer."""
    from ..widgets import centaur as C

    I = _colors()
    stil = I.STYLE if detail else C.Style(fig=I.INK, far=I.INK_FAR, incise=None,
                                          string=I.INK, arrow=I.INK, tip=I.INK)
    poz = C.aim_pose()
    p.save()
    p.translate(x, ground - C.GROUND * scale)
    p.scale(scale, scale)
    C.draw_centaur(p, poz, stil, line)
    p.restore()


def paint_icon(p: QPainter, size: float, rounded: bool = True) -> None:
    """Simgeyi `size` × `size` alana çizer.

    `rounded=False` Discord için: köşeleri platform kendisi yuvarlıyor ya da
    daireye kırpıyor; yuvarlak kare üstüne ikinci bir yuvarlama çirkin.
    """
    I = _colors()
    detail = size >= DETAIL_MIN
    p.save()
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    k = size / CANVAS

    alan = QPainterPath()
    if rounded:
        alan.addRoundedRect(QRectF(0, 0, size, size), 112 * k, 112 * k)
    else:
        alan.addRect(QRectF(0, 0, size, size))
    p.setClipPath(alan)

    zemin = QRadialGradient(QPointF(size * .42, size * .34), size * .85)
    zemin.setColorAt(0.0, I.GROUND_IN)
    zemin.setColorAt(0.5, I.GROUND_MID)
    zemin.setColorAt(1.0, I.GROUND_OUT)
    p.fillRect(QRectF(0, 0, size, size), zemin)

    # Küçükte figür tuvali daha çok dolduruyor.
    doluluk = .86 if detail else .98
    yer = (.79 if detail else .86) * size
    olcek = min(doluluk * size / (FIG_RIGHT - FIG_LEFT), (yer - size * .05) / (FIG_BOTTOM - FIG_TOP))
    x = (size - (FIG_RIGHT - FIG_LEFT) * olcek) / 2 - FIG_LEFT * olcek

    # Ay diski: figürün üst gövdesinin arkasında, siluet açık zeminde okunsun.
    ay = QPointF(x + 400 * olcek, yer - 250 * olcek)
    r = 150 * olcek
    if detail:
        hale = QRadialGradient(ay, r * 1.9)
        hale.setColorAt(0, _alpha(I.SPARK, .35))
        hale.setColorAt(1, _alpha(I.SPARK, 0))
        p.fillRect(QRectF(0, 0, size, size), hale)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(_alpha(I.RING_LIGHT, .55 if detail else .45))
    p.drawEllipse(ay, r, r)

    # Zemin: toynakların bastığı çizgi ve altındaki koyu şerit.
    p.fillRect(QRectF(0, yer, size, size - yer), _alpha(I.GROUND_OUT, .6))
    p.setPen(QPen(I.INK, max(1.0, 7 * k)))
    p.drawLine(QPointF(0, yer), QPointF(size, yer))
    if detail:
        unit = 34 * k
        genislik = size - 2 * 30 * k
        adet = int(genislik // unit)
        sol = (size - adet * unit + unit * .25) / 2
        _meander(p, sol, yer + (size - yer) * .34, adet * unit, unit, 16 * k, _alpha(I.INK, .85), max(1.0, 4.2 * k))

    # Küçükte yay en az ~1,3 piksel kalınlıkta: yoksa okçu değil at adam.
    kalin = 1.0 if detail else max(1.0, 1.3 / (6.4 * olcek))
    _figure(p, x, yer + 3 * olcek, olcek, detail, kalin)
    p.restore()


def paint_banner(p: QPainter, width: float, height: float, tagline: str, subline: str) -> None:
    """README'nin başındaki banner (`docs/media/banner_<dil>.png`).

    Solda nişan almış sentor, sağda "Odyssey" yazısı, altında menderes ve
    iki satır açıklama; zemin açılışın moru, üstte ve altta menderes bordürü.
    """
    import random

    from .theme.tokens import FONTS

    I = _colors()
    p.save()
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    zemin = QRadialGradient(QPointF(width * .34, height * .3), width * .75)
    zemin.setColorAt(0.0, I.GROUND_IN)
    zemin.setColorAt(0.5, I.GROUND_MID)
    zemin.setColorAt(1.0, I.GROUND_OUT)
    p.fillRect(QRectF(0, 0, width, height), zemin)

    # soluk yıldızlar (yalnızca gökte)
    rnd = random.Random(7)
    p.setPen(Qt.PenStyle.NoPen)
    for _ in range(40):
        x, y = rnd.uniform(0, width), rnd.uniform(height * .12, height * .55)
        r = rnd.uniform(.8, 1.9)
        p.setBrush(_alpha(I.SPARK, rnd.uniform(.25, .6)))
        p.drawEllipse(QPointF(x, y), r, r)

    yer = height * .83
    # iki kat tepe
    for oran, yuk, renk in ((.36, height * .12, _alpha(I.HILL, .45)), (.52, height * .07, _alpha(I.HILL, .7))):
        tepe = QPainterPath(QPointF(0, yer))
        adim = width * oran
        xx = -adim * .3
        while xx < width + adim:
            tepe.cubicTo(xx + adim * .2, yer - yuk, xx + adim * .4, yer - yuk * 1.15, xx + adim * .55, yer - yuk * .3)
            tepe.cubicTo(xx + adim * .7, yer, xx + adim * .85, yer - yuk * .6, xx + adim, yer)
            xx += adim
        tepe.lineTo(width, yer + 2)
        tepe.lineTo(0, yer + 2)
        tepe.closeSubpath()
        p.fillPath(tepe, renk)
    p.fillRect(QRectF(0, yer, width, height - yer), _alpha(I.GROUND_OUT, .55))
    p.setPen(QPen(I.INK, 3))
    p.drawLine(QPointF(0, yer), QPointF(width, yer))

    unit = 28.0
    _meander(p, 20, 20, width - 40, unit, 13, _alpha(I.INK, .85), 2.4)
    _meander(p, 20, height - 35, width - 40, unit, 13, _alpha(I.INK, .85), 2.4)

    # sentor: sol üçte bir, arkasında ay diski
    olcek = height * .62 / (FIG_BOTTOM - FIG_TOP)
    fx = width * .045 - FIG_LEFT * olcek
    ay = QPointF(fx + 400 * olcek, yer - 250 * olcek)
    r = 150 * olcek
    hale = QRadialGradient(ay, r * 2)
    hale.setColorAt(0, _alpha(I.SPARK, .3))
    hale.setColorAt(1, _alpha(I.SPARK, 0))
    p.fillRect(QRectF(0, 0, width, height), hale)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(_alpha(I.RING_LIGHT, .5))
    p.drawEllipse(ay, r, r)
    _figure(p, fx, yer + 3 * olcek, olcek, True)

    # yazı bloğu
    sol = width * .40
    aile = FONTS["display"].split(",")[0].strip().strip('"')
    baslik = QFont(aile)
    baslik.setPixelSize(int(height * .25))
    baslik.setWeight(QFont.Weight.DemiBold)
    baslik.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, height * .012)
    p.setFont(baslik)
    p.setPen(I.INK)
    taban = height * .37
    p.drawText(QPointF(sol, taban), "Odyssey")
    genis = p.fontMetrics().horizontalAdvance("Odyssey")
    # Menderes harflerin kuyruğunun (y) altında kalsın.
    _meander(p, sol + 4, taban + height * .085, genis, 24.0, 12, I.INK, 2.6)

    metin = QFont(FONTS["ui"].split(",")[0].strip().strip('"'))
    metin.setPixelSize(int(height * .058))
    metin.setWeight(QFont.Weight.DemiBold)
    p.setFont(metin)
    p.setPen(_alpha(I.INK, .92))
    kutu = QRectF(sol, taban + height * .16, width * .56, height * .2)
    p.drawText(kutu, int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop | Qt.TextFlag.TextWordWrap), tagline)
    satir = p.fontMetrics().boundingRect(kutu.toRect(), int(Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextWordWrap), tagline)
    kucuk = QFont(metin)
    kucuk.setPixelSize(int(height * .044))
    kucuk.setWeight(QFont.Weight.Medium)
    p.setFont(kucuk)
    p.setPen(_alpha(I.INK, .7))
    p.drawText(QPointF(sol, satir.bottom() + height * .075), subline)
    p.restore()


def paint_cover(p: QPainter, width: float, height: float, title: str = "ODYSSEY") -> None:
    """Discord kapak görseli (16:9): açılış sahnesinin özeti.

    Solda nişan almış sentor, sağda hedef ve ODYSSEY yazısı; üstte ve altta
    menderes bordürü.
    """
    I = _colors()
    p.save()
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    zemin = QRadialGradient(QPointF(width * .45, height * .38), width * .7)
    zemin.setColorAt(0.0, I.GROUND_IN)
    zemin.setColorAt(0.55, I.GROUND_MID)
    zemin.setColorAt(1.0, I.GROUND_OUT)
    p.fillRect(QRectF(0, 0, width, height), zemin)

    yer = height * .76
    # uzak tepeler
    tepe = QPainterPath(QPointF(0, yer))
    adim = width * .42
    xx = -adim * .2
    while xx < width + adim:
        tepe.cubicTo(xx + adim * .2, yer - 44, xx + adim * .4, yer - 50, xx + adim * .55, yer - 14)
        tepe.cubicTo(xx + adim * .7, yer, xx + adim * .85, yer - 28, xx + adim, yer)
        xx += adim
    tepe.lineTo(width, yer + 2)
    tepe.lineTo(0, yer + 2)
    tepe.closeSubpath()
    p.fillPath(tepe, _alpha(I.HILL, .55))
    p.fillRect(QRectF(0, yer, width, height - yer), _alpha(I.GROUND_OUT, .5))
    p.setPen(QPen(I.INK, 3))
    p.drawLine(QPointF(0, yer), QPointF(width, yer))

    # bordürler
    unit = 26.0
    _meander(p, 14, 18, width - 28, unit, 12, _alpha(I.INK, .85), 2.2)
    _meander(p, 14, height - 30, width - 28, unit, 12, _alpha(I.INK, .85), 2.2)

    # sentor
    olcek = height * .45 / (FIG_BOTTOM - FIG_TOP)
    _figure(p, width * .035 - FIG_LEFT * olcek, yer + 3 * olcek, olcek, True)

    # hedef: okun hizasında, sehpasıyla zemine iniyor
    from ..widgets import centaur as C

    ok_y = yer - (C.GROUND - 211.8) * olcek
    hx, r = width * .41, 46.0
    kalem = QPen(I.INK, 7)
    kalem.setCapStyle(Qt.PenCapStyle.RoundCap)
    p.setPen(kalem)
    p.drawLine(QPointF(hx, ok_y), QPointF(hx - r * .8, yer))
    p.drawLine(QPointF(hx, ok_y), QPointF(hx + r * .72, yer))
    p.setPen(Qt.PenStyle.NoPen)
    for oran, renk in ((1.0, I.INK), (.82, I.RING_LIGHT), (.66, I.INK), (.48, I.RING_LIGHT), (.3, I.INK), (.14, I.RING_LIGHT)):
        p.setBrush(renk)
        p.drawEllipse(QPointF(hx, ok_y), r * oran, r * oran)
    p.setBrush(I.INCISE)
    for i in range(28):
        a = i * 2 * math.pi / 28
        p.drawEllipse(QPointF(hx + math.cos(a) * r * .91, ok_y + math.sin(a) * r * .91), 1.4, 1.4)

    # başlık
    # Açılıştaki başlıkla aynı yazı tipi ve harf aralığı.
    from .theme.tokens import FONTS

    font = QFont(FONTS["display"].split(",")[0].strip().strip('"'))
    font.setPixelSize(int(height * .12))
    font.setWeight(QFont.Weight.DemiBold)
    font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, height * .024)
    p.setFont(font)
    p.setPen(I.INK)
    sol = hx + r + width * .045
    taban = ok_y + height * .045
    p.drawText(QPointF(sol, taban), title)
    genis = p.fontMetrics().horizontalAdvance(title) - height * .024
    _meander(p, sol + 2, taban + height * .04, genis, 22.0, 11, I.INK, 2.4)
    p.restore()
