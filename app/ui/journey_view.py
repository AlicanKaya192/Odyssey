"""Öğrenme yolu: modül kartları ve bölüm düğümleri.

İki katmanlı bir yapı var. Ana ekranda modüller kart hâlinde duruyor; bir
modüle girince o modülün bölümleri zigzag bir yol üzerinde sıralanıyor.

Neden iki katman: müfredat tamamlandığında 23 modül ve ~180 bölüm olacak.
Hepsini tek bir yola dizmek dakikalarca kaydırma demek. Modül kartları hem
düzeni koruyor hem de "nerede ne kadar ilerledim" sorusunu tek bakışta
cevaplıyor.

Bölümler sırayla açılıyor: bir bölüm, önündeki bölüm tamamlanmadan
açılmıyor. Tamamlanmış bölümlere istendiği zaman geri dönülebiliyor.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date

from PySide6.QtCore import Property, QEvent, QPointF, QRect, QRectF, QSize, Qt, QTimer, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
)
from PySide6.QtWidgets import (
    QGraphicsOpacityEffect,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..widgets.fade_stack import BACK, FORWARD, NONE, FadeStack
from ..widgets.lift_card import GlowCard, LiftSlot
from ..widgets.logo_mark import LogoMark
from ..widgets.progress_bar import ProgressBar
from ..widgets import motion
from ..widgets.path_node import PAD as NODE_PAD, NodeButton
from ..resources.logos import logo_key
from ..core.catalog import Catalog, Chapter, Track
from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..core.unlock import blocking_section
from ..resources.icons import icon, pixmap
from ..resources.theme.tokens import CONTENT_WIDTH, FONTS, PALETTES, RADIUS, SPACING
from ..widgets.common import ElidedText, StatBlock, horizontal_rule, section_label
from ..widgets.streak_flame import FlickerFlame, hero_flame_pixmap, next_tier, tier_for
from ..widgets.effects import apply_shadow, refresh_shadow

# Düğümlerin soldan uzaklıkları — yol bu değerlerle zigzag çiziyor. Dizi
# başa dönünce de kaydırma değişiyor (…120 → 30 → 120…); sonunda bir 30
# daha olsaydı iki halka üst üste gelip aradaki eğri düz bir çizgiye
# dönüyordu.
ZIGZAG = [30, 120, 170, 120]

# Halkaları birleştiren eğri: yüksekliği ve kalınlığı. Eğri bir dairenin
# ortasından çıkıp zikzakta bir sonrakinin ortasına kıvrılarak iniyor.
CONNECTOR_HEIGHT = 44
CONNECTOR_WIDTH = 4

# Her halkanın sabit genişliği. Metne göre değişince satırlar farklı
# genişlikte oluyor, ortalama da satır satır kayıyordu: bağlayıcı çizgiler
# dairelerin ortasına denk gelmiyordu. Sabit genişlik hepsini aynı hizaya
# getiriyor, uzun başlıklara da yer bırakıyor.
NODE_WIDTH = 300

# Zikzak bandının toplam genişliği: en büyük kaydırma + halka.
BAND_WIDTH = max(ZIGZAG) + NODE_WIDTH

# Kilitli bölümün halkasındaki kilit simgesinin boyu.
LOCK_ICON_SIZE = 26

# Henüz yazılmamış bölümlerin solukluğu. Okunacak kadar açık,
# yazılmışlarla karışmayacak kadar soluk.
PLANNED_OPACITY = 0.45

# Kilitli patikanın solukluğu. Okunuyor ama açılabilir olanlarla
# karışmıyor.
LOCKED_OPACITY = 0.5


# Prototip ölçüleri: sayfa sütunu (`.wrapc`) ve karşılama kartı (`.hero`).
PAGE_WIDTH = 1180
HERO_WIDTH = 1030


def scroll_page(widget: QWidget) -> QScrollArea:
    """İçeriği kaydırılabilir bir yüzeye koyar."""
    area = QScrollArea()
    area.setWidgetResizable(True)
    area.setFrameShape(QFrame.Shape.NoFrame)
    area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    area.setWidget(widget)
    return area


def centered_column(inner: QWidget, max_width: int = CONTENT_WIDTH) -> QWidget:
    """İçeriği sabit genişlikte bir sütuna alıp ekranın ortasına yerleştirir.

    Makette yol ve modül kartları uçlara yayılmıyor, ortada toplanıyor.
    Geniş ekranda içeriğin sağa sola dağılması hem dağınık duruyor hem de
    göz her satırda uzun bir yol kat ediyor.
    """
    holder = QWidget()
    row = QHBoxLayout(holder)
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(0)

    inner.setMaximumWidth(max_width)
    inner.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    # İç sütun en geniş hâline (max_width) kadar yeri alıyor, artan iki yana
    # gidiyor (prototip: `max-width` + ortalama). Önce 10'a 1 paylaşılıyordu ve
    # sütun geniş pencerede bile dar kalıyordu.
    row.addStretch(1)
    row.addWidget(inner, 1000)
    row.addStretch(1)
    return holder


# Karşılama kartında son gösterilen sayılar (oturum boyunca). Değer
# değişmediyse sayma yok; her girişte baştan saymak yorucu (ui-taslak B7).
_HERO_SHOWN: dict[str, float] = {}


class WaveEmoji(QWidget):
    """Selamın yanındaki el; ekran açılınca bir kez sallanır (C1)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(34, 34)
        self._t = 1.0

    def play(self) -> None:
        motion.animate(self, "t", 0.0, 1.0, self._set, 1000, "linear", delay=300)

    def _set(self, v: float) -> None:
        self._t = v
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        import math

        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        # ±14°, üç salınım, sönerek; bilek (sağ alt) ekseni.
        aci = 14 * math.sin(self._t * math.pi * 6) * (1 - self._t) if self._t < 1 else 0.0
        g.translate(self.width() * 0.7, self.height() * 0.8)
        g.rotate(aci)
        g.translate(-self.width() * 0.7, -self.height() * 0.8)
        f = QFont(self.font())
        f.setPixelSize(22)
        g.setFont(f)
        g.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "👋")


class HeroRing(QWidget):
    """Karşılama kartının sağındaki genel ilerleme ve sentorun hedefi (F2).

    Hedef açılış animasyonundakinin aynısı: iç içe siyah ve açık mor
    halkalar, dışta kazınmış noktalar, küçük merkez, üç ayaklı sehpa. Sehpa
    sentorun bastığı zemine iniyor. Yüzde hedefin üstünde, skor tabelası
    gibi. (İlk sürüm düz bir ilerleme halkasıydı, ikincisi halkanın içine
    konmuş bir hedefti; ikisi de hedef tahtasına benzemiyordu.)

    Kartın tam boyunda duruyor; hedefin merkezi ve zemin kart tarafından
    veriliyor (`set_scene`), sentorun oku bu merkeze bakıyor.
    """

    WIDTH = 150
    RADIUS = 44.0
    TEXT_TOP = 16.0
    TARGET_TOP = 82.0  # hedefin üst kenarı (yazıların altı)
    INK = "#0E0B1A"
    INK_FAR = "#2A2150"
    LIGHT = "#B5AFFF"
    INCISE = "#A9A2FF"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._value = 0.0
        self._text = ""
        self._caption = ""
        self._ground = 0.0
        self.setFixedWidth(self.WIDTH)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    @classmethod
    def center_y(cls) -> float:
        return cls.TARGET_TOP + cls.RADIUS

    def set_ground(self, ground: float) -> None:
        self._ground = ground
        self.update()

    def _get_value(self) -> float:
        return self._value

    def _set_value(self, v: float) -> None:
        self._value = v
        self.update()

    value = Property(float, _get_value, _set_value)

    def set_percent(self, percent: float) -> None:
        onceki = _HERO_SHOWN.get("ring", 0.0)
        _HERO_SHOWN["ring"] = percent
        motion.animate_property(self, "value", float(percent), 1200, "out", start=onceki)

    def set_texts(self, text: str, caption: str) -> None:
        self._text, self._caption = text, caption
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        import math as _m

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        cx, cy, r = self.width() / 2, self.center_y(), self.RADIUS

        # Yüzde (sayarak artıyor) ve açıklaması, hedefin üstünde.
        p.setPen(QColor("#FFFFFF"))
        f = QFont(self.font())
        f.setPixelSize(28)
        f.setWeight(QFont.Weight.Bold)
        p.setFont(f)
        metin = self._text
        if self._text:
            # Sayma animasyonu: gösterilen sayı değerin kendisi.
            metin = self._text.replace(str(round(_HERO_SHOWN.get("ring", 0))), str(round(self._value)), 1)
        p.drawText(QRectF(0, self.TEXT_TOP, self.width(), 34), Qt.AlignmentFlag.AlignCenter, metin)
        f.setPixelSize(12)
        f.setWeight(QFont.Weight.DemiBold)
        p.setFont(f)
        p.setPen(QColor(255, 255, 255, 215))
        p.drawText(QRectF(0, self.TEXT_TOP + 34, self.width(), 18), Qt.AlignmentFlag.AlignCenter, self._caption)

        # Üç ayaklı sehpa: arkadaki ayak bir ton açık.
        zemin = self._ground or (cy + r + 40)
        kalem = QPen(QColor(self.INK_FAR), 5.5)
        kalem.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(kalem)
        p.drawLine(QPointF(cx + 3, cy), QPointF(cx + 8, zemin))
        kalem.setColor(QColor(self.INK))
        p.setPen(kalem)
        p.drawLine(QPointF(cx, cy), QPointF(cx - 40, zemin))
        p.drawLine(QPointF(cx, cy), QPointF(cx + 36, zemin))

        # Halkalar: dıştan içe siyah / açık mor, merkezde siyah nokta.
        p.setPen(Qt.PenStyle.NoPen)
        merkez = QPointF(cx, cy)
        for oran, renk in ((1.0, self.INK), (.82, self.LIGHT), (.66, self.INK), (.48, self.LIGHT),
                           (.3, self.INK), (.14, self.LIGHT)):
            p.setBrush(QColor(renk))
            p.drawEllipse(merkez, r * oran, r * oran)
        p.setBrush(QColor(self.INK))
        p.drawEllipse(merkez, 2.8, 2.8)
        p.setBrush(QColor(self.INCISE))
        for k in range(30):
            a = k * 2 * _m.pi / 30
            p.drawEllipse(QPointF(cx + _m.cos(a) * r * .91, cy + _m.sin(a) * r * .91), 1.2, 1.2)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(self.INCISE), 1.0))
        for oran in (.58, .38):
            p.drawEllipse(merkez, r * oran, r * oran)


