"""Sağ altta beliren kutlama kartları.

Bölüm bitince ve rozet kazanılınca pencerenin sağ alt köşesinde bir kart
çıkıyor. Önceden alt şeritteki zilde bir bildirim listesi birikiyordu;
kimse açıp bakmıyordu, kutlama da o an değil günler sonra fark ediliyordu
(Alican, 25 Eylül: "zil kalksın, bitirince sağ altta çıksın").

Kart **tamamen elle çiziliyor**, alt widget yok. İki sebebi var:

* Giriş ve çıkışta kartın bütünü saydamlaşıyor. `QGraphicsOpacityEffect`
  gölgeyle aynı widget'a konamıyor (bir widget'ın tek efekti olabiliyor) ve
  alt widget'lardaki yazıları ayrıca soldurmak gerekiyordu. Her şey
  `paintEvent` içinde olunca tek bir `setOpacity` yetiyor.
* Gölge de elle: birkaç katman yarı saydam yuvarlak dikdörtgen. Kartlar
  pencerenin içinde birer alt widget; üst düzey pencere olsalardı Windows
  odak çalıyor ve pencereyle birlikte hareket etmiyorlardı.

Hareketler:

* giriş: sağdan kayarak ve belirerek (`OutCubic`);
* simge: küçükten büyüyüp esneyerek yerine oturuyor (yay, `bounce`),
  arkasından bir halka dalgası ve rozetlerde dağılan küçük parıltılar.
  Rozet kartında rozetin madalyası, bölüm kartında patikanın logosu var
  (0.9.0); ikisi de profildeki ve yoldaki çizimle aynı;
* Ayarlar › Animasyonlar kapalıysa kart hareketsiz belirir, süre yine işler;
* alt kenardaki ince çizgi kalan süreyi gösteriyor; fare kartın üstündeyken
  süre duruyor, çıkınca kaldığı yerden devam ediyor;
* çıkış: sağa kayıp sönerek. Yukarıdaki kartlar boşalan yere iniyor.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QParallelAnimationGroup,
    QPoint,
    QPointF,
    QPropertyAnimation,
    QRectF,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import QColor, QFont, QFontMetrics, QLinearGradient, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QWidget

from ..resources.icons import pixmap
from ..resources.logos import logo_pixmap
from ..resources.medals import medal_pixmap
from ..resources.theme.motion import bounce
from . import motion
from ..resources.theme.tokens import PALETTES

CARD_WIDTH = 360
CARD_HEIGHT = 96
# Gölgenin kartın dışına taştığı pay.
SHADOW = 14
# Girişte kartın ne kadar sağdan geldiği.
SLIDE = 48
CIRCLE = 50
# Madalya ve logo kartta biraz daha büyük çiziliyor (dairenin yerine).
MEDAL = 66
LOGO = 54
ICON = 24
RADIUS = 14
# Kart ekranda ne kadar kalıyor (fare üstündeyken süre işlemiyor).
DURATION_MS = 7000
GAP = 10
MAX_VISIBLE = 3
# Aynı anda gelen kartlar (bölüm bitince çoğu zaman bir de rozet geliyor)
# arka arkaya giriyor. Hepsi aynı karede girince yarı saydam hâlleri üst
# üste biniyor ve okunmuyordu.
ENTRY_GAP_MS = 380


@dataclass(frozen=True)
class ToastData:
    kind: str            # "badge" | "section"
    eyebrow: str         # "YENİ ROZET"
    title: str           # rozetin ya da bölümün adı
    subtitle: str        # açıklama
    icon: str            # `app/resources/icons.py` içindeki ad
    color: str           # dairenin rengi
    color2: str = ""     # degradenin ikinci rengi (boşsa tek renk)
    payload: tuple = ()  # tıklanınca ne açılacağı
    medal: tuple = ()    # rozet kartı: (şekil, kademe, işaret)
    logo: str = ""       # bölüm kartı: patika logosunun anahtarı


class Toast(QWidget):
    """Tek bir kart."""

    closed = Signal(object)
    activated = Signal(object)

    def __init__(self, data: ToastData, mode: str, close_tip: str, parent: QWidget) -> None:
        super().__init__(parent)
        self.data = data
        self._mode = mode
        self._fade = 0.0
        self._pop = 0.0
        self._pulse = 0.0
        self._remaining = 1.0
        self._hover_close = False
        self._closing = False

        self.setFixedSize(CARD_WIDTH + 2 * SHADOW, CARD_HEIGHT + 2 * SHADOW)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("")
        self._close_tip = close_tip

        self._icon_pix = pixmap(data.icon, "#FFFFFF", ICON)
        self._art = None
        if data.medal:
            self._art = medal_pixmap(*data.medal, MEDAL)
        elif data.logo:
            self._art = logo_pixmap(data.logo, data.color, LOGO)

        # Kalan süre çizgisi; biterse kart kapanıyor.
        self._timer_anim = QPropertyAnimation(self, b"remaining", self)
        self._timer_anim.setStartValue(1.0)
        self._timer_anim.setEndValue(0.0)
        self._timer_anim.setDuration(DURATION_MS)
        self._timer_anim.finished.connect(self.dismiss)

        self._move_anim: QPropertyAnimation | None = None
        self._exit_group: QParallelAnimationGroup | None = None

    # --- canlandırılan özellikler ------------------------------------------

    def _get_fade(self) -> float:
        return self._fade

    def _set_fade(self, value: float) -> None:
        self._fade = value
        self.update()

    fade = Property(float, _get_fade, _set_fade)

    def _get_pop(self) -> float:
        return self._pop

    def _set_pop(self, value: float) -> None:
        self._pop = value
        self.update()

    pop = Property(float, _get_pop, _set_pop)

    def _get_pulse(self) -> float:
        return self._pulse

    def _set_pulse(self, value: float) -> None:
        self._pulse = value
        self.update()

    pulse = Property(float, _get_pulse, _set_pulse)

    def _get_remaining(self) -> float:
        return self._remaining

    def _set_remaining(self, value: float) -> None:
        self._remaining = value
        self.update()

    remaining = Property(float, _get_remaining, _set_remaining)

    # --- giriş, yer değiştirme, çıkış --------------------------------------

    def enter(self, target: QPoint) -> None:
        """Hedefin sağından kayarak ve belirerek gelir."""
        if not motion.enabled():
            # Hareketsiz: kart yerinde belirir, halka ve parıltı yok; süre işler.
            self.move(target)
            self.show()
            self.raise_()
            self._fade, self._pop, self._pulse = 1.0, 1.0, 1.0
            self._timer_anim.start()
            return
        self.move(target + QPoint(SLIDE, 0))
        self.show()
        self.raise_()

        kay = QPropertyAnimation(self, b"pos", self)
        kay.setStartValue(target + QPoint(SLIDE, 0))
        kay.setEndValue(target)
        kay.setDuration(420)
        kay.setEasingCurve(QEasingCurve.Type.OutCubic)

        bel = QPropertyAnimation(self, b"fade", self)
        bel.setStartValue(0.0)
        bel.setEndValue(1.0)
        bel.setDuration(320)
        bel.setEasingCurve(QEasingCurve.Type.OutQuad)

        # Kayma ve belirme **ayrı** başlatılıyor, bir gruba konmuyor. Bu kart
        # yerine oturmadan yeni bir kart gelirse `slide_to` aynı `pos`
        # özelliğine yeni bir animasyon başlatıyor; Qt eskisini durduruyor ve
        # ikisi aynı gruptaysa grup da duruyordu: kart yerine gidiyor ama
        # saydam kalıyordu (ölçüldü: üç karttan ikisi görünmez).
        self._move_anim = kay
        kay.start()
        bel.start()

        # Simge kart yerine oturmaya yaklaşırken patlıyor.
        pop = QPropertyAnimation(self, b"pop", self)
        pop.setStartValue(0.0)
        pop.setEndValue(1.0)
        pop.setDuration(560)
        # Doğrusal koşuyor; çizimde `bounce` yayından geçiriliyor (theme.motion).
        pop.setEasingCurve(QEasingCurve.Type.Linear)
        dalga = QPropertyAnimation(self, b"pulse", self)
        dalga.setStartValue(0.0)
        dalga.setEndValue(1.0)
        dalga.setDuration(900)
        dalga.setEasingCurve(QEasingCurve.Type.OutCubic)
        simge = QParallelAnimationGroup(self)
        simge.addAnimation(pop)
        simge.addAnimation(dalga)

        # Simge, kart yerine oturmaya yaklaşırken patlasın diye kısa bir
        # gecikmeyle ayrıca başlatılıyor.
        QTimer.singleShot(200, simge.start)
        QTimer.singleShot(200, self._timer_anim.start)

    def slide_to(self, target: QPoint) -> None:
        """Yığın değişince yeni yerine yumuşakça kayar."""
        if self._closing:
            return
        if self._move_anim is not None:
            self._move_anim.stop()
        self._move_anim = QPropertyAnimation(self, b"pos", self)
        self._move_anim.setStartValue(self.pos())
        self._move_anim.setEndValue(target)
        self._move_anim.setDuration(300)
        self._move_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._move_anim.start()

    def dismiss(self) -> None:
        """Sağa kayıp sönerek kapanır."""
        if self._closing:
            return
        self._closing = True
        self._timer_anim.stop()
        if self._move_anim is not None:
            self._move_anim.stop()

        kay = QPropertyAnimation(self, b"pos", self)
        kay.setStartValue(self.pos())
        kay.setEndValue(self.pos() + QPoint(SLIDE, 0))
        kay.setDuration(260)
        kay.setEasingCurve(QEasingCurve.Type.InCubic)
        son = QPropertyAnimation(self, b"fade", self)
        son.setStartValue(self._fade)
        son.setEndValue(0.0)
        son.setDuration(240)
        son.setEasingCurve(QEasingCurve.Type.InQuad)
        self._exit_group = QParallelAnimationGroup(self)
        self._exit_group.addAnimation(kay)
        self._exit_group.addAnimation(son)
        self._exit_group.finished.connect(self._finish)
        self._exit_group.start()
        # Yığındaki öbür kartlar hemen yer değiştirmeye başlasın.
        self.closed.emit(self)

    def _finish(self) -> None:
        self.hide()
        self.deleteLater()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.update()

    # --- fare --------------------------------------------------------------

    def _card_rect(self) -> QRectF:
        return QRectF(SHADOW, SHADOW, CARD_WIDTH, CARD_HEIGHT)

    def _close_rect(self) -> QRectF:
        kart = self._card_rect()
        return QRectF(kart.right() - 34, kart.top() + 10, 24, 24)

    def enterEvent(self, event) -> None:  # noqa: N802
        if self._timer_anim.state() == QPropertyAnimation.State.Running:
            self._timer_anim.pause()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802
        if self._timer_anim.state() == QPropertyAnimation.State.Paused:
            self._timer_anim.resume()
        if self._hover_close:
            self._hover_close = False
            self.setToolTip("")
            self.update()
        super().leaveEvent(event)

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        ustunde = self._close_rect().adjusted(-4, -4, 4, 4).contains(event.position())
        if ustunde != self._hover_close:
            self._hover_close = ustunde
            self.setToolTip(self._close_tip if ustunde else "")
            self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() != Qt.MouseButton.LeftButton or self._closing:
            return
        if self._close_rect().adjusted(-4, -4, 4, 4).contains(event.position()):
            self.dismiss()
        elif self._card_rect().contains(event.position()):
            self.activated.emit(self.data)
            self.dismiss()

    # --- çizim -------------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802
        p = PALETTES.get(self._mode, PALETTES["dark"])
        koyu = self._mode == "dark"
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        painter.setOpacity(max(0.0, min(1.0, self._fade)))

        kart = self._card_rect()

        # Gölge: dışa doğru açılan, gittikçe silikleşen katmanlar.
        katman = 8
        for i in range(katman, 0, -1):
            alfa = int((26 if koyu else 16) * (1 - i / (katman + 1)))
            renk = QColor(0, 0, 0, alfa)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(renk)
            genis = i * 1.6
            painter.drawRoundedRect(
                kart.adjusted(-genis, -genis + 3, genis, genis + 3), RADIUS + genis, RADIUS + genis
            )

        # Kart zemini ve ince çerçeve.
        yol = QPainterPath()
        yol.addRoundedRect(kart, RADIUS, RADIUS)
        painter.setBrush(QColor(p["surface"]))
        painter.setPen(QPen(QColor(p["border"]), 1))
        painter.drawPath(yol)

        # Kartın solunda simgenin renginde hafif bir ışıma.
        vurgu = QColor(self.data.color)
        isik = QLinearGradient(kart.left(), 0, kart.left() + 140, 0)
        vurgu.setAlpha(46 if koyu else 30)
        isik.setColorAt(0.0, vurgu)
        vurgu.setAlpha(0)
        isik.setColorAt(1.0, vurgu)
        painter.save()
        painter.setClipPath(yol)
        painter.fillRect(kart, isik)
        painter.restore()

        # Simge dairesi.
        merkez = QPointF(kart.left() + 18 + CIRCLE / 2, kart.center().y() - 2)
        self._paint_icon(painter, merkez)

        # Yazılar.
        sol = kart.left() + 18 + CIRCLE + 16
        sag = kart.right() - 40
        genislik = sag - sol

        ust = QFont(self.font())
        ust.setPixelSize(11)
        ust.setWeight(QFont.Weight.Bold)
        ust.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1.1)
        painter.setFont(ust)
        # Açık temada kademe renginin açık tonu (bronz, altın) zeminde
        # okunmuyordu; orada koyulaştırılmış ana renk.
        ust_renk = QColor(self.data.color2 or self.data.color) if koyu else QColor(self.data.color).darker(135)
        painter.setPen(ust_renk)
        painter.drawText(QRectF(sol, kart.top() + 16, genislik, 16),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                         QFontMetrics(ust).elidedText(self.data.eyebrow, Qt.TextElideMode.ElideRight, int(genislik)))

        baslik = QFont(self.font())
        baslik.setPixelSize(15)
        baslik.setWeight(QFont.Weight.Bold)
        painter.setFont(baslik)
        painter.setPen(QColor(p["text"]))
        painter.drawText(QRectF(sol, kart.top() + 34, genislik, 22),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                         QFontMetrics(baslik).elidedText(self.data.title, Qt.TextElideMode.ElideRight, int(genislik)))

        alt = QFont(self.font())
        alt.setPixelSize(12)
        painter.setFont(alt)
        painter.setPen(QColor(p["text_muted"]))
        painter.drawText(QRectF(sol, kart.top() + 57, genislik + 22, 20),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                         QFontMetrics(alt).elidedText(self.data.subtitle, Qt.TextElideMode.ElideRight, int(genislik + 22)))

        # Kapatma düğmesi.
        kapat = self._close_rect()
        if self._hover_close:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(p["surface_alt"]))
            painter.drawEllipse(kapat)
        painter.setPen(QPen(QColor(p["text"] if self._hover_close else p["text_muted"]), 1.7,
                            Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        m = 7.5
        painter.drawLine(QPointF(kapat.left() + m, kapat.top() + m), QPointF(kapat.right() - m, kapat.bottom() - m))
        painter.drawLine(QPointF(kapat.right() - m, kapat.top() + m), QPointF(kapat.left() + m, kapat.bottom() - m))

        # Kalan süre: alt kenarda, kartın içinde ince bir çizgi.
        painter.save()
        painter.setClipPath(yol)
        iz = QRectF(kart.left(), kart.bottom() - 3, kart.width(), 3)
        painter.fillRect(iz, QColor(p["surface_alt"]))
        dolu = QRectF(iz.left(), iz.top(), iz.width() * self._remaining, iz.height())
        cizgi = QLinearGradient(dolu.left(), 0, dolu.right(), 0)
        cizgi.setColorAt(0.0, QColor(self.data.color))
        cizgi.setColorAt(1.0, QColor(self.data.color2 or self.data.color))
        painter.fillRect(dolu, cizgi)
        painter.restore()
        painter.end()

    def _paint_icon(self, painter: QPainter, merkez: QPointF) -> None:
        r = CIRCLE / 2
        renk = QColor(self.data.color)
        renk2 = QColor(self.data.color2 or self.data.color)

        # Halka dalgası: dairenin çevresinden dışa açılıp sönüyor.
        if 0.0 < self._pulse < 1.0:
            halka = QColor(renk)
            halka.setAlphaF(0.55 * (1 - self._pulse))
            painter.setPen(QPen(halka, 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            yaricap = r + 4 + 16 * self._pulse
            painter.drawEllipse(merkez, yaricap, yaricap)

        # Rozetlerde dağılan küçük parıltılar.
        if self.data.kind == "badge" and 0.0 < self._pulse < 1.0:
            painter.setPen(Qt.PenStyle.NoPen)
            for i in range(8):
                aci = i * math.pi / 4 + math.pi / 8
                uzak = r + 6 + 22 * self._pulse
                nokta = QPointF(merkez.x() + math.cos(aci) * uzak, merkez.y() + math.sin(aci) * uzak)
                tane = QColor(renk2 if i % 2 else renk)
                tane.setAlphaF(max(0.0, 1 - self._pulse) * 0.9)
                painter.setBrush(tane)
                boy = 2.6 * (1 - 0.5 * self._pulse)
                painter.drawEllipse(nokta, boy, boy)

        olcek = max(0.0, bounce(self._pop))
        if self._art is not None:
            painter.save()
            painter.translate(merkez)
            painter.scale(olcek, olcek)
            kenar = MEDAL if self.data.medal else LOGO
            painter.drawPixmap(QPointF(-kenar / 2, -kenar / 2 - (2 if self.data.medal else 0)), self._art)
            if self.data.kind == "section":
                self._paint_check(painter, QPointF(kenar / 2 - 4, kenar / 2 - 4))
            painter.restore()
            return
        painter.save()
        painter.translate(merkez)
        painter.scale(olcek, olcek)

        # Dairenin arkasında yumuşak bir ışık.
        isik = QColor(renk)
        isik.setAlpha(60)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(isik)
        painter.drawEllipse(QPointF(0, 2), r + 3, r + 3)

        degrade = QLinearGradient(-r, -r, r, r)
        degrade.setColorAt(0.0, renk)
        degrade.setColorAt(1.0, renk2)
        painter.setBrush(degrade)
        painter.drawEllipse(QPointF(0, 0), r, r)

        # Üstte ince bir parlaklık.
        parlak = QColor(255, 255, 255, 38)
        painter.setBrush(parlak)
        painter.drawEllipse(QPointF(0, -r * 0.35), r * 0.72, r * 0.5)

        painter.drawPixmap(QPointF(-ICON / 2, -ICON / 2), self._icon_pix)

        # Bölüm kartında sağ altta küçük bir onay işareti.
        if self.data.kind == "section":
            self._paint_check(painter, QPointF(r * 0.72, r * 0.72))
        painter.restore()

    def _paint_check(self, painter: QPainter, konum: QPointF) -> None:
        """Yeşil daire içinde onay: bölüm tamamlandı."""
        k = 10.0
        painter.setBrush(QColor("#22C55E"))
        painter.setPen(QPen(QColor(PALETTES.get(self._mode, PALETTES["dark"])["surface"]), 2.5))
        painter.drawEllipse(konum, k, k)
        painter.setPen(QPen(QColor("#FFFFFF"), 2.2, Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.drawPolyline([
            konum + QPointF(-4.5, 0), konum + QPointF(-1.2, 3.3), konum + QPointF(4.8, -3.2),
        ])


class ToastManager:
    """Kartları yığar: en yeni en altta, yukarıdakiler boşalan yere iner.

    `anchor` çağrıldığında `(sağ kenar, alt kenar)` döndüren bir işlev:
    kartlar bu noktanın sol üstüne diziliyor (alt şeridin hemen üstü).
    En fazla üç kart görünüyor; fazlası sırada bekliyor.
    """

    def __init__(self, host: QWidget, anchor, close_tip) -> None:
        self._host = host
        self._anchor = anchor
        self._close_tip = close_tip
        self._mode = "dark"
        self._visible: list[Toast] = []
        self._queue: list[ToastData] = []
        # Girmek için sırasını bekleyenler (`ENTRY_GAP_MS` aralıkla).
        self._incoming: list[ToastData] = []
        self._gap = QTimer(host)
        self._gap.setSingleShot(True)
        self._gap.setInterval(ENTRY_GAP_MS)
        self._gap.timeout.connect(self._next_incoming)
        self.on_activated = None

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        for toast in self._visible:
            toast.set_mode(mode)

    def show(self, data: ToastData) -> None:
        self._incoming.append(data)
        if not self._gap.isActive():
            self._next_incoming()

    def _next_incoming(self) -> None:
        if not self._incoming:
            return
        self._gap.start()
        self._present(self._incoming.pop(0))

    def _present(self, data: ToastData) -> None:
        if len(self._visible) >= MAX_VISIBLE:
            self._queue.append(data)
            return
        toast = Toast(data, self._mode, self._close_tip(), self._host)
        toast.closed.connect(self._on_closed)
        toast.activated.connect(self._on_activated)
        # Yeni kart en alta geliyor; öncekiler bir basamak yukarı kayıyor.
        self._visible.insert(0, toast)
        self._restack(animate=True, skip=toast)
        toast.enter(self._slot(0))

    def _slot(self, index: int) -> QPoint:
        sag, alt = self._anchor()
        x = sag - CARD_WIDTH - SHADOW
        y = alt - (index + 1) * CARD_HEIGHT - index * GAP - SHADOW
        return QPoint(int(x), int(y))

    def _restack(self, animate: bool, skip: Toast | None = None) -> None:
        for index, toast in enumerate(self._visible):
            if toast is skip:
                continue
            hedef = self._slot(index)
            if animate:
                toast.slide_to(hedef)
            else:
                toast.move(hedef)
            toast.raise_()

    def reposition(self) -> None:
        """Pencere boyutu değişince kartlar köşeye yapışık kalsın."""
        self._restack(animate=False)

    def _on_closed(self, toast: Toast) -> None:
        if toast in self._visible:
            self._visible.remove(toast)
        self._restack(animate=True)
        if self._queue:
            # Sıradaki, yeni gelenlerin önüne geçiyor: o daha önce geldi.
            self._incoming.insert(0, self._queue.pop(0))
            QTimer.singleShot(260, lambda: None if self._gap.isActive() else self._next_incoming())

    def _on_activated(self, data: ToastData) -> None:
        if self.on_activated is not None:
            self.on_activated(data)

    def dismiss_all(self) -> None:
        self._queue.clear()
        self._incoming.clear()
        for toast in list(self._visible):
            toast.dismiss()