def stagger_cards(cards: list) -> None:
    """Kartlar saydamdan, 8 px aşağıdan, 40 ms arayla yayla gelir (prototip `.stg`/`sIn`)."""
    from ..widgets.pop_effect import enter

    baslaticilar = []
    for i, kart in enumerate(cards):
        yuva = kart.parentWidget()
        hedef = yuva if isinstance(yuva, LiftSlot) else kart
        baslaticilar.append(enter(hedef, 8, "spring", delay=min(i, 7) * 40,
                                  shadow_of_widget=kart, hold=True))
    return [b for b in baslaticilar if b]


class ShiftSlot(QWidget):
    """Düğmeyi taşıyan yuva: üzerine gelince düğme `shift` piksel sağa kayar."""

    def __init__(self, button: QPushButton, shift: int) -> None:
        super().__init__()
        self.setProperty("role", "bare")
        self._button = button
        self._shift = shift
        self._x = 0.0
        button.setParent(self)
        button.installEventFilter(self)
        self.fit()

    def fit(self) -> None:
        boy = self._button.sizeHint()
        self._button.resize(boy)
        self.setFixedSize(boy.width() + self._shift, boy.height())

    def _set_x(self, v: float) -> None:
        self._x = v
        self._button.move(round(v), 0)

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        if obj is self._button:
            if event.type() == QEvent.Type.Enter:
                motion.animate(self, "x", self._x, float(self._shift), self._set_x, "spring", "spring")
            elif event.type() == QEvent.Type.Leave:
                motion.animate(self, "x", self._x, 0.0, self._set_x, "spring", "spring")
        return False


class HeroCard(QFrame):
    """Üstteki karşılama kartı: kaldığın yer ve özet sayılar.

    Zemini kendisi çiziyor: çivit→mor geçiş ve üstünde yarı saydam
    daireler (Alican'ın verdiği örneğe göre). Renkler temadan değil
    logodan geliyor; koyu temanın açık vurgu rengiyle zemin pastel
    kalıyor, beyaz yazı zor okunuyordu.
    """

    resume = Signal()

    GRADIENT = ("#4F46E5", "#7C3AED")

    # Sentor: açılış animasyonundaki siyah figür. Ölçek kartın genişliğine
    # göre; yazılara yer kalmıyorsa figür çizilmiyor.
    FIGURE_INK = "#0E0B1A"
    FIGURE_SCALE_MAX = 0.6
    FIGURE_SCALE_MIN = 0.42
    TEXT_MIN_WIDTH = 480
    # Figürün kendi birimindeki genişliği (kuyruk ucu → ok ucu), ok ucunun
    # x'i ve okun yüksekliği: halkaya nişan alsın diye figür bunlarla konuyor.
    FIG_WIDTH, FIG_RIGHT, FIG_ARROW_Y = 373.0, 528.0, 211.8
    FIG_GAP = 14  # ok ucu ile hedef arası
    GROUND_MARGIN = 20  # toynakların ve sehpanın bastığı zemin, kartın altından

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._name = ""
        self._resume = ""
        self._streak = 0
        self._studied_today = False
        self._progress = 0
        self.setProperty("role", "hero")
        # Prototip: mor, aşağı düşen yumuşak ışıma (0 20px 50px rgba(99,70,229,.65)).
        apply_shadow(self, "dark", strong=True, blur=46, offset_y=18, radius=26,
                     color=(99, 70, 229, 150))
        self._drift = 0.0
        self._drift_timer = QTimer(self)
        self._drift_timer.setInterval(33)
        self._drift_timer.timeout.connect(self._tick_drift)
        motion.on_enabled_changed(lambda _on: self._sync_drift(), owner=self)

        # Solda selam, kaldığın yer, devam düğmesi ve sayılar; sağda halka.
        yatay = QHBoxLayout(self)
        yatay.setContentsMargins(36, 30, 40, 30)
        yatay.setSpacing(SPACING["lg"])
        sol = QWidget()
        sol.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        sol.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(sol)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING["sm"])
        yatay.addWidget(sol, 1)
        # Maskot: açılıştaki sentor halkaya (hedefe) nişan alıyor. Yeri boş
        # bir kutu, figürü kart kendisi çiziyor; genişliği kart genişliğine göre.
        from ..widgets import centaur as C
        self._C = C
        self._pose = C.aim_pose()
        self._figure_style = C.Style(
            fig=QColor(self.FIGURE_INK), far=QColor("#2A2150"), incise=QColor("#B3ACFF"),
            string=QColor(self.FIGURE_INK), arrow=QColor(self.FIGURE_INK), tip=QColor(self.FIGURE_INK))
        self._figure_scale = 0.0
        self._figure_draw = 1.0
        self._idle = 0.0
        self._scene_space = QWidget()
        self._scene_space.setProperty("role", "bare")
        self._scene_space.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._scene_space.setFixedWidth(0)
        yatay.addWidget(self._scene_space, 0)
        # Hedef yerleşimin dışında, kartın tam boyunda (sehpası zemine
        # iniyor); yerleşimde yalnızca yeri tutuluyor.
        self._ring_space = QWidget()
        self._ring_space.setProperty("role", "bare")
        self._ring_space.setFixedWidth(HeroRing.WIDTH)
        yatay.addWidget(self._ring_space, 0)
        self._ring = HeroRing(self)
        # Yer tutucu yerleşimle kayınca hedef de onunla gidiyor.
        self._ring_space.installEventFilter(self)

        self._title = QLabel()
        self._title.setStyleSheet(
            "color:#FFFFFF; font-size:26px; font-weight:700; background:transparent;"
            f"font-family: {FONTS['display']};"
        )
        # El sallama emojisi ayrı: ekran açılınca bir kez sallanıyor (C1).
        self._wave = WaveEmoji()
        baslik = QHBoxLayout()
        baslik.setSpacing(8)
        baslik.addWidget(self._title)
        baslik.addWidget(self._wave, 0, Qt.AlignmentFlag.AlignVCenter)
        baslik.addStretch(1)
        layout.addLayout(baslik)

        self._subtitle = QLabel()
        self._subtitle.setStyleSheet(
            "color:rgba(255,255,255,0.9); font-size:14.5px; font-weight:500;"
            " background:transparent;"
        )
        self._subtitle.setWordWrap(True)
        layout.addWidget(self._subtitle)

        # "Kaldığın yerden devam et": doğrudan sıradaki bölüme (F2).
        self._continue = QPushButton()
        self._continue.setCursor(Qt.CursorShape.PointingHandCursor)
        self._continue.setIcon(icon("play", "#FFFFFF", 18))
        self._continue.setStyleSheet(
            "QPushButton { color:#FFFFFF; font-weight:700; font-size:14px; padding:9px 16px 9px 12px;"
            " background: rgba(255,255,255,0.14); border:1px solid rgba(255,255,255,0.22);"
            " border-radius:14px; min-height:0px; }"
            " QPushButton:hover { background: rgba(255,255,255,0.24); }"
            " QPushButton:pressed { background: rgba(255,255,255,0.30); }"
        )
        self._continue.clicked.connect(self.resume)
        # Üzerine gelince yayla 3 px sağa kayar (prototip `.cont:hover`).
        # Düğme yerleşimin dışında bir yuvada; kayarken kart yeniden
        # yerleşmiyor.
        self._continue_slot = ShiftSlot(self._continue, 3)
        layout.addSpacing(SPACING["sm"])
        layout.addWidget(self._continue_slot, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addSpacing(SPACING["sm"])

        stats = QHBoxLayout()
        stats.setSpacing(30)
        self._stats = {
            key: StatBlock("0", "", inverse=True)
            for key in ("sections", "exercises", "streak")
        }
        for block in self._stats.values():
            # Sayılar etiketleriyle birlikte sola yaslı (örnekteki gibi).
            block.set_centered(False)
            block.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            block.setStyleSheet("background: transparent;")
            stats.addWidget(block)
        stats.addStretch(1)
        layout.addLayout(stats)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        self._wave.play()
        self._sync_drift()
        self._fit_figure()
        # Oturumdaki ilk gösterimde sentor yayını geriyor.
        if not _HERO_SHOWN.get("drawn") and motion.enabled():
            _HERO_SHOWN["drawn"] = 1.0
            self._figure_draw = 0.62
            motion.animate(self, "draw", 0.62, 1.0, self._set_figure_draw, 900, "out", delay=380)

    # Boşta döngü (sn): nişan alıp bekliyor, yayı gevşetip indiriyor,
    # başını çevirip arkasına bakıyor, dönüp yayı yeniden kaldırıp geriyor.
    IDLE_CYCLE = 14.0

    def _idle_pose(self, t: float):
        """Karttaki sentorun `t` anındaki duruşu (boşta döngü)."""
        import math as _m

        def ara(a: float, b: float) -> float:
            return self._C.smoothstep((k - a) / (b - a))

        k = t % self.IDLE_CYCLE
        grip = self._C.GRIP_DRAW
        # Gerginlik: kirişi yavaşça bırakıyor, el tutamayınca kiriş yerine
        # dönüyor; kaldırınca el kirişi yakalayıp yeniden geriyor.
        if k < 6.5:
            draw = 1.0
        elif k < 7.0:
            draw = 1 - (1 - grip) * ara(6.5, 6.9) - grip * ara(6.9, 7.0)
        elif k < 10.8:
            draw = 0.0
        else:
            draw = grip * ara(10.8, 10.88) + (1 - grip) * ara(10.9, 11.7)
        hand_rest = ara(6.9, 7.5) - ara(10.2, 10.8)
        bow_lower = 30 * (ara(7.0, 7.7) - ara(10.0, 10.7))
        head_turn = ara(7.9, 8.15) - ara(9.5, 9.75)
        return replace(
            self._pose,
            draw=min(draw, self._figure_draw),
            hand_rest=hand_rest,
            bow_lower=bow_lower,
            head_turn=head_turn,
            head_tilt=-4 * head_turn,
            lean=0.7 * _m.sin(t * 2 * _m.pi / 4.2),
            tail=4 * _m.sin(t * 2 * _m.pi / 3.1) + 2 + 6 * _m.sin(_m.pi * ara(8.6, 9.4)),
        )

    def _set_figure_draw(self, v: float) -> None:
        self._figure_draw = v
        self.update()

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._fit_figure()

    def _fit_figure(self) -> None:
        """Sentorun ölçeği ve yeri: yazılara `TEXT_MIN_WIDTH` kalacak kadar."""
        margins = self.layout().contentsMargins()
        bosluk = self.layout().spacing()
        kalan = (self.width() - margins.left() - margins.right() - HeroRing.WIDTH
                 - 2 * bosluk - self.TEXT_MIN_WIDTH - self.FIG_GAP)
        # Ok hedefin ortasına bakıyor, toynaklar ve sehpa aynı zeminde.
        zemin = self.height() - self.GROUND_MARGIN
        ayak = (zemin - HeroRing.center_y()) / (self._C.GROUND - self.FIG_ARROW_Y)
        olcek = min(self.FIGURE_SCALE_MAX, kalan / self.FIG_WIDTH, ayak)
        if olcek < self.FIGURE_SCALE_MIN:
            olcek = 0.0
        self._figure_scale = olcek
        genislik = round(self.FIG_WIDTH * olcek + self.FIG_GAP) if olcek else 0
        if self._scene_space.width() != genislik:
            self._scene_space.setFixedWidth(genislik)
        self._place_ring()

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        if obj is self._ring_space and event.type() in (QEvent.Type.Move, QEvent.Type.Resize):
            self._place_ring()
        elif obj is self._stats.get("streak") and event.type() == QEvent.Type.Enter:
            obj.setToolTip(self._streak_tooltip())
        return False

    def _place_ring(self) -> None:
        yer = self._ring_space.geometry()
        self._ring.setGeometry(yer.x(), 0, HeroRing.WIDTH, self.height())
        self._ring.set_ground(self.height() - self.GROUND_MARGIN)

    def hideEvent(self, event) -> None:  # noqa: N802
        super().hideEvent(event)
        self._drift_timer.stop()

    def _sync_drift(self) -> None:
        """Daireler sürekli kayar (C1); görünmezken durur.

        Prototipte 14 s'lik döngü ve 36 px'lik kayma göze çarpmıyordu
        (Alican: "kişinin gözüne çarpsın"); 5 s ve daha geniş kayma.
        """
        if motion.enabled() and self.isVisible():
            if not self._drift_timer.isActive():
                self._drift_timer.start()
        else:
            self._drift_timer.stop()

    def _tick_drift(self) -> None:
        pencere = self.window()
        if pencere is not None and not pencere.isActiveWindow():
            return
        # Bir gidiş 5 s; ikinci daire kendi fazında (7 s) — hep birlikte değil.
        self._drift = (self._drift + 33 / 5000) % 2.0
        self._drift2 = (getattr(self, '_drift2', 0.0) + 33 / 7000) % 2.0
        self._idle += 0.033
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802 (Qt adlandırması)
        """Geçişli zemin ve dekoratif daireler, kartın köşelerine kırpılmış."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect())
        shape = QPainterPath()
        shape.addRoundedRect(rect, RADIUS["xl"], RADIUS["xl"])
        painter.setClipPath(shape)

        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        gradient.setColorAt(0.0, QColor(self.GRADIENT[0]))
        gradient.setColorAt(1.0, QColor(self.GRADIENT[1]))
        painter.fillPath(shape, gradient)

        painter.setPen(Qt.PenStyle.NoPen)
        w, h = rect.width(), rect.height()
        # Yavaş kayma: 0 → 1 → 0 gidip gelen yumuşak bir faz (C1).
        import math as _m
        faz = (1 - _m.cos(self._drift * _m.pi)) / 2
        faz2 = (1 - _m.cos(getattr(self, "_drift2", 0.0) * _m.pi)) / 2
        dx, dy = -70 * faz, 40 * faz
        dx2, dy2 = 60 * faz2, -34 * faz2
        # Sağda kartın dışına taşan büyük daire, solda altta küçüğü.
        for cx, cy, r, alpha in (
            (w - 40 + dx, h * 0.42 + dy, h * 0.95 * (1 + 0.10 * faz), 20),
            (w - 150 + dx2, h + 30 + dy2, h * 0.55 * (1 + 0.08 * faz2), 12),
            (30 - dx2 * 0.6, h + 10 + dy * 0.4, h * 0.42, 14),
        ):
            color = QColor(255, 255, 255, alpha)
            painter.setBrush(color)
            painter.drawEllipse(QPointF(cx, cy), r, r)

        # Sentor, okun ucu halkanın ortasına bakacak şekilde. Boşta nefes
        # alıyor (üst gövde çok hafif), kuyruğu kendi ritminde sallanıyor.
        olcek = self._figure_scale
        if olcek > 0:
            halka = self._ring.geometry()
            hedef_sol = halka.x() + HeroRing.WIDTH / 2 - HeroRing.RADIUS
            x = hedef_sol - self.FIG_GAP - self.FIG_RIGHT * olcek
            y = HeroRing.center_y() - self.FIG_ARROW_Y * olcek
            poz = self._idle_pose(self._idle)
            painter.save()
            painter.translate(x, y)
            painter.scale(olcek, olcek)
            self._C.draw_centaur(painter, poz, self._figure_style)
            painter.restore()

    def update_stats(
        self,
        name: str,
        resume_text: str,
        sections: int,
        total_sections: int,
        exercises: int,
        total_exercises: int,
        streak: int,
        progress: int,
        studied_today: bool = False,
    ) -> None:
        """Şeritteki dört sayıyı yeniler.

        Bölüm ve alıştırma **kesir** olarak yazılıyor. Tek başına "13"
        ilerlemeyi anlatmıyor: on üç alıştırmanın kaçta kaçı olduğu
        bilinmeden o sayı iyi mi kötü mü belli olmuyor.
        """
        # Ad ve "kaldığın yer" metni saklanıyor: dil değişince ikisi de
        # yeniden üretilecek. Eskiden yalnızca burada yazılıyordu ve
        # `retranslate` onlara dokunmadığı için dil değiştiğinde selamlama
        # eski dilde kalıyordu.
        self._name = name
        self._resume = resume_text
        self._render_greeting()

        # Sayılar son gösterilen değerden yeniye sayıyor (B7).
        self._totals = (total_sections, total_exercises)
        for anahtar, deger, fmt in (
            ("sections", sections, lambda v: str(round(v))),
            ("exercises", exercises, lambda v: str(round(v))),
            ("streak", streak, lambda v: str(round(v))),
        ):
            onceki = _HERO_SHOWN.get(anahtar, deger)
            _HERO_SHOWN[anahtar] = deger
            motion.count_up(self._stats[anahtar]._value, onceki, deger, fmt)
        self._ring.set_percent(progress)
        self._progress = progress
        self._streak = streak
        self._studied_today = studied_today
        self.retranslate()

    def set_mode(self, mode: str) -> None:
        refresh_shadow(self, mode, strong=True)

    def set_resume(self, text: str) -> None:
        """Kaldığın yer satırı. Metni çağıran üretiyor, dil ona bağlı."""
        self._resume = text
        self._subtitle.setText(text)

    def _render_greeting(self) -> None:
        selam = (
            self._language.t("home.welcome_named", name=self._name)
            if self._name
            else self._language.t("home.welcome")
        )
        self._title.setText(selam)
        self._subtitle.setText(self._resume)

    def _streak_tooltip(self) -> str:
        """Alevin ipucu: serinin ne zaman biteceği (geri sayım), şu anki ve
        sonraki aşama, bir günün neyle sayıldığı.

        Fare üstüne geldiği anda yeniden hesaplanıyor; saat hep güncel.
        Geri sayım önce yoktu (Alican'a gelen geri bildirim, 29 Eylül).
        """
        from datetime import datetime, timedelta

        t = self._language.t
        simdi = datetime.now()
        gece = datetime.combine(simdi.date() + timedelta(days=1), datetime.min.time())

        def sure(bitis: datetime) -> str:
            dakika = max(1, int((bitis - simdi).total_seconds() // 60))
            saat, dakika = divmod(dakika, 60)
            if saat >= 24:
                return t("streak.dh", d=saat // 24, h=saat % 24)
            return t("streak.hm", h=saat, m=dakika) if saat else t("streak.m", m=dakika)

        from ..widgets import tips

        # Başlık: kaç gün ve aşama; durum: ne zaman biter (renkli); altta
        # sonraki aşama ve bir günün neyle sayıldığı.
        tier = tier_for(self._streak)
        if self._streak <= 0:
            baslik = t("streak.title_none")
            durum, ton = t("streak.start"), "accent"
        else:
            ad = t(f"streak.tier_{tier.key}") if tier else ""
            baslik = t("streak.title", days=self._streak, tier=ad)
            if self._studied_today:
                durum, ton = t("streak.safe", time=sure(gece + timedelta(days=1))), "success"
            else:
                durum, ton = t("streak.ends_in", time=sure(gece)), "warning"
        govde = []
        sonraki = next_tier(self._streak)
        if sonraki is not None:
            govde.append(t("streak.next", days=sonraki.min_days - self._streak,
                           name=t(f"streak.tier_{sonraki.key}")))
        govde.append(t("streak.counts"))
        return tips.rich(baslik, "\n\n".join(govde), durum, ton)

    def _render_flame(self) -> None:
        """Serinin alevi ve ipucu (bkz. `_streak_tooltip`)."""
        # Alev titreyen bir widget (C12); StatBlock'un düz simge yeri gizli.
        blok = self._stats["streak"]
        blok.set_icon(None, self._streak_tooltip())
        if not getattr(self, "_streak_filter", False):
            # İpucu fare üstüne gelince tazeleniyor (geri sayım).
            self._streak_filter = True
            blok.installEventFilter(self)
        if not hasattr(self, "_flame"):
            self._flame = FlickerFlame()
            blok._icon.parentWidget().layout()  # noqa: B018 — düzen var mı
            satir = blok.layout().itemAt(1).layout()
            # Prototip: alev "günlük seri" yazısının önünde.
            satir.insertWidget(0, self._flame, 0, Qt.AlignmentFlag.AlignVCenter)
        # Seri sıfır olsa da alev hep hareketli (Alican).
        self._flame.set_pixmap(hero_flame_pixmap(max(2.0, self.devicePixelRatioF() or 1.0)),
                               alive=True)

    def retranslate(self) -> None:
        self._render_greeting()
        toplam = getattr(self, "_totals", (0, 0))
        self._stats["sections"].set_label(self._language.t("home.stat_sections", total=toplam[0]))
        self._stats["exercises"].set_label(self._language.t("home.stat_exercises", total=toplam[1]))
        self._stats["streak"].set_label(self._language.t("home.stat_streak"))
        # Yüzde işareti dile göre: Türkçede önde (%40), İngilizcede sonda (40%).
        self._ring.set_texts(self._language.t("home.percent", value=self._progress),
                             self._language.t("home.stat_progress"))
        self._continue.setText("  " + self._language.t("home.continue"))
        self._continue_slot.fit()
        self._render_flame()


class ModuleCard(GlowCard):
    """Tek bir modülü temsil eden tıklanabilir kart.

    Düğme yerine çerçeve: genel `QPushButton` stil kuralındaki `min-height`,
    Python'dan verilen en küçük yüksekliği eziyor ve kart eziliyordu.
    """

    clicked = Signal()

    def __init__(
        self,
        chapter: Chapter,
        language: LanguageManager,
        mode: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._chapter = chapter
        self._language = language
        self.set_accent(chapter.color)
        self.set_card_mode(mode)
        self.setProperty("variant", "module")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        apply_shadow(self, mode)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"])
        layout.setSpacing(SPACING["sm"])

        header = QHBoxLayout()
        header.setSpacing(SPACING["sm"])

        self._icon = LogoMark(logo_key(chapter.icon, chapter.id), chapter.color, 40)
        self.hovered.connect(self._icon.set_hovered)
        header.addWidget(self._icon, 0, Qt.AlignmentFlag.AlignVCenter)

        self._title = QLabel()
        self._title.setProperty("role", "subtitle")
        self._title.setWordWrap(True)
        header.addWidget(self._title, 1)
        layout.addLayout(header)

        self._description = QLabel()
        self._description.setProperty("role", "muted")
        self._description.setWordWrap(True)
        layout.addWidget(self._description)
        layout.addStretch(1)

        self._bar = ProgressBar(f"module:{chapter.id}")
        self._bar.set_color(chapter.color)
        self._bar.set_mode(mode)
        layout.addWidget(self._bar)

        self._caption = QLabel()
        self._caption.setProperty("role", "muted")
        layout.addWidget(self._caption)

    @property
    def chapter_id(self) -> str:
        return self._chapter.id

    def update_progress(self, completed: int, total: int) -> None:
        percent = round(completed * 100 / total) if total else 0
        self._bar.set_percent(percent)
        self._caption.setText(
            self._language.t("module.progress", done=completed, total=total, percent=percent)
        )

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def set_mode(self, mode: str) -> None:
        refresh_shadow(self, mode)
        self.set_card_mode(mode)
        self._bar.set_mode(mode)

    def retranslate(self) -> None:
        self._title.setText(self._language.pick(self._chapter.title))
        self._description.setText(self._language.pick(self._chapter.description))


# Patika kartı başlığının denenen yazı boyutları; ilki QSS'teki boyut.
TITLE_SIZES = (17, 16, 15, 14, 13)
TITLE_LINES = 2

# Kilitli patikada logonun köşesindeki kilit rozetinin çapı.
LOCK_BADGE = 22


class TrackCard(GlowCard):
    """Bir öğrenme patikasını temsil eden kart (prototipteki `.tcard`).

    Üstte logo (50 px) ve yanında başlık ile "17 bölüm" alt satırı; altında
    iki satırlık açıklama; en altta ilerleme çubuğu ve "1 / 17 bölüm · %6".
    Kilitli patikada kart kesik çerçeveli ve soluk zeminli, logo gri, sağ üstte
    zeminli bir kilit kutusu ve en altta bilgi simgeli ön koşul satırı var.
    """

    clicked = Signal()

    PAD = 20
    LOGO = 50

    def __init__(self, track: Track, language: LanguageManager, mode: str,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent, interactive=not track.locked)
        self._track = track
        self._language = language
        self._completed = 0
        self._total = 0
        self._mode = mode
        self._radius = 20
        self.set_accent(track.color)
        self.set_card_mode(mode)
        self.setProperty("variant", "track")
        self.setProperty("locked", "true" if track.locked else "false")
        # Bütün kartlar aynı boyda: genişlik ızgaradan, yükseklik `_fix_height`.
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        if not track.locked:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            apply_shadow(self, mode, radius=20)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(self.PAD, self.PAD, self.PAD, self.PAD)
        layout.setSpacing(12)

        header = QHBoxLayout()
        header.setSpacing(14)
        self._icon = LogoMark(logo_key(track.icon, track.id), track.color, self.LOGO, locked=track.locked)
        self.hovered.connect(self._icon.set_hovered)
        header.addWidget(self._icon, 0, Qt.AlignmentFlag.AlignVCenter)
        baslik = QVBoxLayout()
        baslik.setSpacing(1)
        baslik.addStretch(1)
        self._title = QLabel()
        self._title.setWordWrap(True)
        self._title.setProperty("role", "track-title")
        baslik.addWidget(self._title)
        self._sub = QLabel()
        self._sub.setProperty("role", "track-sub")
        baslik.addWidget(self._sub)
        baslik.addStretch(1)
        header.addLayout(baslik, 1)
        self._lock: QLabel | None = None
        if track.locked:
            # Tıklanınca sallanıyor: neden açılmadığını anlatıyor (C2).
            # Logonun sağ alt köşesinde küçük rozet (kilitli madalyalar gibi),
            # yerleşimin dışında. Önce başlık satırının sağında 44 piksel
            # tutuyordu ve dar kartta başlık sığmıyordu ("Algoritmal").
            self._lock = QLabel(self)
            self._lock.setProperty("role", "lock-chip")
            self._lock.setFixedSize(LOCK_BADGE, LOCK_BADGE)
            self._lock.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._lock.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        layout.addLayout(header)

        self._description = ElidedText(lines=2)
        self._description.setProperty("role", "track-desc")
        layout.addWidget(self._description)
        layout.addStretch(1)

        # Alt blok: açıkta çubuk + "1 / 17 bölüm · %6", kilitlide ön koşul satırı.
        self._foot = QWidget()
        self._foot.setProperty("role", "bare")
        alt = QVBoxLayout(self._foot)
        alt.setContentsMargins(0, 0, 0, 0)
        alt.setSpacing(8)
        self._bar = ProgressBar(f"track:{track.id}")
        self._bar.set_color(track.color)
        self._bar.set_mode(mode)
        alt.addWidget(self._bar)
        meta = QHBoxLayout()
        meta.setSpacing(8)
        self._meta_left = QLabel()
        self._meta_left.setProperty("role", "track-meta")
        self._meta_right = QLabel()
        self._meta_right.setProperty("role", "track-meta")
        meta.addWidget(self._meta_left)
        meta.addStretch(1)
        meta.addWidget(self._meta_right)
        alt.addLayout(meta)
        self._why_row = QWidget()
        self._why_row.setProperty("role", "bare")
        why = QHBoxLayout(self._why_row)
        why.setContentsMargins(0, 0, 0, 0)
        why.setSpacing(6)
        self._why_icon = QLabel()
        self._why_icon.setFixedWidth(16)
        why.addWidget(self._why_icon, 0, Qt.AlignmentFlag.AlignTop)
        self._caption = ElidedText(lines=2)
        self._caption.setProperty("role", "track-why")
        why.addWidget(self._caption, 1)
        alt.addWidget(self._why_row)
        for parca in (self._bar,):
            parca.setVisible(not track.locked)
        self._meta_left.setVisible(not track.locked)
        self._meta_right.setVisible(not track.locked)
        self._why_row.setVisible(track.locked)
        layout.addWidget(self._foot)
        self._paint_icons()

    def _paint_icons(self) -> None:
        p = PALETTES.get(self._mode, PALETTES["dark"])
        if self._lock is not None:
            self._lock.setPixmap(pixmap("lock", p["text_muted"], 12))
        self._why_icon.setPixmap(pixmap("info", p["text_muted"], 14))

    def showEvent(self, event) -> None:  # noqa: N802 (Qt adlandırması)
        # Ölçü ekrana gelince alınıyor: kurulurken yazı tipi henüz stil
        # dosyasından gelmemiş olabiliyor.
        super().showEvent(event)
        self._fix_height()
        QTimer.singleShot(0, self._place_lock)

    def changeEvent(self, event) -> None:  # noqa: N802
        super().changeEvent(event)
        if event.type() == event.Type.StyleChange and self.isVisible():
            self._fix_height()

    def _fix_height(self) -> None:
        """Kart yüksekliği: en kalabalık hâlin sığacağı sabit boy (hepsi aynı)."""
        for label in (self._description, self._caption):
            label.ensurePolished()
            label._reflow()
        self._meta_left.ensurePolished()
        self._title.ensurePolished()
        ust = self.LOGO + 12
        alt_acik = self._bar.sizeHint().height() + 8 + self._meta_left.sizeHint().height()
        alt_kilitli = self._caption.height()
        height = (2 * self.PAD + ust + 12 + self._description.height() + 12
                  + max(alt_acik, alt_kilitli) + 4)
        self.setFixedHeight(height)

    @property
    def track_id(self) -> str:
        return self._track.id

    def update_progress(self, completed: int, total: int) -> None:
        """Patikanın altındaki modüllerin toplam ilerlemesi."""
        self._completed = completed
        self._total = total
        percent = round(completed * 100 / total) if total else 0
        self._bar.set_percent(percent)
        self._render_meta()

    def _render_meta(self) -> None:
        percent = round(self._completed * 100 / self._total) if self._total else 0
        p = PALETTES.get(self._mode, PALETTES["dark"])
        self._meta_left.setText(
            f"<span style='color:{p['text']};font-weight:700'>{self._completed}</span>"
            + self._language.t("track.meta_sections", total=self._total))
        self._meta_right.setText(self._language.t("home.percent", value=percent))

    def _shake_lock(self) -> None:
        """Kilit ±4 px üç kez sallanır, alttaki ön koşul yazısı bir an vurgulanır."""
        from ..resources.theme.motion import DISTANCE

        kilit = self._lock
        if kilit is None:
            return
        genlik = DISTANCE["shake"]

        def adim(t: float) -> None:
            import math
            x = round(genlik * math.sin(t * math.pi * 6) * (1 - t))
            kilit.setContentsMargins(x, 0, -x, 0)

        motion.animate(kilit, "shake", 0.0, 1.0, adim, 300, "linear",
                       on_done=lambda: kilit.setContentsMargins(0, 0, 0, 0))
        vurgu = PALETTES.get(self._mode, PALETTES["dark"])["accent"]
        self._caption.setStyleSheet(f"color: {vurgu};")
        QTimer.singleShot(1100, lambda: self._caption.setStyleSheet(""))

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if self._track.locked:
            if event.button() == Qt.MouseButton.LeftButton:
                self._shake_lock()
            return
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.set_card_mode(mode)
        self._bar.set_mode(mode)
        self._paint_icons()
        self._render_meta()
        if not self._track.locked:
            refresh_shadow(self, mode)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._fit_title()
        self._place_lock()

    def _place_lock(self) -> None:
        """Kilit rozetini logonun sağ alt köşesine, biraz dışarı taşırarak koyar."""
        if self._lock is None:
            return
        logo = self._icon.geometry()
        if logo.isEmpty():
            # Yerleşim henüz kurulmadı; logo kenar boşluğunda, dikeyde ortada.
            logo = self._icon.rect().translated(self.PAD, self.PAD)
        self._lock.move(logo.right() - LOCK_BADGE + 6, logo.bottom() - LOCK_BADGE + 6)
        self._lock.raise_()

    def _fit_title(self) -> None:
        """Başlık yazısını kartın genişliğine sığdırır; kartın boyu değişmez.

        Kartlar pencereyle ölçeklenince dar kalan başlık kırpılıyordu:
        "Algoritmalar" "Algoritmal", "Kütüphaneler" "Kütüphane" oluyordu,
        "GenAI ve Prompt Eng." üç satıra taşıyordu (Alican bildirdi). Yazı
        her kelime tek parça ve en fazla iki satır olacak kadar küçülüyor.
        """
        metin = self._title.text()
        if not metin:
            return
        # Logonun gerçek sağ kenarından: logo bileşeni çizdiği 50 pikselden
        # geniş, sabitten hesaplanınca oda 14 piksel fazla çıkıyordu.
        logo = self._icon.geometry()
        sol = logo.right() + 1 if not logo.isEmpty() else self.PAD + self._icon.sizeHint().width()
        # Son 8 piksel pay: etiketin kendi satır kırması ölçümden birkaç
        # piksel dar davranıyor ("System Design" sığar görünüp bölünüyordu).
        oda = self.width() - self.PAD - sol - 14 - 8
        if oda <= 0:
            return
        self._title.ensurePolished()
        font = QFont(self._title.font())
        secilen = TITLE_SIZES[-1]
        for boyut in TITLE_SIZES:
            font.setPixelSize(boyut)
            olcu = QFontMetrics(font)
            satir, satirlar = "", 1
            sigdi = True
            for kelime in metin.split():
                if olcu.horizontalAdvance(kelime) > oda:
                    sigdi = False
                    break
                aday = f"{satir} {kelime}".strip()
                if olcu.horizontalAdvance(aday) > oda:
                    satirlar += 1
                    satir = kelime
                else:
                    satir = aday
            if sigdi and satirlar <= TITLE_LINES:
                secilen = boyut
                break
        stil = "" if secilen == TITLE_SIZES[0] else f"font-size: {secilen}px;"
        if self._title.styleSheet() != stil:
            self._title.setStyleSheet(stil)

    def retranslate(self) -> None:
        self._title.setText(self._language.pick(self._track.title))
        self._fit_title()
        self._description.set_full_text(self._language.pick(self._track.description))
        if self._track.locked:
            self._sub.setText("")
            self._caption.set_full_text(
                self._language.t("track.prerequisite") if self._track.prerequisite
                else self._language.t("track.locked"))
        else:
            if self._track.chapter_tabs and len(self._track.chapters) > 1:
                kisa = [self._language.pick(c.raw.get("short"), "") for c in self._track.chapters]
                self._sub.setText(" · ".join(k for k in kisa if k))
            else:
                # Bölüm sayısı kartın altında ("1 / 17 bölüm") zaten yazıyor.
                self._sub.setText("")
        self._sub.setVisible(bool(self._sub.text()))
        self._render_meta()


class TracksView(QWidget):
    """Patika kartlarının 2x2 dizildiği ana ekran."""

    track_opened = Signal(str)
    resume_requested = Signal()

    def __init__(
        self,
        catalog: Catalog,
        language: LanguageManager,
        store: ProgressStore,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._catalog = catalog
        self._language = language
        self._store = store
        self._mode = "light"
        self._cards: list[TrackCard] = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        column = QWidget()
        self._page_layout = QVBoxLayout(column)
        self._page_layout.setContentsMargins(
            SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xxl"]
        )
        self._page_layout.setSpacing(SPACING["lg"])

        self._hero = HeroCard(language)
        # Prototip: karşılama kartı en fazla 1030 px, ortada.
        self._hero.setMaximumWidth(HERO_WIDTH)
        self._hero.resume.connect(self.resume_requested)
        hero_satir = QHBoxLayout()
        hero_satir.addStretch(1)
        hero_satir.addWidget(self._hero, 1000)
        hero_satir.addStretch(1)
        self._page_layout.addLayout(hero_satir)
        self._page_layout.addSpacing(14)

        self._label = section_label("")
        self._page_layout.addWidget(self._label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self._grid = QGridLayout()
        self._grid.setSpacing(SPACING["md"])
        self._page_layout.addLayout(self._grid)
        self._page_layout.addStretch(1)

        # Sütun karşılama kartı genişliğinde: patika kartları kartla aynı
        # kenarlardan başlayıp bitiyor (Alican: sayfa hizalı olsun).
        outer.addWidget(scroll_page(centered_column(column, max_width=HERO_WIDTH + 2 * SPACING["xl"])))
        self._build_cards()

    def _build_cards(self) -> None:
        for index, track in enumerate(self._catalog.tracks):
            card = TrackCard(track, self._language, self._mode)
            card.clicked.connect(lambda t=track.id: self.track_opened.emit(t))
            self._grid.addWidget(LiftSlot(card), index // 4, index % 4)
            self._cards.append(card)
        self._entered = False
        # Sütunlar eşit paylaşılıyor; yoksa her sütun içindeki en geniş
        # kartın isteğine göre büyüyordu (233 ile 247 piksel arası).
        for column in range(4):
            self._grid.setColumnStretch(column, 1)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        # Oturumdaki ilk gösterimde prototipteki gibi: karşılama kartı ve
        # başlık 16 px aşağıdan (ekranın `pgIn`'i), kartlar sırayla (`sIn`).
        if not self._entered:
            self._entered = True
            from ..widgets.pop_effect import enter
            hepsi = [enter(self._hero, 16, "spring", hold=True),
                     enter(self._label, 16, "spring", hold=True)]
            hepsi += stagger_cards(self._cards)
            hepsi = [b for b in hepsi if b]
            # İlk çizim bittikten sonra başlasın (bkz. `enter`, `hold`).
            QTimer.singleShot(0, self, lambda: QTimer.singleShot(
                16, self, lambda: [b() for b in hepsi]))

    def _chapter_progress(self, chapter) -> tuple[int, int]:
        """Bir modülde kaç bölüm tamamlandı, kaç bölüm var."""
        biten = 0
        for section in chapter.sections:
            state = self._store.section_state(
                chapter.id, section.id, section.exercises
            )
            if state.status(
                section.requires_quiz, section.requires_exercises
            ) == "completed":
                biten += 1
        return biten, len(chapter.sections)

    def refresh(self) -> None:
        toplam = 0
        biten = 0

        for card in self._cards:
            track = self._catalog.track(card.track_id)
            if track is None:
                continue
            t_biten = t_toplam = 0
            for chapter in track.chapters:
                b, s = self._chapter_progress(chapter)
                t_biten += b
                t_toplam += s
            card.update_progress(t_biten, t_toplam)
            biten += t_biten
            toplam += t_toplam

        self._hero.update_stats(
            name=self._store.profile().get("first_name", ""),
            resume_text=self._resume_text(),
            sections=biten,
            total_sections=toplam,
            exercises=self._store.solved_exercise_count(),
            total_exercises=sum(
                len(section.exercises) for section in self._catalog.all_sections
            ),
            streak=self._store.streak(),
            progress=round(biten * 100 / toplam) if toplam else 0,
            studied_today=self._store.last_study_day() == date.today(),
        )
        self.retranslate()

    def resume_target(self) -> tuple[str, str] | None:
        """"Devam et" düğmesinin açacağı bölüm: son ziyaret ya da ilk bölüm."""
        last = self._store.last_visited()
        if last is not None and self._catalog.section(*last) is not None:
            return last
        sections = self._catalog.all_sections
        return (sections[0].chapter_id, sections[0].id) if sections else None

    def _resume_text(self) -> str:
        """Kaldığın yer. Modül ekranındakiyle aynı mantık."""
        last = self._store.last_visited()
        if last is None:
            sections = self._catalog.all_sections
            if not sections:
                return ""
            section = sections[0]
        else:
            section = self._catalog.section(*last)
            if section is None:
                return ""

        chapter = self._catalog.chapter(section.chapter_id)
        return self._language.t(
            "home.resume",
            chapter=self._language.pick(chapter.title) if chapter else "",
            section=self._language.pick(section.title),
        )

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._hero.set_mode(mode)
        for card in self._cards:
            card.set_mode(mode)

    def retranslate(self) -> None:
        self._label.setText(self._language.t_upper("track.section_label"))
        # "Kaldığın yer" satırı bölüm adını taşıyor ve o ad dile bağlı;
        # yeniden üretilmesi gerekiyor. **`refresh()` çağrılmıyor:** o da
        # sonunda `retranslate` çağırıyor ve ikisi birbirini sonsuza kadar
        # tetikliyor (denendi, `RecursionError`).
        self._hero.set_resume(self._resume_text())
        self._hero.retranslate()
        for card in self._cards:
            card.retranslate()


class ModulesView(QWidget):
    """Modül kartlarının listelendiği ana ekran."""

    module_opened = Signal(str)
    resume_requested = Signal()

    def __init__(
        self,
        catalog: Catalog,
        language: LanguageManager,
        store: ProgressStore,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._catalog = catalog
        self._language = language
        self._store = store
        self._mode = "light"
        self._cards: list[ModuleCard] = []
        self._track_id = ""

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        column = QWidget()
        self._page_layout = QVBoxLayout(column)
        self._page_layout.setContentsMargins(
            SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xxl"]
        )
        self._page_layout.setSpacing(SPACING["lg"])
        page = centered_column(column, max_width=1600)

        self._hero = HeroCard(language)
        self._hero.setFixedWidth(CONTENT_WIDTH)
        self._hero.resume.connect(self.resume_requested)
        self._page_layout.addWidget(self._hero, alignment=Qt.AlignmentFlag.AlignHCenter)

        self._modules_label = section_label("")
        self._page_layout.addWidget(self._modules_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self._grid = QGridLayout()
        self._grid.setSpacing(SPACING["md"])
        self._page_layout.addLayout(self._grid)
        self._page_layout.addStretch(1)

        outer.addWidget(scroll_page(page))
        self._build_cards()

    def show_track(self, track_id: str) -> None:
        """Yalnızca bu patikanın modüllerini gösterir."""
        self._track_id = track_id
        self._build_cards()
        self.refresh()

    def _build_cards(self) -> None:
        while self._grid.count():
            item = self._grid.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
                item.widget().deleteLater()
        self._cards = []

        track = self._catalog.track(self._track_id)
        chapters = track.chapters if track else self._catalog.chapters

        for index, chapter in enumerate(chapters):
            card = ModuleCard(chapter, self._language, self._mode)
            card.clicked.connect(lambda c=chapter.id: self.module_opened.emit(c))
            self._grid.addWidget(LiftSlot(card), index // 4, index % 4)
            self._cards.append(card)

    def refresh(self) -> None:
        """İlerleme verilerini veritabanından okuyup ekranı günceller."""
        total_sections = 0
        completed_sections = 0

        for card in self._cards:
            chapter = self._catalog.chapter(card.chapter_id)
            if chapter is None:
                continue

            done = 0
            for section in chapter.sections:
                state = self._store.section_state(
                    chapter.id, section.id, section.exercises
                )
                if state.status(section.requires_quiz, section.requires_exercises) == "completed":
                    done += 1

            card.update_progress(done, len(chapter.sections))
            card.retranslate()
            total_sections += len(chapter.sections)
            completed_sections += done

        total_exercises = sum(
            len(section.exercises) for section in self._catalog.all_sections
        )
        self._hero.update_stats(
            name=self._store.profile().get("first_name", ""),
            resume_text=self._resume_text(),
            sections=completed_sections,
            total_sections=total_sections,
            exercises=self._store.solved_exercise_count(),
            total_exercises=total_exercises,
            streak=self._store.streak(),
            progress=round(completed_sections * 100 / total_sections) if total_sections else 0,
        )
        self._modules_label.setText(self._language.t_upper("home.modules"))

    def _resume_text(self) -> str:
        last = self._store.last_visited()
        if last is None:
            first = self._catalog.all_sections
            if not first:
                return ""
            section = first[0]
            chapter = self._catalog.chapter(section.chapter_id)
        else:
            section = self._catalog.section(*last)
            if section is None:
                return ""
            chapter = self._catalog.chapter(section.chapter_id)

        return self._language.t(
            "home.resume",
            chapter=self._language.pick(chapter.title) if chapter else "",
            section=self._language.pick(section.title),
        )

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._hero.set_mode(mode)
        for card in self._cards:
            card.set_mode(mode)

    def retranslate(self) -> None:
        self.refresh()
        self._hero.retranslate()


class PathNode(QWidget):
    """Yol üzerindeki tek bir bölüm: yuvarlak düğme ve yanında başlık."""

    opened = Signal(str, str)

    def __init__(
        self,
        chapter_id: str,
        section_id: str,
        title: str,
        caption: str,
        state: str,
        order: int = 0,
        lock_color: str = "",
        color: str = "#8B84FF",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._chapter_id = chapter_id
        self._section_id = section_id
        self.state = state

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # Düğmenin çizim payı adın aralığından düşülüyor (yazı yerinde kalsın).
        layout.setSpacing(SPACING["md"] - NODE_PAD)

        # Düğme kendisi çiziyor (widgets/path_node.py): durum rengi, onay,
        # kilit, "şu an" halkası ve geçişler orada.
        self.button = NodeButton(state, order, color, lock_color)

        if state in ("planned", "locked"):
            # "planned" henüz yazılmadı, "locked" ise önündeki bölüm
            # bitmedi. İkisi de tıklanmıyor; boş ya da sırası gelmemiş bir
            # bölümü açmak "bozuk" izlenimi veriyor.
            self.button.setEnabled(False)
        else:
            self.button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.button.clicked.connect(
                lambda: self.opened.emit(self._chapter_id, self._section_id)
            )

        layout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignTop)

        # Adlar kendi kutusunda: yol ilk açılınca düğmeyle birlikte belirsin
        # (prototipte ad düğmenin içinde, onunla birlikte esniyor).
        self._labels_box = QWidget()
        self._labels_box.setProperty("role", "bare")
        labels = QVBoxLayout(self._labels_box)
        labels.setContentsMargins(0, 0, 0, 0)
        labels.setSpacing(0)
        labels.addSpacing(SPACING["md"] + NODE_PAD)

        self._title = QLabel(title)
        self._title.setProperty("role", "heading")
        self._title.setProperty("muted", "true" if state == "planned" else "false")
        # Kilitli bölümün adı da düğmesiyle birlikte soluk (prototip `.locked`).
        self._title.setProperty("locked", "true" if state == "locked" else "false")
        self._title.setWordWrap(True)
        labels.addWidget(self._title)

        self._caption = QLabel(caption)
        self._caption.setProperty("role", "muted")
        self._caption.setProperty("locked", "true" if state == "locked" else "false")
        self._caption.setWordWrap(True)
        labels.addWidget(self._caption)
        labels.addStretch(1)

        layout.addWidget(self._labels_box, 1)

        if state == "planned":
            # Kesik çerçeve tek başına yetmiyordu: yazılmış ama başlanmamış
            # bölümle yazılmamış bölüm ekranda birbirine çok benziyordu.
            # Soluklaştırma ayrımı bir bakışta veriyor.
            #
            # Kilitli bölüm **soluklaştırılmıyor**: soluk hâlde "hiç yok"
            # gibi duruyordu. O bölüm var, yazılmış ve sırası gelince
            # açılacak; onu anlatan şey kilit simgesi, silikleşme değil.
            solukluk = QGraphicsOpacityEffect(self)
            solukluk.setOpacity(PLANNED_OPACITY)
            self.setGraphicsEffect(solukluk)


    def hide_for_appear(self) -> None:
        """İlk çizimden önce: düğme ve adı görünmez."""
        from ..widgets.pop_effect import PopEffect
        self.button._appear = 0.0  # noqa: SLF001
        etki = PopEffect(self._labels_box)
        etki.set_state(0.0, 0.0, 0.0)
        self._labels_box.setGraphicsEffect(etki)

    def start_appear(self, delay: int) -> None:
        """Düğme 0'dan esneyerek büyür; adı da **düğmenin ortasından** onunla
        birlikte büyür (prototipte ad düğmenin içinde, `pop` ikisine birden)."""
        from ..resources.theme.motion import bounce
        self.button.start_appear(delay)
        etki = self._labels_box.graphicsEffect()
        if etki is None:
            return
        merkez = self.button.geometry().center()
        etki.origin = QPointF(merkez - self._labels_box.pos())

        def adim(t: float) -> None:
            k = bounce(t)
            etki.set_state(max(0.0, min(1.0, k)), max(0.0, k), 0.0)

        motion.animate(self, "labels", 0.0, 1.0, adim, "bounce", "linear", delay=delay,
                       on_done=lambda: self._labels_box.setGraphicsEffect(None))

    def show_now(self) -> None:
        self.button._appear = 1.0  # noqa: SLF001
        self.button.update()
        self._labels_box.setGraphicsEffect(None)


class OverlapColumn(QLayout):
    """Alt alta dizen yerleşim; yol satırlarını komşularına bindirir.

    Yol düğmesinin çevresinde `NODE_PAD` kadar boş çizim payı var (büyüme,
    gölge, halka kırpılmasın). Satır (`path_row` özelliği) bu pay kadar
    üstündekine ve altındakine biniyor; çizgi daireden daireye dokunmaya,
    başlıklarla aralar eskisi gibi kalmaya devam ediyor. `QVBoxLayout`
    negatif aralığı "varsayılan aralık" sayıyor, bindirme yapamıyor.
    Sonra eklenen öğe üstte çiziliyor (Qt'nin kardeş sırası).
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._items: list = []

    def addItem(self, item) -> None:  # noqa: N802
        self._items.append(item)

    def addStretch(self, _stretch: int = 0) -> None:  # noqa: N802 — QVBoxLayout ile aynı ad
        pass  # sayfa kaydırma alanında; esnemeye gerek yok

    def count(self) -> int:
        return len(self._items)

    def itemAt(self, index: int):  # noqa: N802
        return self._items[index] if 0 <= index < len(self._items) else None

    def takeAt(self, index: int):  # noqa: N802
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def expandingDirections(self):  # noqa: N802
        return Qt.Orientation(0)

    def hasHeightForWidth(self) -> bool:  # noqa: N802
        return True

    def heightForWidth(self, width: int) -> int:  # noqa: N802
        return self._place(QRect(0, 0, width, 0), apply=False)

    def sizeHint(self) -> QSize:  # noqa: N802
        m = self.contentsMargins()
        genis = max((i.sizeHint().width() for i in self._items), default=0)
        return QSize(genis + m.left() + m.right(), self.heightForWidth(max(genis, 400) + m.left() + m.right()))

    def minimumSize(self) -> QSize:  # noqa: N802
        m = self.contentsMargins()
        genis = max((i.minimumSize().width() for i in self._items), default=0)
        return QSize(genis + m.left() + m.right(), 0)

    def setGeometry(self, rect) -> None:  # noqa: N802
        super().setGeometry(rect)
        self._place(rect, apply=True)

    @staticmethod
    def _is_row(item) -> bool:
        w = item.widget()
        return bool(w is not None and w.property("path_row"))

    def _place(self, rect, apply: bool) -> int:
        m = self.contentsMargins()
        x = rect.x() + m.left()
        w = rect.width() - m.left() - m.right()
        y = rect.y() + m.top()
        onceki_satir = False
        ilk = True
        for item in self._items:
            if item.isEmpty():
                continue
            satir = self._is_row(item)
            if not ilk:
                y -= NODE_PAD * (int(onceki_satir) + int(satir))
            h = item.heightForWidth(w) if item.hasHeightForWidth() else item.sizeHint().height()
            if apply:
                item.setGeometry(QRect(x, y, w, h))
            y += h
            onceki_satir = satir
            ilk = False
        return y + m.bottom() - rect.y()


class PathConnector(QWidget):
    """İki halkayı birleştiren S biçimli eğri.

    Önceden halkanın altından dümdüz inen bir çizgiydi; halkalar zikzak
    dizildiği için bir sonraki halkaya ulaşmıyor, yarıda kopuk kalıyordu
    (Alican bildirdi). Eğri üstteki dairenin ortasından dikey çıkıp alttaki
    dairenin ortasına dikey giriyor; iki ucu da daireye teğet görünüyor.

    Uçlar düğmelerin **gerçek** ortasından hesaplanıyor, sabit sayıdan
    değil: halkanın genişliği kenarlıkla birlikte duruma göre 78 ya da 80
    piksel (QSS `max-width` kenarlığı saymıyor). Eski düz çizgi 74'e göre
    konduğu için dairelerin ortasından 1-3 piksel kaymıştı (ölçüldü).
    """

    def __init__(self, start: QWidget, color: str, parent: QWidget | None = None,
                 done_color: str = "", done: bool = False) -> None:
        super().__init__(parent)
        self._start = start
        self._end: QWidget | None = None
        self._color = color
        # Tamamlanan kısım patikanın renginde; `fill` 0 → 1 dolarak uzar.
        self._done_color = done_color or color
        self._fill = 1.0 if done else 0.0
        # Yol ilk açılırken temel çizgi yukarıdan aşağı çiziliyor (`draw`).
        self._draw = 1.0
        self.setFixedSize(BAND_WIDTH, CONNECTOR_HEIGHT)
        # Saydam: satırlara biniyor, zemin boyarsa düğmenin halkasını örtüyordu.
        self.setProperty("role", "bare")
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def _get_fill(self) -> float:
        return self._fill

    def _set_fill(self, v: float) -> None:
        self._fill = v
        self.update()

    fill = Property(float, _get_fill, _set_fill)

    def _get_draw(self) -> float:
        return self._draw

    def _set_draw(self, v: float) -> None:
        self._draw = v
        self.update()

    draw = Property(float, _get_draw, _set_draw)

    def set_end(self, end: QWidget) -> None:
        """Alttaki halkanın düğmesi; o halka kurulunca veriliyor."""
        self._end = end
        self.update()

    def _center_x(self, button: QWidget) -> float:
        left = self.mapFromGlobal(button.mapToGlobal(button.rect().topLeft())).x()
        return left + button.width() / 2

    def endpoints(self) -> tuple[float, float]:
        start = self._center_x(self._start)
        end = self._center_x(self._end) if self._end is not None else start
        return start, end

    def paintEvent(self, event) -> None:  # noqa: N802 (Qt adlandırması)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor(self._color))
        pen.setWidthF(CONNECTOR_WIDTH)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        start, end = self.endpoints()
        h = self.height()
        path = QPainterPath(QPointF(start, 0))
        path.cubicTo(QPointF(start, h * 0.55), QPointF(end, h * 0.45), QPointF(end, h))
        # Eğri yukarıdan aşağı tek yönlü iniyor: kısmi çizim üstten kırpmayla.
        if self._draw < 1.0:
            painter.setClipRect(QRectF(0, 0, self.width(), h * max(0.0, self._draw)))
        painter.drawPath(path)
        if self._fill > 0.0:
            renkli = QPen(QColor(self._done_color))
            renkli.setWidthF(CONNECTOR_WIDTH + 0.5)
            renkli.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(renkli)
            painter.setClipRect(QRectF(0, 0, self.width(), h * min(1.0, self._fill)))
            painter.drawPath(path)


class LevelHeader(QWidget):
    """Yolun üstünde bir seviye grubunu açan başlık.

    Uzun bir patikada (SQL sıfırdan ileri seviyeye gidiyor) bölümler tek
    sıra hâlinde akınca "ben neredeyim" sorusunun cevabı kayboluyor.
    Başlık iki yanına çizgi çekilmiş bir etiket: yolu kesmeden bölüyor.
    """

    def __init__(
        self,
        title: str,
        count: str,
        first: bool,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        row = QHBoxLayout(self)
        # İlk başlık sayfanın kendi üst boşluğunun altında duruyor; sonraki
        # başlıklar bir önceki grubun son halkasından ayrılmak için nefes
        # alanı istiyor.
        row.setContentsMargins(
            0, 0 if first else SPACING["xl"], 0, SPACING["md"]
        )
        row.setSpacing(SPACING["sm"])

        orta = Qt.AlignmentFlag.AlignVCenter
        row.addWidget(horizontal_rule(), 1, orta)
        row.addWidget(section_label(title), 0, orta)
        etiket = QLabel(count)
        etiket.setProperty("role", "muted")
        row.addWidget(etiket, 0, orta)
        row.addWidget(horizontal_rule(), 1, orta)


# Oturum boyunca: hangi modülün yolu görüldü, görüldüğünde hangi bölümler
# bitmişti. Yola dönüldüğünde aradaki fark "yeni biten" sayılıp canlandırılıyor.
_SEEN_CHAPTERS: set[str] = set()
_SEEN_DONE: dict[str, set[str]] = {}


class PathView(QWidget):
    """Bir modülün bölümlerini yol hâlinde gösterir."""

    section_opened = Signal(str, str)
    back_requested = Signal()

    def __init__(
        self,
        catalog: Catalog,
        language: LanguageManager,
        store: ProgressStore,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._catalog = catalog
        self._language = language
        self._store = store
        self._chapter_id = ""
        self._mode = "light"
        # Son kurulan yolun düğmeleri ve eğrileri (sırayla), oynatılmayı
        # bekleyen hareket.
        self._nodes: list[tuple[str, PathNode]] = []
        self._curves: dict[int, PathConnector] = {}
        self._pending: tuple[bool, list[int]] | None = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self._page = QWidget()
        # Satırlar düğmenin çizim payı kadar komşularına biniyor
        # (`OverlapColumn`): yol çizgisi daireden daireye dokunuyor.
        self._layout = OverlapColumn(self._page)
        self._layout.setContentsMargins(
            SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xxl"]
        )

        outer.addWidget(scroll_page(centered_column(self._page)))

    @property
    def chapter_id(self) -> str:
        """Şu an gösterilen modülün id'si."""
        return self._chapter_id

    def show_chapter(self, chapter_id: str) -> None:
        """Modülün yolunu kurar."""
        self._chapter_id = chapter_id
        self._rebuild()

    def refresh(self) -> None:
        if self._chapter_id:
            self._rebuild()

    def _rebuild(self) -> None:
        self._nodes = []
        self._curves = {}
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        chapter = self._catalog.chapter(self._chapter_id)
        if chapter is None:
            return

        # **Modülün adı ve açıklaması burada yazmıyor.** Ekranın başlığı
        # zaten modülün adını taşıyor (`_update_headers`), açıklaması da bir
        # önceki ekrandaki modül kartında duruyor. Sayfanın tepesinde
        # üçüncü kez tekrar etmek yolu aşağı itiyordu.

        self._pending_curve: PathConnector | None = None

        # "Şu an buradasın" işareti: tamamlanmamış ilk yazılmış bölüm.
        outline = chapter.outline
        current_index = self._current_index(outline, chapter.id)

        basliklar = self._level_headers(chapter, outline)

        for index, section in enumerate(outline):
            son = index == len(outline) - 1
            grup_bitiyor = (index + 1) in basliklar
            baslik = basliklar.get(index)
            if baslik is not None:
                self._layout.addWidget(baslik)

            if isinstance(section, dict):
                # Henüz yazılmamış bölüm: soluk, tıklanmayan halka. Modülün
                # nereye gittiğini baştan göstermek, "burası bu kadarmış"
                # izlenimini önlüyor.
                node = PathNode(
                    chapter.id,
                    section.get("id", ""),
                    self._language.pick(section.get("title")),
                    self._language.t("path.planned"),
                    "planned",
                    order=index + 1,
                    color=chapter.color,
                )
                self._attach(node)
                self._nodes.append((section.get("id", ""), node))
                self._layout.addWidget(self._zigzag_row(node, index))
                if not son and not grup_bitiyor:
                    self._layout.addWidget(self._connector(node, False, len(self._nodes) - 1, chapter.color))
                continue

            state = self._state_of(chapter.id, section)
            if index == current_index and state != "completed":
                state = "current"

            # Önündeki bölüm bitmemişse bu bölüm kilitli. "Şu an buradasın"
            # işareti kilitli bölüme düşemiyor: ilk tamamlanmamış bölümün
            # önü tanım gereği açık.
            engel = blocking_section(self._catalog, self._store, chapter.id, section.id)
            if engel is not None:
                state = "locked"

            palette = PALETTES.get(self._mode, PALETTES["light"])
            node = PathNode(
                chapter.id,
                section.id,
                self._language.pick(section.title),
                self._caption_for(section, state, engel),
                state,
                order=index + 1,
                lock_color=palette["warning"],
                color=chapter.color,
            )
            node.opened.connect(self.section_opened)

            self._attach(node)
            self._nodes.append((section.id, node))
            self._layout.addWidget(self._zigzag_row(node, index))

            # Bir sonraki bölüm yeni bir grubu açıyorsa bağlayıcı çizgi
            # çizilmiyor: çizgi başlığın içinden geçmiş gibi duruyordu.
            if not son and not grup_bitiyor:
                self._layout.addWidget(self._connector(node, state == "completed",
                                                       len(self._nodes) - 1, chapter.color))

        self._layout.addStretch(1)
        self._prepare_motion(chapter.id)

    def _prepare_motion(self, chapter_id: str) -> None:
        """İlk açılış çizimi ve yeni biten bölümler için başlangıç görünümü.

        Yeni biten bölümün düğmesi önce "şu an" olarak, ondan çıkan eğri boş
        çiziliyor; oynatılınca düğme dolup onay zıplıyor, eğri renkle
        doluyor, sonraki düğme "şu an" oluyor (ui-taslak C3). Görünmezken
        kurulduysa (bölümden dönmeden önce) hareket görünür olunca oynuyor.
        """
        biten = {sid for sid, node in self._nodes if node.state == "completed"}
        ilk = chapter_id not in _SEEN_CHAPTERS
        gorulen = _SEEN_DONE.get(chapter_id)
        yeni = [] if gorulen is None else [i for i, (sid, _n) in enumerate(self._nodes)
                                           if sid in biten and sid not in gorulen]
        for i in yeni:
            node = self._nodes[i][1]
            node.button.set_state("current", animate=False)
            egri = self._curves.get(i)
            if egri is not None:
                egri._set_fill(0.0)  # noqa: SLF001
            if i + 1 < len(self._nodes):
                sonraki = self._nodes[i + 1][1].button
                if sonraki.state == "current":
                    sonraki.set_state("locked" if not self._unlock_all() else "not_started", animate=False)
        if ilk and motion.enabled():
            for _sid, node in self._nodes[:14]:
                node.hide_for_appear()
            for egri in self._curves.values():
                egri._set_draw(0.0)  # noqa: SLF001
        self._pending = (ilk, yeni) if (ilk or yeni) else None
        if self._pending and self.isVisible():
            QTimer.singleShot(0, self._play)

    def _unlock_all(self) -> bool:
        from ..core.unlock import unlock_all
        return unlock_all(self._store)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        if self._pending:
            QTimer.singleShot(0, self._play)

    def _play(self) -> None:
        if not self._pending or not self.isVisible():
            return
        ilk, yeni = self._pending
        self._pending = None
        _SEEN_CHAPTERS.add(self._chapter_id)
        _SEEN_DONE[self._chapter_id] = {sid for sid, node in self._nodes
                                        if node.state == "completed" or node.button.state == "completed"}
        _SEEN_DONE[self._chapter_id] |= {self._nodes[i][0] for i in yeni}
        gecikme = 0
        if ilk and motion.enabled():
            # Düğmeler sırayla esneyerek beliriyor, eğriler yukarıdan aşağı çiziliyor.
            for i, (_sid, node) in enumerate(self._nodes[:14]):
                node.start_appear(120 + min(i, 12) * 55)
            # Çizgi tek parça: yolun tamamı yukarıdan aşağı 800 ms'de,
            # yavaşlayarak çiziliyor (prototip `.pathsvg .base`, `draw`).
            egriler = [self._curves[i] for i in sorted(self._curves)]
            if egriler:
                adet = len(egriler)

                def ciz(t: float, egriler=egriler, adet=adet) -> None:
                    ilerleme = t * adet
                    for j, egri in enumerate(egriler):
                        egri._set_draw(max(0.0, min(1.0, ilerleme - j)))  # noqa: SLF001

                motion.animate(self, "draw", 0.0, 1.0, ciz, 800, "out")
            for _sid, node in self._nodes[14:]:
                node.show_now()
            gecikme = 900
        elif ilk:
            for _sid, node in self._nodes:
                node.show_now()
            for egri in self._curves.values():
                egri._set_draw(1.0)  # noqa: SLF001
        # Yeni biten her bölüm sırayla: düğme dolar, çizgi uzar, sonraki "şu an".
        adim = 0
        for i in yeni:
            bekle = gecikme + 350 + adim * 900
            adim += 1
            QTimer.singleShot(bekle if motion.enabled() else 0, lambda k=i: self._complete_step(k))
        if yeni:
            self._scroll_to(yeni[0])

    def _complete_step(self, i: int) -> None:
        if i >= len(self._nodes):
            return
        self._nodes[i][1].button.set_state("completed")
        egri = self._curves.get(i)

        def sonraki() -> None:
            if i + 1 < len(self._nodes):
                node = self._nodes[i + 1][1]
                node.button.set_state(node.state)

        if egri is not None:
            motion.animate_property(egri, "fill", 1.0, "long", "out", start=0.0, delay=200,
                                    on_done=sonraki)
        else:
            QTimer.singleShot(200, sonraki)

    def _scroll_to(self, i: int) -> None:
        alan = self.findChild(QScrollArea)
        if alan is None or i >= len(self._nodes):
            return
        node = self._nodes[i][1]
        y = node.mapTo(alan.widget(), QPointF(0, 0).toPoint()).y()
        alan.verticalScrollBar().setValue(max(0, y - alan.viewport().height() // 3))

    def _attach(self, node: PathNode) -> None:
        """Bekleyen eğrinin alt ucunu bu halkaya bağlar."""
        if self._pending_curve is not None:
            self._pending_curve.set_end(node.button)
            self._pending_curve = None

    def _level_headers(self, chapter: Chapter, outline: list) -> dict[int, QWidget]:
        """Seviyenin değiştiği her bölümün önüne konacak başlıklar.

        Bölümlerde `level` yazmıyorsa sözlük boş kalıyor ve yol eskisi gibi
        kesintisiz akıyor — mevcut modüllerin hiçbiri etkilenmiyor. Sayı
        kesir yazılıyor (`2/6`), çünkü çıplak bir sayı grubun ne kadarının
        bittiğini söylemiyor.
        """
        basliklar: dict[int, QWidget] = {}
        onceki = ""

        def seviyesi(entry) -> str:
            # Planlanan bölüm sözlük; seviyesi `level` anahtarında.
            return entry.get("level", "") if isinstance(entry, dict) else entry.level

        for index, section in enumerate(outline):
            seviye = seviyesi(section)
            if not seviye or seviye == onceki:
                continue
            onceki = seviye

            grup = [s for s in outline if seviyesi(s) == seviye]
            biten = sum(
                1
                for s in grup
                if not isinstance(s, dict) and self._state_of(chapter.id, s) == "completed"
            )
            # Büyük harf `t_upper` ile alınıyor: Python'un `.upper()`
            # metodu Türkçedeki `i`yi noktasız `I` yapıyor ve "Orta Seviye"
            # ekranda "ORTA SEVIYE" diye yazılıyordu.
            basliklar[index] = LevelHeader(
                self._language.t_upper(f"path.level_{seviye}"),
                self._language.t(
                    "path.level_count", done=biten, total=len(grup)
                ),
                first=not basliklar,
            )

        return basliklar

    def _zigzag_row(self, node: QWidget, index: int) -> QWidget:
        """Bir yol halkasını zikzak konumuna koyup satırı ortalar.

        Halkalar önce yalnızca soldan boşluk verilerek diziliyordu; zikzak
        çalışıyordu ama bandın tamamı sütunun soluna yapışıyor, sağda geniş
        bir boşluk kalıyordu. Şimdi bandın genişliği en büyük kaydırma kadar
        sabit sayılıyor (`max(ZIGZAG)`) ve iki yanına eşit esneme konuyor —
        yol, hangi halkada olursak olalım ekranın ortasında duruyor.
        """
        kaydirma = ZIGZAG[index % len(ZIGZAG)]
        node.setFixedWidth(NODE_WIDTH)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)
        row.addStretch(1)
        row.addSpacing(kaydirma)
        row.addWidget(node)
        row.addSpacing(BAND_WIDTH - kaydirma - NODE_WIDTH)
        row.addStretch(1)

        container = QWidget()
        container.setProperty("role", "bare")
        container.setProperty("path_row", True)
        container.setLayout(row)
        return container

    def _connector(self, node: PathNode, done: bool, index: int = -1, color: str = "") -> QWidget:
        # Eğri, bu halkanın dairesinin ortasından bir sonrakininkine gidiyor;
        # sonraki halka kurulunca `_rebuild` ucunu ona bağlıyor. Tamamlanan
        # kısım patikanın renginde (önce yeşildi).
        palette = PALETTES.get(self._mode, PALETTES["light"])
        curve = PathConnector(node.button, palette["border"], done_color=color or palette["success"], done=done)
        self._pending_curve = curve
        if index >= 0:
            self._curves[index] = curve

        holder = QWidget()
        # Saydam: satırlara biniyor; zemin boyarsa düğmenin halkasını örtüyordu.
        holder.setProperty("role", "bare")
        holder.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        layout = QHBoxLayout(holder)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addStretch(1)
        layout.addWidget(curve)
        layout.addStretch(1)
        return holder

    def _state_of(self, chapter_id: str, section) -> str:
        state = self._store.section_state(chapter_id, section.id, section.exercises)
        return state.status(section.requires_quiz, section.requires_exercises)

    def _current_index(self, outline: list, chapter_id: str) -> int:
        for index, section in enumerate(outline):
            if isinstance(section, dict):
                continue
            if self._state_of(chapter_id, section) != "completed":
                return index
        return -1

    def _caption_for(self, section, state: str, blocker=None) -> str:
        progress = self._store.section_state(
            self._chapter_id, section.id, section.exercises
        )
        minutes = section.estimated_minutes

        if state == "locked" and blocker is not None:
            return self._language.t(
                "path.caption_locked", section=self._language.pick(blocker.title)
            )
        if state == "completed":
            return self._language.t("path.caption_completed", minutes=minutes)
        if state == "current":
            return self._language.t("path.caption_current", minutes=minutes)
        if state == "in_progress":
            return self._language.t(
                "path.caption_partial",
                done=progress.exercises_solved,
                total=max(progress.exercises_total, 1),
            )
        return self._language.t("path.caption_new", minutes=minutes)

    def set_mode(self, mode: str) -> None:
        # Kilit simgesinin rengi temaya göre üretiliyor; mod saklanmazsa
        # koyu temada açık temanın rengi çiziliyordu.
        self._mode = mode
        self._rebuild()

    def retranslate(self) -> None:
        self._rebuild()


class JourneyView(FadeStack):
    """Modül kartları ile yol arasında geçiş yapan kapsayıcı."""

    section_opened = Signal(str, str)
    # Başlık şeridindeki geri düğmesi buna bakarak görünüp kayboluyor.
    view_changed = Signal()

    def __init__(
        self,
        catalog: Catalog,
        language: LanguageManager,
        store: ProgressStore,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._catalog = catalog

        # Üç katman: patikalar -> modüller -> yol.
        self.tracks = TracksView(catalog, language, store)
        self.modules = ModulesView(catalog, language, store)
        self.path = PathView(catalog, language, store)

        self.addWidget(self.tracks)
        self.addWidget(self.modules)
        self.addWidget(self.path)

        self.tracks.track_opened.connect(self.open_track)
        self.tracks.resume_requested.connect(self._resume)
        self.modules.resume_requested.connect(self._resume)
        self.modules.module_opened.connect(self.open_module)
        self.path.section_opened.connect(self.section_opened)

        self._track_id = ""
        self._skipped_modules = False

    def _resume(self) -> None:
        hedef = self.tracks.resume_target()
        if hedef is not None:
            self.section_opened.emit(*hedef)

    def open_track(self, track_id: str) -> None:
        """Patikayı açar.

        Patikada tek modül varsa modül listesi atlanıyor: tek kartlık bir
        ekranda "Python Temelleri"ne bir kez daha tıklatmanın kimseye
        faydası yok. Birden fazla modül olduğunda liste gerekiyor, o zaman
        gösteriliyor.
        """
        self._track_id = track_id
        track = self._catalog.track(track_id)
        chapters = track.chapters if track else []

        if len(chapters) == 1 or (track is not None and track.chapter_tabs and chapters):
            self._skipped_modules = True
            self.open_module(chapters[0].id)
            return

        self._skipped_modules = False
        self.modules.show_track(track_id)
        self.slide_to(self.modules, FORWARD)
        self.view_changed.emit()

    def open_module(self, chapter_id: str) -> None:
        # Sekmeli patikada modül değişince (MAT 1 → MAT 2) yön yok, yalnızca geçiş.
        yon = NONE if self.currentWidget() is self.path else FORWARD
        self.path.show_chapter(chapter_id)
        self.slide_to(self.path, yon)
        self.view_changed.emit()

    def show_modules(self) -> None:
        """Patika ekranına döner: şeritteki "Öğrenme Yolu" buraya gidiyor."""
        self.tracks.refresh()
        self.slide_to(self.tracks, NONE if self.currentWidget() is self.tracks else BACK)
        self.view_changed.emit()

    def back(self) -> None:
        """Bir seviye yukarı çıkar.

        Modül listesi atlanmışsa geri de atlıyor; yoksa kullanıcı gelirken
        görmediği bir ekrana düşüyor.
        """
        if self.currentWidget() is self.path and not self._skipped_modules:
            self.modules.refresh()
            self.slide_to(self.modules, BACK)
        else:
            self.tracks.refresh()
            self.slide_to(self.tracks, BACK)
        self.view_changed.emit()

    @property
    def showing_path(self) -> bool:
        return self.currentWidget() is self.path

    @property
    def back_goes_to_tracks(self) -> bool:
        """Geri düğmesi patikalara mı dönüyor (modül listesi atlandıysa)?"""
        return self.currentWidget() is self.modules or self._skipped_modules

    @property
    def showing_tracks(self) -> bool:
        return self.currentWidget() is self.tracks

    @property
    def chapter_tabs(self) -> list:
        """Yoldayken başlıkta gösterilecek modül sekmeleri; yoksa boş liste."""
        track = self._catalog.track(self._track_id)
        if track is None or not track.chapter_tabs or not self.showing_path:
            return []
        return list(track.chapters)

    @property
    def track_title(self) -> dict:
        track = self._catalog.track(self._track_id)
        return track.title if track else {}

    def refresh(self) -> None:
        self.tracks.refresh()
        self.modules.refresh()
        self.path.refresh()

    def set_mode(self, mode: str) -> None:
        self.set_background(PALETTES[mode]["bg"])
        self.tracks.set_mode(mode)
        self.modules.set_mode(mode)
        self.path.set_mode(mode)

    def retranslate(self) -> None:
        self.tracks.retranslate()
        self.modules.retranslate()
        self.path.retranslate()
