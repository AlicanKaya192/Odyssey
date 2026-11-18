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

import re
from dataclasses import replace
from datetime import date

from PySide6.QtCore import (
    Property,
    QElapsedTimer,
    QEvent,
    QObject,
    QPoint,
    QPointF,
    QRect,
    QRectF,
    QSize,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QFont,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
)
from PySide6.QtWidgets import (
    QButtonGroup,
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
from ..widgets.lift_card import ENTER, LIFT, GlowCard, LiftSlot
from ..widgets.logo_mark import LogoMark
from ..widgets.progress_bar import ProgressBar
from ..widgets import motion
from ..widgets.path_node import PAD as NODE_PAD, NodeButton
from ..resources.logos import logo_key
from ..core.catalog import Catalog, Chapter, Track, TrackGroup
from ..core.completion import is_completed
from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..core.unlock import blocking_section
from ..core import for_you, new_tracks, review_box, weekly_goal
from ..resources.icons import icon, pixmap
from ..resources.theme.tokens import CONTENT_WIDTH, FONTS, PALETTES, RADIUS, SPACING, mix
from ..widgets.common import StatBlock, horizontal_rule, section_label
from ..widgets.streak_flame import FlickerFlame, hero_flame_pixmap, next_tier, tier_for
from ..widgets.effects import ShadowLayer, apply_shadow, refresh_shadow, repolish

# Qt iki harf arasındaki eğik çizgiden sonra satırı kırabiliyor ("(CI/" + "CD).",
# "A/" + "B"); arkasına konan görünmez birleştirici (word joiner) bunu önlüyor.
# Yalnızca ekrandaki metne konur: içerik dosyasında olsa aramada "CI/CD" bulunmazdı.
WORD_JOINER = chr(0x2060)
_SLASH_BETWEEN_LETTERS = re.compile(r"(?<=\w)/(?=\w)")


def keep_slash_words(text: str) -> str:
    """"CI/CD", "A/B" gibi kelimeleri satır sonunda bölünmez yapar."""
    return _SLASH_BETWEEN_LETTERS.sub("/" + WORD_JOINER, text)


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


# Prototip ölçüsü: sayfa sütunu (`.wrapc`). Ana ekranınki `JOURNEY_WIDTH`.
PAGE_WIDTH = 1180


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
        # Emoji yazı tipi açıkça: arayüz yazı tipinde 👋 yok ve Qt yedek
        # yazı tipi ararken bütün sistem yazı tiplerini tarıyor (`tokens.FONTS`).
        f = QFont(self.font())
        f.setFamily("Segoe UI Emoji")
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
    # Tekrar kutusunu aç (`core/review_box.py`).
    review = Signal()

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
        # Tekrar kutusu: bugün sorulacak soru varsa yanında, daha sade.
        self._review = QPushButton()
        self._review.setCursor(Qt.CursorShape.PointingHandCursor)
        self._review.setIcon(icon("repeat", "#FFFFFF", 16))
        self._review.setStyleSheet(
            "QPushButton { color:#FFFFFF; font-weight:600; font-size:13.5px; padding:9px 14px 9px 12px;"
            " background: transparent; border:1px solid rgba(255,255,255,0.30);"
            " border-radius:14px; min-height:0px; }"
            " QPushButton:hover { background: rgba(255,255,255,0.14); }"
            " QPushButton:pressed { background: rgba(255,255,255,0.22); }"
        )
        self._review.clicked.connect(self.review)
        self._review_slot = ShiftSlot(self._review, 3)
        self._review_slot.hide()
        self._reviews = 0
        dugmeler = QHBoxLayout()
        dugmeler.setSpacing(SPACING["sm"])
        dugmeler.addWidget(self._continue_slot)
        dugmeler.addWidget(self._review_slot)
        dugmeler.addStretch(1)
        layout.addSpacing(SPACING["sm"])
        layout.addLayout(dugmeler)
        layout.addSpacing(SPACING["sm"])

        stats = QHBoxLayout()
        stats.setSpacing(30)
        self._stats = {
            key: StatBlock("0", "", inverse=True)
            for key in ("sections", "exercises", "streak", "goal")
        }
        for block in self._stats.values():
            # Sayılar etiketleriyle birlikte sola yaslı (örnekteki gibi).
            block.set_centered(False)
            block.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            block.setStyleSheet("background: transparent;")
            stats.addWidget(block)
        stats.addStretch(1)
        layout.addLayout(stats)
        # Haftalık hedef yalnızca açıksa görünüyor (`core/weekly_goal.py`).
        self._goal = None
        self._stats["goal"].hide()

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
        goal=None,
        reviews: int = 0,
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
        self._goal = goal
        self._reviews = reviews
        self._review_slot.setVisible(reviews > 0)
        self._stats["goal"].setVisible(goal is not None)
        if goal is not None:
            self._stats["goal"].set_value(f"{goal.done}/{goal.target}")
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
        self._render_goal()
        # Yüzde işareti dile göre: Türkçede önde (%40), İngilizcede sonda (40%).
        self._ring.set_texts(self._language.t("home.percent", value=self._progress),
                             self._language.t("home.stat_progress"))
        self._continue.setText("  " + self._language.t("home.continue"))
        self._continue_slot.fit()
        self._review.setText("  " + self._language.t("home.review", count=self._reviews))
        self._review.setToolTip(self._language.t("home.review_tip"))
        self._review_slot.fit()
        self._render_flame()


    def _render_goal(self) -> None:
        """Haftalık hedefin etiketi ve ipucu (dil değişince de)."""
        goal = self._goal
        if goal is None:
            return
        from ..widgets import tips

        t = self._language.t
        blok = self._stats["goal"]
        blok.set_label(t(f"home.stat_goal_{goal.kind}"))
        if goal.reached:
            durum, ton = t("goal.tip_done"), "success"
        else:
            durum, ton = t(f"goal.tip_left_{goal.kind}", n=goal.target - goal.done), "accent"
        blok.setToolTip(tips.rich(t("goal.tip_title"), t("goal.tip_body"), durum, ton))


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


# Kilitli patikada logonun köşesindeki kilit rozetinin çapı.
LOCK_BADGE = 22

# Kart gölgesinin (bulanıklık 24) grup bileşeninin içinde kalan payı. Gölge
# kartı taşıyan bileşenin sınırında kesiliyor; pay yokken açık temada
# ızgaranın iki yanında düz kenarlı gri bir dikdörtgen görünüyordu.
SHADOW_ROOM = 24

# Ana ekranın sütunu (taslak 1, `.page`: 1436 px'te iki yanda 98 px).
JOURNEY_WIDTH = 1240

# "Senin için" şeridinin atlama düğmesindeki anahtarı; öteki düğmeler grup kimliği.
FOR_YOU = "for_you"


class ElidedLabel(QLabel):
    """Tek satırlık etiket: sığmazsa sonu "…" ile kesilir, tamamı `full_text`.

    Önerdiği genişlik metnin tamamı, en küçüğü 0: yer varsa metin bütün
    görünüyor, yoksa yanındakileri itmeden kısalıyor.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._full = ""
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

    def full_text(self) -> str:
        return self._full

    def setText(self, text: str) -> None:  # noqa: N802 (Qt adlandırması)
        self._full = text
        self._elide()
        self.updateGeometry()

    def _elide(self) -> None:
        kisa = self.fontMetrics().elidedText(self._full, Qt.TextElideMode.ElideRight, max(0, self.width()))
        if kisa != super().text():
            super().setText(kisa)

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(self.fontMetrics().horizontalAdvance(self._full) + 2, super().sizeHint().height())

    def minimumSizeHint(self) -> QSize:  # noqa: N802
        return QSize(0, super().minimumSizeHint().height())

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._elide()

    def changeEvent(self, event) -> None:  # noqa: N802
        super().changeEvent(event)
        if event.type() == QEvent.Type.FontChange:
            self._elide()


class RingSpin(QObject):
    """Yeni patika kartının kenarında dönen ışık yayının saati.

    Tur 5 sn, doğrusal; açılışta 3 tur (ilk %4'te belirip son %8'de sönüyor),
    üzerine gelince 1 tur (%10 / %85). Zamanlayıcı yalnızca dönerken **ve**
    izin varken (ekran görünür, pencere etkin, kart görünür alanda) çalışıyor;
    izin kalkınca duruyor, gelince kaldığı yerden sürüyor. Animasyonlar
    kapalıysa (Ayarlar; varsayılanı Windows'un "animasyon efektleri") hiç
    dönmüyor.
    """

    TURN_MS = 5000
    TICK_MS = 16

    def __init__(self, target: QWidget) -> None:
        super().__init__(target)
        self._target = target
        self._timer = QTimer(self)
        self._timer.setInterval(self.TICK_MS)
        self._timer.timeout.connect(self._tick)
        self._clock = QElapsedTimer()
        self._elapsed = 0
        self._duration = 0
        self._fade = (0.0, 1.0)
        self._allowed = False
        self.ticks = 0  # ölçüm için: kaç kez tetiklendi

    @property
    def spinning(self) -> bool:
        return self._duration > 0

    @property
    def running(self) -> bool:
        return self._timer.isActive()

    def start(self, turns: int, fade_in: float, fade_out: float) -> None:
        """`turns` tur döndürür; zaten dönüyorsa dokunmaz."""
        if self.spinning or not motion.enabled():
            return
        self._duration = turns * self.TURN_MS
        self._elapsed = 0
        self._fade = (fade_in, fade_out)
        self._sync()

    def stop(self) -> None:
        self._duration = 0
        self._elapsed = 0
        self._sync()
        self._target.update()

    def set_allowed(self, allowed: bool) -> None:
        self._allowed = allowed
        self._sync()

    def _sync(self) -> None:
        calissin = self._allowed and self.spinning
        if calissin and not self._timer.isActive():
            self._clock.start()
            self._timer.start()
        elif not calissin and self._timer.isActive():
            self._timer.stop()

    def _tick(self) -> None:
        self.ticks += 1
        self._elapsed += self._clock.restart()
        if self._elapsed >= self._duration:
            self.stop()
            return
        self._target.update()

    @property
    def angle(self) -> float:
        """Işığın açısı: üstten saat yönünde, derece."""
        return 360.0 * (self._elapsed % self.TURN_MS) / self.TURN_MS

    @property
    def opacity(self) -> float:
        if not self.spinning:
            return 0.0
        k = self._elapsed / self._duration
        giris, cikis = self._fade
        if k < giris:
            return k / giris
        if k > cikis:
            return max(0.0, (1.0 - k) / (1.0 - cikis))
        return 1.0


def _ring_gradient(rect: QRectF, angle: float, accent: str, mode: str, opacity: float) -> QConicalGradient:
    """Prototipteki `conic-gradient`: 290°'ye kadar saydam, sonra patika
    renginden açık mora, uçta beyaz (açık temada beyaz yok, alfa düşük).

    CSS konik geçişi üstten saat yönünde, Qt'ninki sağdan saat tersine
    ilerliyor: açı `90 - a`, konumlar `1 - p`.
    """
    renk = QColor(mix(accent, "#B7A8FF", 0.3))
    gecis = QConicalGradient(rect.center(), 90.0 - angle)
    saydam = QColor(renk)
    saydam.setAlpha(0)

    def alfa(c: QColor, a: float) -> QColor:
        c = QColor(c)
        c.setAlphaF(max(0.0, min(1.0, a * opacity)))
        return c

    koyu = mode == "dark"
    uc = alfa(QColor("#FFFFFF"), 0.9) if koyu else alfa(renk, 0.75)
    gecis.setColorAt(0.0, saydam)
    gecis.setColorAt(8 / 360, uc)
    gecis.setColorAt(35 / 360, alfa(renk, 1.0 if koyu else 0.55))
    gecis.setColorAt(70 / 360, saydam)
    gecis.setColorAt(1.0, saydam)
    return gecis


class PrereqChip(QFrame):
    """Önerilen ön koşul hapı: tabela simgesi ve "Önce: Python".

    Düz soluk yazıyken sayaçla aynı satırda kaybolup gidiyordu (Alican 17
    Kasım). Ön koşul bir öneri; ne kilit ne uyarı. Bu yüzden renk nötr:
    "Devam ediyor"un vurgu renginden ve uyarı turuncusundan ayrı, çerçeveli
    gri bir hap, yazı tam metin renginde ve orta kalınlıkta.
    """

    ICON = 12

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("role", "pre-chip")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        satir = QHBoxLayout(self)
        satir.setContentsMargins(7, 2, 9, 2)
        satir.setSpacing(5)
        self._icon = QLabel()
        self._icon.setFixedSize(self.ICON, self.ICON)
        self._text = QLabel()
        self._text.setProperty("role", "pre-chip-text")
        satir.addWidget(self._icon, 0, Qt.AlignmentFlag.AlignVCenter)
        satir.addWidget(self._text, 0, Qt.AlignmentFlag.AlignVCenter)

    def text(self) -> str:
        return self._text.text()

    def set_text(self, text: str) -> None:
        self._text.setText(text)

    def set_mode(self, mode: str) -> None:
        p = PALETTES.get(mode, PALETTES["dark"])
        self._icon.setPixmap(pixmap("signpost", p["text_muted"], self.ICON))


class TrackCard(GlowCard):
    """Bir öğrenme patikasının büyük kartı ("Senin için" şeridi; taslak 1).

    Solda logo, sağda başlık ve etiketler ("Devam ediyor", "YENİ", "Rotanda
    sıradaki"), açıklamanın tamamı, en altta ilerleme çubuğu ile "3 / 19
    bölüm · ~13 saat" ve sağda yüzde ya da önerilen ön koşul ("Önce:
    Python"). Boyu şerit veriyor: yan yana kartlar aynı boyda.

    Yeni patikada (`set_marks(new=True)`) kenar patika renginde, arkasında
    hâle ve kenarda dönen bir ışık yayı var (`RingSpin`).
    """

    clicked = Signal()

    PAD = 20
    LOGO = 44
    CHIP_GAP = 10
    META_GAP = 12

    def __init__(self, track: Track, language: LanguageManager, mode: str,
                 prerequisite: Track | None = None, parent: QWidget | None = None) -> None:
        super().__init__(parent, interactive=not track.locked)
        self._track = track
        self._prerequisite = prerequisite
        self._language = language
        self._completed = 0
        self._total = sum(len(chapter.sections) for chapter in track.chapters)
        # Tahmini süre: bölümlerin `estimated_minutes` toplamı, saate yuvarlanmış.
        minutes = sum(s.estimated_minutes for chapter in track.chapters for s in chapter.sections)
        self._hours = max(1, round(minutes / 60)) if minutes else 0
        self._started = False
        self._prerequisite_done = False
        self._new = False
        self._route = ""
        self._halo: ShadowLayer | None = None
        self._mode = mode
        self._radius = 18
        self._spin = RingSpin(self)
        self.set_accent(track.color)
        self.set_card_mode(mode)
        self.setProperty("variant", "track")
        self.setProperty("locked", "true" if track.locked else "false")
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        if not track.locked:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            apply_shadow(self, mode, radius=18)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(self.PAD, self.PAD, self.PAD, self.PAD)
        layout.setSpacing(16)
        self._icon = LogoMark(logo_key(track.icon, track.id), track.color, self.LOGO, locked=track.locked)
        self.hovered.connect(self._icon.set_hovered)
        layout.addWidget(self._icon, 0, Qt.AlignmentFlag.AlignTop)

        body = QVBoxLayout()
        body.setSpacing(0)
        baslik = QHBoxLayout()
        baslik.setSpacing(self.CHIP_GAP)
        self._title = QLabel()
        self._title.setWordWrap(True)
        self._title.setProperty("role", "track-title")
        baslik.addWidget(self._title)
        # Etiketler: "Devam ediyor", "YENİ", "Rotanda sıradaki".
        self._chips = []
        for role in ("track-chip", "track-chip-new", "track-chip-next"):
            chip = QLabel()
            chip.setProperty("role", role)
            chip.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            chip.hide()
            baslik.addWidget(chip, 0, Qt.AlignmentFlag.AlignVCenter)
            self._chips.append(chip)
        self._chip, self._new_chip, self._route_chip = self._chips
        baslik.addStretch(1)
        body.addLayout(baslik)
        body.addSpacing(6)
        self._description = QLabel()
        self._description.setWordWrap(True)
        self._description.setProperty("role", "track-desc")
        body.addWidget(self._description)
        body.addSpacing(14)
        body.addStretch(1)

        self._bar = ProgressBar(f"track:{track.id}")
        self._bar.set_color(track.color)
        self._bar.set_mode(mode)
        self._bar.hide()
        body.addWidget(self._bar)
        meta = QHBoxLayout()
        meta.setContentsMargins(0, 0, 0, 0)
        meta.setSpacing(self.META_GAP)
        self._meta = meta
        self._meta_left = QLabel()
        self._meta_left.setProperty("role", "track-meta")
        self._meta_right = QLabel()
        self._meta_right.setProperty("role", "track-meta")
        self._pre = PrereqChip()
        self._pre.set_mode(mode)
        meta.addWidget(self._meta_left)
        meta.addStretch(1)
        meta.addWidget(self._meta_right)
        meta.addWidget(self._pre, 0, Qt.AlignmentFlag.AlignVCenter)
        self._meta_space = QWidget()
        self._meta_space.setProperty("role", "bare")
        self._meta_space.setFixedHeight(8)
        body.addWidget(self._meta_space)
        body.addLayout(meta)
        layout.addLayout(body, 1)
        self._show_progress()

    def height_for(self, width: int) -> int:
        """Bu genişlikte içeriğin sığdığı en küçük boy."""
        self.ensurePolished()
        for label in (self._title, self._description, self._pre, self._pre._text, self._meta_left,
                      self._meta_right, *self._chips):
            label.ensurePolished()
        self._fit(width)
        return self.layout().totalHeightForWidth(width)

    def _body_width(self, width: int) -> int:
        """Logonun sağındaki sütunun genişliği. Logo bileşeni döndürülünce
        köşeleri taşmasın diye `LOGO`'dan geniş (`LogoMark` payı)."""
        return width - 2 * self.PAD - self._icon.sizeHint().width() - self.layout().spacing()

    def _fit(self, width: int) -> None:
        self._fit_title(width)
        self._fit_meta(width)

    def _fit_meta(self, width: int) -> None:
        """Alt satır sığmazsa ön koşul ("Önce: Makine Öğrenmesi") alta iner.

        Üç sütunlu şeritte dar pencerede (1280 px) "0 / 51 bölüm · ~50 saat"
        ile ön koşul yan yana sığmıyor, kartı taşırıyordu.
        """
        yer = self._body_width(width)
        sag = self._pre if self._pre.isVisibleTo(self) else self._meta_right
        gereken = self._meta_left.sizeHint().width() + self.META_GAP + sag.sizeHint().width()
        yon = QHBoxLayout.Direction.LeftToRight if gereken <= yer else QHBoxLayout.Direction.TopToBottom
        if self._meta.direction() != yon:
            yatay = yon == QHBoxLayout.Direction.LeftToRight
            self._meta.setDirection(yon)
            self._meta.setSpacing(self.META_GAP if yatay else 2)
            # Aradaki esneyen boşluk yalnızca yan yanayken; alt altayken satırları ayırmasın.
            bosluk = self._meta.itemAt(1).spacerItem()
            esnek = QSizePolicy.Policy.Expanding if yatay else QSizePolicy.Policy.Minimum
            bosluk.changeSize(0, 0, esnek, QSizePolicy.Policy.Minimum)
            # Üstteki yerleşimlerin boy önbelleği de eskidi (`height_for` hemen soruyor).
            yerlesim = self._meta
            while isinstance(yerlesim, QLayout):
                yerlesim.invalidate()
                yerlesim = yerlesim.parent()

    def _fit_title(self, width: int) -> None:
        """Başlık yer varken tek satırda kalır.

        Sarılan etiketin önerdiği genişlik dar bir tahmin; yanındaki esneyen
        boşluk geri kalanı alıyor ve "Sistem Tasarımı (CI/CD)" yer olduğu
        hâlde "(CI/" diye bölünüyordu (Alican 3 Kasım). En küçük genişlik
        başlığın tek satırlık boyu; kartta o kadar yer yoksa kalan yer.
        """
        yer = self._body_width(width)
        for chip in self._chips:
            if chip.isVisibleTo(self):
                yer -= chip.sizeHint().width() + self.CHIP_GAP
        gereken = self._title.fontMetrics().horizontalAdvance(self._title.text()) + 1
        self._title.setMinimumWidth(max(0, min(gereken, yer)))

    @property
    def track_id(self) -> str:
        return self._track.id

    @property
    def started(self) -> bool:
        return self._started

    @property
    def is_new(self) -> bool:
        return self._new

    @property
    def spin(self) -> RingSpin:
        return self._spin

    def update_progress(self, completed: int, total: int, started: bool) -> None:
        """Patikanın toplam ilerlemesi; `started`: bir bölümünde etkinlik var."""
        self._completed = completed
        self._total = total
        self._started = started
        percent = round(completed * 100 / total) if total else 0
        self._bar.set_percent(percent)
        self._show_progress()
        self._render_meta()

    def set_prerequisite_done(self, done: bool) -> None:
        """Ön koşul patikası bitmişse önerisi gösterilmez."""
        if done != self._prerequisite_done:
            self._prerequisite_done = done
            self._show_progress()

    def set_marks(self, new: bool, route: str) -> None:
        """Etiketler: yeni patika ve rota (`for_you.ROUTE_NEXT` / `ROUTE_LATER` / "")."""
        self._route = route
        if new != self._new:
            self._new = new
            if not new:
                self._spin.stop()
            self._build_halo()
            self.update()
        self._render_chips()
        self._show_chips()

    def _show_chips(self) -> None:
        """Tek etiket, önem sırasıyla: devam ediyor, yeni, rotada.

        Dar kartta iki etiket başlığı ikiye bölüp etiketi kırpıyordu; başladığın
        patika zaten rotandaysa "Devam ediyor" yeterince söylüyor.
        """
        devam = self._started and not self._track.locked
        self._chip.setVisible(devam)
        self._new_chip.setVisible(self._new and not devam)
        self._route_chip.setVisible(bool(self._route) and not devam and not self._new)
        self._fit(self.width())

    def _show_progress(self) -> None:
        acik = not self._track.locked
        devam = acik and self._started
        # Başlanmamış patikada da çubuk 0'da duruyor (Alican 27 Ekim); sağda
        # yüzde yerine önerilen ön koşul.
        on_kosul = acik and not devam and self._prerequisite is not None and not self._prerequisite_done
        self._bar.setVisible(acik)
        self._meta_left.setVisible(acik)
        self._meta_right.setVisible(acik and not on_kosul)
        self._pre.setVisible(on_kosul)
        self._meta_space.setVisible(acik)
        self._show_chips()

    def _render_meta(self) -> None:
        t = self._language.t
        percent = round(self._completed * 100 / self._total) if self._total else 0
        p = PALETTES.get(self._mode, PALETTES["dark"])
        self._meta_left.setText(
            f"<span style='color:{p['text']};font-weight:700'>{self._completed}</span>"
            + t("track.meta_sections", total=self._total)
            + (t("track.meta_hours", hours=self._hours) if self._hours else ""))
        self._meta_right.setText(t("home.percent", value=percent))
        if self._prerequisite is not None:
            self._pre.set_text(t("track.before", name=self._language.pick(self._prerequisite.title)))

    def _render_chips(self) -> None:
        t = self._language.t
        self._chip.setText(t("track.in_progress"))
        self._new_chip.setText(t("track.new"))
        self._route_chip.setText(t("track.route_next" if self._route == for_you.ROUTE_NEXT
                                   else "track.route_later"))

    # --- yeni patika: hâle ve dönen ışık -----------------------------------------

    def _build_halo(self) -> None:
        """Hâle bir kez yumuşak bir resme çiziliyor (`ShadowLayer`), kartın arkasında."""
        if self._halo is not None:
            self._halo.detach()
            self._halo = None
        yuva = self.parentWidget()
        host = yuva.parentWidget() if isinstance(yuva, LiftSlot) else yuva
        if not self._new or host is None:
            return
        renk = QColor(self._track.color)
        alfa = 0.28 if self._mode == "dark" else 0.18
        self._halo = ShadowLayer(self, host, self._mode, False, blur=22, offset_y=0, radius=self._radius,
                                 color=(renk.red(), renk.green(), renk.blue(), round(255 * alfa)))

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        if self._new and (self._halo is None or self._halo.parentWidget() is None):
            self._build_halo()

    def enterEvent(self, event) -> None:  # noqa: N802
        super().enterEvent(event)
        if self._new:
            self._spin.start(1, 0.10, 0.85)

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        if not self._new:
            return
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        p = PALETTES.get(self._mode, PALETTES["dark"])
        kenar = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        g.setBrush(Qt.BrushStyle.NoBrush)
        g.setPen(QPen(QColor(mix(p["border"], self._track.color, 0.55)), 1))
        g.drawRoundedRect(kenar, self._radius, self._radius)
        gorunurluk = self._spin.opacity
        if gorunurluk <= 0.0:
            return
        halka = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        gecis = _ring_gradient(halka, self._spin.angle, self._track.color, self._mode, gorunurluk)
        g.setPen(QPen(QBrush(gecis), 2))
        g.drawRoundedRect(halka, self._radius - 1, self._radius - 1)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.set_card_mode(mode)
        self._bar.set_mode(mode)
        self._pre.set_mode(mode)
        self._render_meta()
        if not self._track.locked:
            refresh_shadow(self, mode)
        if self._new:
            self._build_halo()

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._fit(self.width())

    def retranslate(self) -> None:
        self._title.setText(keep_slash_words(self._language.pick(self._track.title)))
        self._description.setText(keep_slash_words(self._language.pick(self._track.description)))
        self._render_chips()
        self._render_meta()
        self._fit(self.width())


class TrackTile(GlowCard):
    """Bütün patikalar listesindeki sıkı karo (taslak 1, `.tile`).

    Logo, ad (yanında "Devam ediyor" / "YENİ"), sağda "3 / 19 · %16", tek
    satırlık açıklama (sığmazsa "…"; tamamı ipucunda) ve ince çubuk.
    Başlanmamış, ön koşullu patikada açıklama satırının sağında ön koşul hapı;
    yer dar kalırsa kısalan açıklama, hap tam kalır. Kilitli patikada
    açıklamanın yerinde neden açılmadığı; tıklayınca kilit sallanıyor.
    """

    clicked = Signal()

    PAD_X = 16
    PAD_Y = 13
    LOGO = 36
    BAR = 4

    def __init__(self, track: Track, language: LanguageManager, mode: str,
                 prerequisite: Track | None = None, parent: QWidget | None = None) -> None:
        super().__init__(parent, interactive=not track.locked)
        self._track = track
        self._prerequisite = prerequisite
        self._language = language
        self._mode = mode
        self._completed = 0
        self._total = sum(len(chapter.sections) for chapter in track.chapters)
        self._started = False
        self._prerequisite_done = False
        self._new = False
        self._radius = 14
        self.set_accent(track.color)
        self.set_card_mode(mode)
        self.setProperty("variant", "track-tile")
        self.setProperty("locked", "true" if track.locked else "false")
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        if not track.locked:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            apply_shadow(self, mode, radius=14)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(self.PAD_X, self.PAD_Y, self.PAD_X, self.PAD_Y)
        layout.setSpacing(12)
        self._icon = LogoMark(logo_key(track.icon, track.id), track.color, self.LOGO, locked=track.locked)
        self.hovered.connect(self._icon.set_hovered)
        layout.addWidget(self._icon, 0, Qt.AlignmentFlag.AlignVCenter)

        body = QVBoxLayout()
        body.setSpacing(0)
        ust = QHBoxLayout()
        ust.setSpacing(10)
        self._title = ElidedLabel()
        self._title.setProperty("role", "tile-title")
        ust.addWidget(self._title)
        self._chip = QLabel()
        self._chip.setProperty("role", "track-chip")
        self._chip.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._chip.hide()
        ust.addWidget(self._chip, 0, Qt.AlignmentFlag.AlignVCenter)
        self._new_chip = QLabel()
        self._new_chip.setProperty("role", "track-chip-new")
        self._new_chip.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._new_chip.hide()
        ust.addWidget(self._new_chip, 0, Qt.AlignmentFlag.AlignVCenter)
        ust.addStretch(1)
        self._count = QLabel()
        self._count.setProperty("role", "tile-count")
        ust.addWidget(self._count, 0, Qt.AlignmentFlag.AlignVCenter)
        body.addLayout(ust)
        body.addSpacing(2)
        alt = QHBoxLayout()
        alt.setSpacing(8)
        self._line = ElidedLabel()
        self._line.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self._line.setProperty("role", "tile-desc")
        alt.addWidget(self._line, 1)
        self._pre = PrereqChip()
        self._pre.set_mode(mode)
        self._pre.hide()
        alt.addWidget(self._pre, 0, Qt.AlignmentFlag.AlignVCenter)
        body.addLayout(alt)
        body.addSpacing(9)
        self._bar = ProgressBar(f"tile:{track.id}")
        self._bar.setFixedHeight(self.BAR)
        self._bar.set_color(track.color)
        self._bar.set_mode(mode)
        self._bar.setVisible(not track.locked)
        body.addWidget(self._bar)
        layout.addLayout(body, 1)

        self._lock: QLabel | None = None
        if track.locked:
            self._lock = QLabel(self)
            self._lock.setProperty("role", "lock-chip")
            self._lock.setFixedSize(LOCK_BADGE, LOCK_BADGE)
            self._lock.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._lock.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            self._count.hide()
        self._paint_icons()

    @property
    def track_id(self) -> str:
        return self._track.id

    @property
    def started(self) -> bool:
        return self._started

    def height_for(self, width: int) -> int:
        self.ensurePolished()
        for label in (self._title, self._line, self._chip, self._new_chip, self._count, self._pre, self._pre._text):
            label.ensurePolished()
        # Satırlar hap kadar yüksek: etiketli, haplı ve yalın karolar aynı boyda.
        self._line.setMinimumHeight(self._pre.sizeHint().height())
        self._title.setMinimumHeight(max(self._chip.sizeHint().height(), self._new_chip.sizeHint().height()))
        # Sarılan etiket yok: boy genişliğe bağlı değil.
        return self.layout().totalSizeHint().height()

    def update_progress(self, completed: int, total: int, started: bool) -> None:
        self._completed = completed
        self._total = total
        self._started = started
        self._bar.set_percent(round(completed * 100 / total) if total else 0)
        self._chip.setVisible(started and not self._track.locked)
        self._render()

    def set_prerequisite_done(self, done: bool) -> None:
        """Ön koşul patikası bitmişse önerisi gösterilmez."""
        self._prerequisite_done = done
        self._render()

    def _shows_prerequisite(self) -> bool:
        return (self._prerequisite is not None and not self._track.locked
                and not self._started and not self._prerequisite_done)

    def set_new(self, new: bool) -> None:
        self._new = new
        self._new_chip.setVisible(new)

    def _paint_icons(self) -> None:
        if self._lock is not None:
            p = PALETTES.get(self._mode, PALETTES["dark"])
            self._lock.setPixmap(pixmap("lock", p["text_muted"], 12))

    def _reason(self) -> str:
        t = self._language.t
        if self._track.unavailable:
            return t("track.unavailable")
        return t("track.prerequisite") if self._track.prerequisite else t("track.locked")

    def _render(self) -> None:
        t = self._language.t
        pick = self._language.pick
        p = PALETTES.get(self._mode, PALETTES["dark"])
        percent = round(self._completed * 100 / self._total) if self._total else 0
        yuzde = t("home.percent", value=percent)
        self._count.setText(f"<span style='color:{p['text']};font-weight:700'>{self._completed}</span>"
                            f" / {self._total} · {yuzde}")
        aciklama = keep_slash_words(pick(self._track.description))
        self._line.setText(self._reason() if self._track.locked else aciklama)
        # İpucu: adın ve açıklamanın tamamı; durum satırında ön koşul ya da neden.
        if self._track.locked:
            durum, ton = self._reason(), "warning"
        elif self._shows_prerequisite():
            durum, ton = t("track.before", name=pick(self._prerequisite.title)), "muted"
        else:
            durum, ton = "", "muted"
        self._pre.setVisible(self._shows_prerequisite())
        if self._prerequisite is not None:
            self._pre.set_text(t("track.before", name=pick(self._prerequisite.title)))
        from ..widgets import tips

        self.setToolTip(tips.rich(pick(self._track.title), aciklama, durum, ton))

    def _shake_lock(self) -> None:
        """Kilit ±4 px üç kez sallanır, açıklama satırı bir an vurgulanır."""
        import math

        from ..resources.theme.motion import DISTANCE

        kilit = self._lock
        if kilit is None:
            return
        genlik = DISTANCE["shake"]

        def adim(t: float) -> None:
            x = round(genlik * math.sin(t * math.pi * 6) * (1 - t))
            kilit.setContentsMargins(x, 0, -x, 0)

        motion.animate(kilit, "shake", 0.0, 1.0, adim, 300, "linear",
                       on_done=lambda: kilit.setContentsMargins(0, 0, 0, 0))
        vurgu = PALETTES.get(self._mode, PALETTES["dark"])["accent"]
        self._line.setStyleSheet(f"color: {vurgu};")
        QTimer.singleShot(1100, lambda: self._line.setStyleSheet(""))

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if self._track.locked:
            if event.button() == Qt.MouseButton.LeftButton:
                self._shake_lock()
            return
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        QTimer.singleShot(0, self._place_lock)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._place_lock()

    def _place_lock(self) -> None:
        """Kilit rozetini logonun sağ alt köşesine, biraz dışarı taşırarak koyar."""
        if self._lock is None:
            return
        logo = self._icon.geometry()
        self._lock.move(logo.right() - LOCK_BADGE + 6, logo.bottom() - LOCK_BADGE + 6)
        self._lock.raise_()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.set_card_mode(mode)
        self._bar.set_mode(mode)
        self._pre.set_mode(mode)
        self._paint_icons()
        self._render()
        if not self._track.locked:
            refresh_shadow(self, mode)

    def retranslate(self) -> None:
        self._title.setText(keep_slash_words(self._language.pick(self._track.title)))
        self._chip.setText(self._language.t("track.in_progress"))
        self._new_chip.setText(self._language.t("track.new"))
        self._render()


class TrackGroupSection(QWidget):
    """Başlık ("Temeller" + kısa açıklama + sağda "6 patika") ve altında üç sütun.

    `group` yoksa "Senin için" şeridi: başlık sabit metin, sayı yok, kartlar
    her yenilemede seçime göre diziliyor (`show_cards`).
    """

    COLUMNS = 3

    def __init__(self, group: TrackGroup | None, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("role", "bare")
        self._group = group
        self._language = language
        self.cards: list = []
        self._shown: list = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)
        self._header = QWidget()
        self._header.setProperty("role", "bare")
        baslik = QHBoxLayout(self._header)
        baslik.setContentsMargins(SHADOW_ROOM + 2, 0, SHADOW_ROOM + 2, 0)
        baslik.setSpacing(12)
        self._title = QLabel()
        self._title.setProperty("role", "group-title")
        self._description = ElidedLabel()
        self._description.setProperty("role", "group-desc")
        self._count = QLabel()
        self._count.setProperty("role", "group-count")
        baslik.addWidget(self._title, 0, Qt.AlignmentFlag.AlignBaseline)
        baslik.addWidget(self._description, 0, Qt.AlignmentFlag.AlignBaseline)
        baslik.addStretch(1)
        baslik.addWidget(self._count, 0, Qt.AlignmentFlag.AlignBaseline)
        self._count.setVisible(group is not None)
        layout.addWidget(self._header)
        self._header.setVisible(group is None or bool(group.title))

        self._body = QWidget()
        self._body.setProperty("role", "bare")
        self._grid = QGridLayout(self._body)
        self._grid.setContentsMargins(SHADOW_ROOM, 0, SHADOW_ROOM, SHADOW_ROOM)
        self._grid.setHorizontalSpacing(SPACING["md"])
        self._grid.setVerticalSpacing(SPACING["md"] - LIFT - ENTER)
        for column in range(self.COLUMNS):
            self._grid.setColumnStretch(column, 1)
        layout.addWidget(self._body)

    @property
    def group(self) -> TrackGroup | None:
        return self._group

    @property
    def group_id(self) -> str:
        return self._group.id if self._group is not None else FOR_YOU

    def header_text(self) -> str:
        return self._title.text()

    def count_text(self) -> str:
        return self._count.text()

    def add_card(self, card) -> None:
        self.cards.append(card)
        LiftSlot(card, self._body)

    def show_cards(self, visible: list) -> None:
        """Verilen kartları bu sırayla dizer; listede olmayan yer tutmaz.

        `QGridLayout` gizli widget'ın satırını çöktürüyor ve kalan kartlar
        yanlış sütuna kayıyor; bu yüzden ızgara her seferinde baştan kuruluyor.
        """
        while self._grid.count():
            self._grid.takeAt(0)
        for card in self.cards:
            card.parentWidget().setVisible(card in visible)
        self._shown = [card for card in visible if card in self.cards]
        for index, card in enumerate(self._shown):
            self._grid.addWidget(card.parentWidget(), index // self.COLUMNS, index % self.COLUMNS)
        self.setVisible(bool(self._shown))
        self.equalize()

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self.equalize()

    def equalize(self) -> None:
        """Aynı sıradaki kartlar en uzun olanın boyunda."""
        if not self._shown:
            return
        genislik = (self._body.width() - 2 * SHADOW_ROOM
                    - self._grid.horizontalSpacing() * (self.COLUMNS - 1)) // self.COLUMNS
        if genislik <= 0:
            return
        for start in range(0, len(self._shown), self.COLUMNS):
            sira = self._shown[start:start + self.COLUMNS]
            boy = max(card.height_for(genislik) for card in sira)
            for card in sira:
                if card.height() != boy:
                    card.setFixedHeight(boy)

    def retranslate(self) -> None:
        t = self._language.t
        if self._group is None:
            self._title.setText(t("track.for_you"))
            self._description.setText(t("track.for_you_desc"))
        else:
            self._title.setText(self._language.pick(self._group.title))
            self._description.setText(self._language.pick(self._group.description))
            self._count.setText(t("track.group_count", count=len(self._group.tracks)))
        for card in self.cards:
            card.retranslate()
        self.equalize()


# Yeni patika noktasının rengi (prototip `#FB7185`, "YENİ" etiketiyle aynı).
NEW_DOT = "#FB7185"


class JumpChip(QPushButton):
    """Atlama düğmesi: ad, patika sayısı ve yeni patika varsa küçük nokta.

    Nokta açılışta üç kez dalga yayıyor (prototip `pulse`, 2,4 sn); dalga
    düğmenin kendi çiziminde, noktanın yerinden.
    """

    DOT = 7
    PULSE_MS = 2400
    PULSE_REACH = 9.0

    def __init__(self, key: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.key = key
        self._pulse = 0.0
        self.setCheckable(True)
        self.setProperty("variant", "jump-chip")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        satir = QHBoxLayout(self)
        satir.setContentsMargins(14, 7, 14, 7)
        satir.setSpacing(8)
        self._name = QLabel()
        self._name.setProperty("role", "jump-name")
        self._count = QLabel()
        self._count.setProperty("role", "jump-count")
        self._dot = QWidget()
        self._dot.setProperty("role", "bare")
        self._dot.setFixedSize(self.DOT, self.DOT)
        self._dot.hide()
        for parca in (self._name, self._count, self._dot):
            parca.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            satir.addWidget(parca, 0, Qt.AlignmentFlag.AlignVCenter)
        self._count.hide()
        self.toggled.connect(self._mark)
        self._mark(False)

    def set_label(self, name: str, count: int | None) -> None:
        self._name.setText(name)
        self._count.setVisible(count is not None)
        self._count.setText(str(count) if count is not None else "")
        self.updateGeometry()

    def set_dot(self, on: bool) -> None:
        self._dot.setVisible(on)
        self.updateGeometry()
        self.update()

    @property
    def has_dot(self) -> bool:
        return self._dot.isVisibleTo(self)

    def pulse(self) -> None:
        """Noktanın dalgası üç kez (animasyonlar kapalıysa hiç)."""
        if not self.has_dot or not motion.enabled():
            return

        def kez(n: int) -> None:
            if n == 0:
                return
            motion.animate(self, "pulse", 0.0, 1.0, self._set_pulse, self.PULSE_MS, "out",
                           on_done=lambda: kez(n - 1))

        kez(3)

    def _set_pulse(self, value: float) -> None:
        self._pulse = 0.0 if value >= 1.0 else value
        self.update()

    def _mark(self, on: bool) -> None:
        for etiket in (self._name, self._count):
            etiket.setProperty("on", "true" if on else "false")
            repolish(etiket)

    def sizeHint(self) -> QSize:  # noqa: N802
        return self.layout().sizeHint()

    def minimumSizeHint(self) -> QSize:  # noqa: N802
        return self.layout().sizeHint()

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        if not self.has_dot:
            return
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        merkez = QRectF(self._dot.geometry()).center()
        renk = QColor(NEW_DOT)
        g.setPen(Qt.PenStyle.NoPen)
        if 0.0 < self._pulse < 1.0:
            dalga = QColor(renk)
            dalga.setAlphaF(0.6 * (1.0 - self._pulse))
            g.setBrush(dalga)
            yari = self.DOT / 2 + self.PULSE_REACH * self._pulse
            g.drawEllipse(merkez, yari, yari)
        g.setBrush(renk)
        g.drawEllipse(merkez, self.DOT / 2, self.DOT / 2)



class JumpBar(QWidget):
    """Atlama düğmeleri şeridi. Sayfayla kayar, üste gelince orada yapışık kalır.

    Kaydırma alanının içinde değil, onun üstünde duran bir katman:
    `TracksView` onu sayfadaki yer tutucunun hizasına koyuyor (prototip
    `position: sticky`). Üste yapışınca zemini sayfanın rengi, altından geçen
    kartları örtüyor; yerindeyken saydam, karşılama kartının hâlesini kesmiyor.
    """

    PAD = 8

    def __init__(self, keys: list[str], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setProperty("role", "jump-bar")
        self.setProperty("stuck", "false")
        satir = QHBoxLayout(self)
        satir.setContentsMargins(SHADOW_ROOM + 2, self.PAD, SHADOW_ROOM, self.PAD)
        satir.setSpacing(SPACING["sm"])
        self._label = QLabel()
        self._label.setProperty("role", "filter-label")
        satir.addWidget(self._label)
        satir.addSpacing(4)
        self.chips: dict[str, JumpChip] = {}
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        for key in keys:
            chip = JumpChip(key)
            self._group.addButton(chip)
            self.chips[key] = chip
            satir.addWidget(chip)
        satir.addStretch(1)

    def set_label(self, text: str) -> None:
        self._label.setText(text)

    def bar_height(self) -> int:
        return self.layout().sizeHint().height()

    def set_stuck(self, stuck: bool) -> None:
        deger = "true" if stuck else "false"
        if self.property("stuck") != deger:
            self.setProperty("stuck", deger)
            repolish(self)


class TracksView(QWidget):
    """Ana ekran (taslak 1): karşılama kartı, atlama düğmeleri, "Senin için"
    şeridi ve gruplara ayrılmış bütün patikalar (sıkı karolar)."""

    track_opened = Signal(str)
    resume_requested = Signal()
    review_requested = Signal()

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
        # Bütün patikaların karoları (gruplardaki sırayla); tur da bunlara bakıyor.
        self._cards: list[TrackTile] = []
        self._groups: list[TrackGroupSection] = []
        # "Senin için"in büyük kartları ilk gerektiğinde kuruluyor.
        self._big: dict[str, TrackCard] = {}
        self._progress: dict[str, tuple[int, int, bool]] = {}
        self._new: set[str] = set()
        self._picks: list[for_you.Pick] = []
        self._watched_window: QWidget | None = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        column = QWidget()
        self._page_layout = QVBoxLayout(column)
        # Yanlarda gölge payı kadar az: grupların içindeki ızgara o payı
        # kendisi bırakıyor, kartlar yine karşılama kartıyla aynı hizada.
        self._page_layout.setContentsMargins(
            SPACING["xl"] - SHADOW_ROOM, SPACING["xl"], SPACING["xl"] - SHADOW_ROOM, SPACING["xxl"]
        )
        self._page_layout.setSpacing(0)

        self._hero = HeroCard(language)
        self._hero.resume.connect(self.resume_requested)
        self._hero.review.connect(self.review_requested)
        hero_satir = QHBoxLayout()
        hero_satir.setContentsMargins(SHADOW_ROOM, 0, SHADOW_ROOM, 0)
        hero_satir.addWidget(self._hero, 1)
        self._page_layout.addLayout(hero_satir)
        # Prototip: şeridin üstünde 28 px, şeridin kendi iç boşluğu 8 px.
        self._page_layout.addSpacing(28 - JumpBar.PAD)

        keys = [FOR_YOU] + [g.id for g in catalog.groups if g.title]
        self._jump = JumpBar(keys, self)
        for key, chip in self._jump.chips.items():
            chip.clicked.connect(lambda _=False, k=key: self.jump_to(k))
        self._jump.chips[FOR_YOU].setChecked(True)
        self._jump_slot = QWidget()
        self._jump_slot.setProperty("role", "bare")
        self._jump_slot.installEventFilter(self)
        self._page_layout.addWidget(self._jump_slot)

        self._for_you = TrackGroupSection(None, language)
        self._page_layout.addSpacing(28 - JumpBar.PAD)
        self._page_layout.addWidget(self._for_you)
        self._build_tiles()
        self._page_layout.addStretch(1)

        # Sütun prototipin sayfa genişliğinde (karşılama kartı da onunla).
        self._scroll = scroll_page(centered_column(column, max_width=JOURNEY_WIDTH + 2 * SPACING["xl"]))
        self._scroll.verticalScrollBar().valueChanged.connect(self._on_scroll)
        outer.addWidget(self._scroll)
        self._jump.raise_()
        self._entered = False

    # --- kurulum ------------------------------------------------------------------

    def _build_tiles(self) -> None:
        by_id = {track.id: track for track in self._catalog.tracks}
        for group in self._catalog.groups:
            section = TrackGroupSection(group, self._language)
            for track in group.tracks:
                tile = TrackTile(track, self._language, self._mode,
                                 prerequisite=by_id.get(track.prerequisite))
                tile.clicked.connect(lambda t=track.id: self.track_opened.emit(t))
                section.add_card(tile)
                self._cards.append(tile)
            # Gruplar arası 28 px; önceki ızgaranın alttaki gölge payı da sayılıyor.
            self._page_layout.addSpacing(28 - SHADOW_ROOM)
            self._page_layout.addWidget(section)
            section.show_cards(section.cards)
            self._groups.append(section)

    def _big_card(self, track_id: str) -> TrackCard:
        kart = self._big.get(track_id)
        if kart is None:
            track = self._catalog.track(track_id)
            kart = TrackCard(track, self._language, self._mode,
                             prerequisite=self._catalog.track(track.prerequisite))
            kart.clicked.connect(lambda t=track_id: self.track_opened.emit(t))
            self._for_you.add_card(kart)
            kart.retranslate()
            self._big[track_id] = kart
        return kart

    # --- atlama şeridi ------------------------------------------------------------

    def _anchor(self, key: str) -> QWidget | None:
        if key == FOR_YOU:
            return self._for_you if self._for_you.isVisibleTo(self) else (self._groups[0] if self._groups else None)
        return next((g for g in self._groups if g.group_id == key), None)

    def scroll_target(self, key: str) -> int:
        """Grubun başlığı yapışık şeridin hemen altına gelecek kaydırma değeri."""
        hedef = self._anchor(key)
        cubuk = self._scroll.verticalScrollBar()
        if hedef is None:
            return cubuk.value()
        y = hedef.mapTo(self._scroll.widget(), QPoint(0, 0)).y()
        return max(0, min(cubuk.maximum(), y - self._jump.bar_height() - 4))

    def jump_to(self, key: str, animate: bool = True) -> None:
        """Atlama düğmesi: süzmüyor, sayfayı o bölüme (yumuşakça) kaydırıyor."""
        chip = self._jump.chips.get(key)
        if chip is not None:
            chip.setChecked(True)
        cubuk = self._scroll.verticalScrollBar()
        hedef = self.scroll_target(key)
        if not animate:
            motion.stop(self, "jump")
            cubuk.setValue(hedef)
            return
        motion.animate(self, "jump", float(cubuk.value()), float(hedef),
                       lambda v: cubuk.setValue(round(v)), "long", "out")

    def scroll_to_top(self) -> None:
        self.jump_to(FOR_YOU, animate=False)
        self._scroll.verticalScrollBar().setValue(0)

    def reveal(self, widget: QWidget) -> None:
        """Parçayı (tur için) yapışık şeridin altında görünür yapar."""
        cubuk = self._scroll.verticalScrollBar()
        y = widget.mapTo(self._scroll.widget(), QPoint(0, 0)).y()
        alt = y + widget.height() - self._scroll.viewport().height() + SPACING["lg"]
        ust = y - self._jump.bar_height() - SPACING["lg"]
        if cubuk.value() > ust:
            cubuk.setValue(max(0, ust))
        elif cubuk.value() < alt:
            cubuk.setValue(min(cubuk.maximum(), alt))

    def _place_jump(self) -> None:
        """Şeridi yer tutucunun hizasına koyar; yukarı kayınca üstte durur."""
        self._jump_slot.setFixedHeight(self._jump.bar_height())
        yer = self._jump_slot.mapTo(self, QPoint(0, 0))
        self._jump.setGeometry(yer.x(), max(0, yer.y()), self._jump_slot.width(), self._jump.bar_height())
        self._jump.set_stuck(yer.y() < 0)
        self._jump.raise_()

    def _on_scroll(self, _value: int = 0) -> None:
        self._place_jump()
        self._update_glow()

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        if obj is self._jump_slot and event.type() in (QEvent.Type.Move, QEvent.Type.Resize):
            self._place_jump()
        elif obj is self._watched_window and event.type() == QEvent.Type.ActivationChange:
            self._update_glow()
        return False

    # --- yeni patikanın parlaması ---------------------------------------------------

    def _card_on_screen(self, card: QWidget) -> bool:
        if not card.isVisibleTo(self):
            return False
        viewport = self._scroll.viewport()
        yer = card.mapTo(viewport, QPoint(0, 0))
        return viewport.rect().intersects(QRect(yer, card.size()))

    def _update_glow(self) -> None:
        """Işık yalnızca ekran görünür, pencere etkin ve kart görünür alandayken döner."""
        acik = self.isVisible() and self.window().isActiveWindow()
        for kart in self._big.values():
            if kart.is_new:
                kart.spin.set_allowed(acik and self._card_on_screen(kart))

    def _start_glow(self) -> None:
        for kart in self._big.values():
            if kart.is_new and kart.isVisibleTo(self):
                kart.spin.start(3, 0.04, 0.92)
        for chip in self._jump.chips.values():
            chip.pulse()
        self._update_glow()

    def glow_ticks(self) -> int:
        """Ölçüm için: dönen ışığın zamanlayıcısı toplam kaç kez tetiklendi."""
        return sum(kart.spin.ticks for kart in self._big.values())

    def note_opened(self, track_id: str) -> None:
        """Patika açıldı: yeni işareti kalıcı olarak söner."""
        if new_tracks.mark_opened(self._store, track_id) and track_id in self._new:
            self._new.discard(track_id)
            self._apply_marks()

    # --- gösterim -----------------------------------------------------------------

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        pencere = self.window()
        if pencere is not self._watched_window:
            if self._watched_window is not None:
                self._watched_window.removeEventFilter(self)
            pencere.installEventFilter(self)
            self._watched_window = pencere
        QTimer.singleShot(0, self, self._place_jump)
        # Ekran her açılışında yeni patikanın ışığı üç tur döner.
        QTimer.singleShot(0, self, self._start_glow)
        # Oturumdaki ilk gösterimde prototipteki gibi: karşılama kartı ve
        # şerit 16 px aşağıdan (ekranın `pgIn`'i), kartlar sırayla (`sIn`).
        if not self._entered:
            self._entered = True
            from ..widgets.pop_effect import enter
            hepsi = [enter(self._hero, 16, "spring", hold=True),
                     enter(self._jump, 16, "spring", hold=True)]
            kartlar = [k for k in self._big.values() if k.isVisibleTo(self)] + self._cards
            hepsi += stagger_cards(kartlar)
            hepsi = [b for b in hepsi if b]
            # İlk çizim bittikten sonra başlasın (bkz. `enter`, `hold`).
            QTimer.singleShot(0, self, lambda: QTimer.singleShot(
                16, self, lambda: [b() for b in hepsi]))

    def hideEvent(self, event) -> None:  # noqa: N802
        super().hideEvent(event)
        self._update_glow()

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        QTimer.singleShot(0, self, self._on_scroll)

    # --- veri ---------------------------------------------------------------------

    def _chapter_progress(self, chapter, active) -> tuple[int, int, bool]:
        """Bir modülde kaç bölüm tamamlandı, kaç bölüm var, etkinlik var mı."""
        biten = sum(1 for section in chapter.sections if is_completed(self._store, section, active))
        basladi = any((chapter.id, section.id) in active for section in chapter.sections)
        return biten, len(chapter.sections), basladi

    def _first_install(self) -> bool:
        from .welcome import SETTING_KEY

        return self._store.setting(SETTING_KEY, "") == ""

    def _choose(self, active) -> list[for_you.Pick]:
        """"Senin için"in patikaları (`core.for_you`)."""
        from .roadmap_view import ROUTE_SETTING, load_routes

        acik = [t for t in self._catalog.tracks if not t.locked]
        basladi = [t.id for t in acik if self._progress.get(t.id, (0, 0, False))[2]]
        son_bitirme = {
            t.id: max((active.get((c.id, s.id)) or "" for c in t.chapters for s in c.sections), default="")
            for t in acik
        }
        son = self._store.last_visited()
        son_patika = next((t.id for t in acik if son and any(c.id == son[0] for c in t.chapters)), None)
        sirali = for_you.order_started(basladi, son_patika, son_bitirme)
        yeni = [t.id for g in self._catalog.groups for t in g.tracks if t.id in self._new and not t.locked]
        rota = for_you.route_for(load_routes(), self._store.setting(ROUTE_SETTING, ""))
        siradaki, sonraki = for_you.route_tracks(self._catalog, self._store, rota)
        return for_you.pick(sirali, yeni, siradaki, sonraki)

    def _prerequisite_done(self, track_id: str) -> bool:
        """Patikanın önerilen ön koşulu bitirildi mi (bütün bölümleri tamam)?"""
        track = self._catalog.track(track_id)
        done, total, _ = self._progress.get(track.prerequisite if track else "", (0, 0, False))
        return total > 0 and done == total

    def _apply_marks(self) -> None:
        """Seçimi ve yeni işaretlerini kartlara, karolara ve düğmelere yazar."""
        kartlar = []
        for secim in self._picks:
            kart = self._big_card(secim.track_id)
            rota = next((tag for tag in (for_you.ROUTE_NEXT, for_you.ROUTE_LATER) if tag in secim.tags), "")
            kart.set_marks(secim.track_id in self._new, rota)
            kartlar.append(kart)
        for kart in self._big.values():
            if kart not in kartlar:
                kart.set_marks(False, "")
            done, total, started = self._progress.get(kart.track_id, (0, 0, False))
            kart.set_prerequisite_done(self._prerequisite_done(kart.track_id))
            kart.update_progress(done, total, started)
        self._for_you.show_cards(kartlar)
        for tile in self._cards:
            tile.set_new(tile.track_id in self._new)
            tile.set_prerequisite_done(self._prerequisite_done(tile.track_id))
        for section in self._groups:
            chip = self._jump.chips.get(section.group_id)
            if chip is not None:
                chip.set_dot(any(tile.track_id in self._new for tile in section.cards))
            # "YENİ" ve "Devam ediyor" etiketi satırı biraz uzatıyor.
            section.equalize()
        self._jump.chips[FOR_YOU].setVisible(bool(kartlar))
        QTimer.singleShot(0, self, self._update_glow)

    def refresh(self) -> None:
        toplam = 0
        biten = 0
        active = self._store.active_sections()

        for tile in self._cards:
            track = self._catalog.track(tile.track_id)
            if track is None:
                continue
            t_biten = t_toplam = 0
            t_basladi = False
            for chapter in track.chapters:
                b, s, basladi = self._chapter_progress(chapter, active)
                t_biten += b
                t_toplam += s
                t_basladi = t_basladi or basladi
            self._progress[track.id] = (t_biten, t_toplam, t_basladi)
            tile.update_progress(t_biten, t_toplam, t_basladi)
            biten += t_biten
            toplam += t_toplam

        from ..version import APP_VERSION

        self._new = new_tracks.refresh(
            self._store, [(t.id, t.since) for t in self._catalog.tracks if not t.locked],
            APP_VERSION, date.today(), self._first_install(),
            {kimlik for kimlik, (_, _, basladi) in self._progress.items() if basladi})
        self._picks = self._choose(active)

        self._hero.update_stats(
            name=self._store.profile().get("first_name", ""),
            resume_text=self._resume_text(),
            sections=biten,
            total_sections=toplam,
            exercises=self._store.solved_exercise_count(),
            total_exercises=sum(
                section.exercise_count for section in self._catalog.all_sections
            ),
            streak=self._store.streak(),
            progress=round(biten * 100 / toplam) if toplam else 0,
            studied_today=self._store.last_study_day() == date.today(),
            goal=weekly_goal.current(self._store),
            reviews=review_box.today_count(self._store),
        )
        self.retranslate()
        self._apply_marks()

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
        # Hiç bölüm açılmamışsa "kaldığı yer" yok (Mac deneme raporu, 13 Kasım).
        return self._language.t(
            "home.resume" if last is not None else "home.start",
            chapter=self._language.pick(chapter.title) if chapter else "",
            section=self._language.pick(section.title),
        )

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._hero.set_mode(mode)
        for card in [*self._cards, *self._big.values()]:
            card.set_mode(mode)

    def retranslate(self) -> None:
        t = self._language.t
        self._jump.set_label(t("track.jump_label"))
        self._jump.chips[FOR_YOU].set_label(t("track.for_you"), None)
        for section in self._groups:
            chip = self._jump.chips.get(section.group_id)
            if chip is not None:
                chip.set_label(self._language.pick(section.group.title), len(section.group.tracks))
        # "Kaldığın yer" satırı bölüm adını taşıyor ve o ad dile bağlı;
        # yeniden üretilmesi gerekiyor. **`refresh()` çağrılmıyor:** o da
        # sonunda `retranslate` çağırıyor ve ikisi birbirini sonsuza kadar
        # tetikliyor (denendi, `RecursionError`).
        self._hero.set_resume(self._resume_text())
        self._hero.retranslate()
        self._for_you.retranslate()
        for section in self._groups:
            section.retranslate()
        QTimer.singleShot(0, self, self._place_jump)


class ModulesView(QWidget):
    """Modül kartlarının listelendiği ana ekran."""

    module_opened = Signal(str)
    resume_requested = Signal()
    review_requested = Signal()

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
        self._hero.review.connect(self.review_requested)
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
        active = self._store.active_sections()

        for card in self._cards:
            chapter = self._catalog.chapter(card.chapter_id)
            if chapter is None:
                continue

            done = sum(1 for section in chapter.sections
                       if is_completed(self._store, section, active))

            card.update_progress(done, len(chapter.sections))
            card.retranslate()
            total_sections += len(chapter.sections)
            completed_sections += done

        total_exercises = sum(
            section.exercise_count for section in self._catalog.all_sections
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
            goal=weekly_goal.current(self._store),
            reviews=review_box.today_count(self._store),
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

        # Hiç bölüm açılmamışsa "kaldığı yer" yok (Mac deneme raporu, 13 Kasım).
        return self._language.t(
            "home.resume" if last is not None else "home.start",
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


class PlacementBanner(QFrame):
    """Yolun başında "seviyeni belirle" kartı (`core/placement.py`).

    Daha önce girildiyse sonucu yazıyor ve "Yeniden dene" diyor.
    """

    requested = Signal()
    # İkinci düğme (tekrar kartında "Alıştırma tekrarı").
    secondary_requested = Signal()

    def __init__(self, title: str, text: str, button: str, mode: str,
                 icon_name: str = "target", secondary: str | None = None) -> None:
        super().__init__()
        p = PALETTES.get(mode, PALETTES["light"])
        self.setObjectName("placementBanner")
        self.setStyleSheet(
            f"QFrame#placementBanner {{ background: {p['accent_soft']}; border: 1px solid {mix(p['accent'], p['surface'], 0.55)};"
            f" border-radius: 16px; }}"
            "QFrame#placementBanner QLabel { background: transparent; }"
        )
        satir = QHBoxLayout(self)
        satir.setContentsMargins(SPACING["lg"], SPACING["md"], SPACING["md"], SPACING["md"])
        satir.setSpacing(SPACING["md"])
        simge = QLabel()
        simge.setPixmap(pixmap(icon_name, p["accent"], 26))
        satir.addWidget(simge, 0, Qt.AlignmentFlag.AlignVCenter)
        yazilar = QVBoxLayout()
        yazilar.setSpacing(2)
        baslik = QLabel(title)
        baslik.setStyleSheet(f"color: {p['text']}; font-weight: 650; font-size: 14.5px;")
        yazilar.addWidget(baslik)
        metin = QLabel(text)
        metin.setWordWrap(True)
        metin.setStyleSheet(f"color: {p['text_muted']}; font-size: 13px;")
        yazilar.addWidget(metin)
        satir.addLayout(yazilar, 1)
        self.button = QPushButton(button)
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.clicked.connect(self.requested)
        # Önce karta eklenir, sonra görünürlüğü verilir: üst penceresi
        # yokken `setVisible(True)` düğmeyi bir an ayrı pencere olarak açıyordu.
        satir.addWidget(self.button, 0, Qt.AlignmentFlag.AlignVCenter)
        self.button.setVisible(bool(button))
        self.secondary_button = None
        if secondary:
            self.secondary_button = QPushButton(secondary)
            self.secondary_button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.secondary_button.clicked.connect(self.secondary_requested)
            satir.addWidget(self.secondary_button, 0, Qt.AlignmentFlag.AlignVCenter)


# Oturum boyunca: hangi modülün yolu görüldü, görüldüğünde hangi bölümler
# bitmişti. Yola dönüldüğünde aradaki fark "yeni biten" sayılıp canlandırılıyor.
_SEEN_CHAPTERS: set[str] = set()
_SEEN_DONE: dict[str, set[str]] = {}


class PathView(QWidget):
    """Bir modülün bölümlerini yol hâlinde gösterir."""

    section_opened = Signal(str, str)
    back_requested = Signal()
    # Seviye tespiti kaydedildi: kilitler değişti, başka ekranlar tazelensin.
    placement_finished = Signal()
    # Tekrar sınavında "Derse git" (arama sonucu biçiminde hedef).
    spot_requested = Signal(dict)

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
        # Açılıştaki çizim animasyonu (800 ms) eski çizgilere bağlı; yol o
        # sırada yeniden kurulursa silinmiş çizgiye ulaşıp çöküyordu.
        motion.stop(self, "draw")
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

        kart = self._placement_banner(chapter, outline)
        if kart is not None:
            self._layout.addWidget(kart)

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
        state = self._store.section_state(chapter_id, section.id, section.exercise_ids)
        return state.status(section.requires_quiz, section.requires_exercises)

    def _placement_banner(self, chapter, outline: list):
        """Seviye tespit kartı; modülde yeterli bölüm yoksa ya da bütün
        bölümler bittiyse yok. Kilit kaldırılmışken de görünüyor (Alican):
        kişi nereden başlayacağını, neyi tekrar etmesi gerektiğini görsün."""
        from ..core import exercise_practice, placement, practice_exam

        kartlar = []
        t = self._language.t
        bolumler = [s for s in outline if not isinstance(s, dict)]
        hepsi_bitti = bool(bolumler) and all(
            self._state_of(chapter.id, s) == "completed" for s in bolumler)
        if placement.available(chapter, self._language.language) and not hepsi_bitti:
            sonuc = placement.load(self._store, chapter.id)
            if sonuc:
                acilan = placement.reach_index(self._store, chapter) + 1
                kart = PlacementBanner(t("placement.banner_done_title"),
                                       t("placement.banner_done", count=acilan),
                                       t("placement.retry"), self._mode)
            else:
                kart = PlacementBanner(t("placement.banner_title"), t("placement.banner_text"),
                                       t("placement.banner_button"), self._mode)
            kart.requested.connect(lambda: self.open_placement(chapter.id))
            self._placement = kart
            kartlar.append(kart)
        # Tekrar sınavı: en az üç bölüm bitince (Alican 27 Ekim). Seviye
        # tespit kartı onaylı davranışıyla yerinde kalıyor; ikisi alt alta.
        # Alıştırma tekrarı aynı kartta ikinci düğme (Alican 7 Kasım).
        biten = len(practice_exam.done_sections(chapter, self._store, self._language.language))
        sinav = biten >= practice_exam.MIN_DONE
        alistirma = exercise_practice.available(chapter, self._store)
        if sinav or alistirma:
            parcalar = []
            if sinav:
                son = practice_exam.load(self._store, chapter.id)
                if son:
                    parcalar.append(t("practice.banner_last", correct=son.get("correct", 0),
                                      total=son.get("total", 0)))
                parcalar.append(t("practice.banner_text", count=biten,
                                  questions=practice_exam.TOTAL))
            if alistirma:
                parcalar.append(t("xpractice.banner_text", count=exercise_practice.TOTAL))
                son = exercise_practice.load(self._store, chapter.id)
                if son:
                    parcalar.append(t("xpractice.banner_last", solved=son.get("solved", 0),
                                      total=son.get("total", 0)))
            kart = PlacementBanner(
                t("practice.title") if sinav else t("xpractice.title"), " ".join(parcalar),
                t("practice.start") if sinav else "", self._mode, icon_name="repeat",
                secondary=t("xpractice.button") if alistirma else None)
            kart.requested.connect(lambda: self.open_practice(chapter.id))
            kart.secondary_requested.connect(lambda: self.open_exercise_practice(chapter.id))
            self._practice = kart
            kartlar.append(kart)
        if not kartlar:
            return None
        # Altında nefes payı: yol düğmeleri komşularına biniyor (`OverlapColumn`).
        sarmal = QWidget()
        sarmal.setProperty("role", "bare")
        duzen = QVBoxLayout(sarmal)
        duzen.setContentsMargins(0, 0, 0, SPACING["xl"])
        duzen.setSpacing(SPACING["sm"])
        for kart in kartlar:
            duzen.addWidget(kart)
        return sarmal

    def open_practice(self, chapter_id: str, rng=None):
        """Tekrar sınavı penceresi; kapanınca kart son sonucu gösteriyor."""
        from .modal import Backdrop
        from .review_dialog import PracticeDialog

        chapter = self._catalog.chapter(chapter_id)
        if chapter is None:
            return None
        kok = self.window()
        perde = Backdrop(kok)
        perde.show()
        dialog = PracticeDialog(self._language, self._store, chapter, self._mode, kok, rng=rng)
        self.practice_dialog = dialog

        def kapandi(_sonuc) -> None:
            perde.deleteLater()
            if dialog.answered:
                self._rebuild()
                # Seri ve tekrar kutusu değişti: karşılama kartları da yenilensin.
                self.placement_finished.emit()
            dialog.deleteLater()
            self.practice_dialog = None

        dialog.finished.connect(kapandi)
        dialog.spot_requested.connect(self.spot_requested)
        dialog.open()
        return dialog

    def open_exercise_practice(self, chapter_id: str, rng=None, today=None):
        """Alıştırma tekrarı; ana pencerenin ekran alanını (şeritler dışı)
        kaplayan sayfa. Bir şey çözüldüyse kart ve seri tazeleniyor."""
        from .exercise_practice_dialog import ExercisePracticeDialog

        chapter = self._catalog.chapter(chapter_id)
        if chapter is None:
            return None
        kok = self.window()
        sahip = getattr(kok, "_stack", None) or kok
        dialog = ExercisePracticeDialog(self._language, self._store, chapter, self._mode, sahip,
                                        today=today, rng=rng)
        self.exercise_practice_dialog = dialog
        hedef: list[tuple[str, str]] = []

        def kapandi(_sonuc) -> None:
            if dialog.solved_count:
                self._rebuild()
                self.placement_finished.emit()
            dialog.deleteLater()
            self.exercise_practice_dialog = None
            if hedef:
                self.section_opened.emit(*hedef[0])

        dialog.section_requested.connect(lambda c, s: hedef.append((c, s)))
        dialog.finished.connect(kapandi)
        dialog.show()
        dialog.raise_()
        dialog.setFocus()
        return dialog

    def open_placement(self, chapter_id: str, rng=None):
        """Seviye tespit penceresini açar; sonuç kaydedildiyse yolu yeniden kurar."""
        from .modal import Backdrop
        from .placement_dialog import PlacementDialog

        chapter = self._catalog.chapter(chapter_id)
        if chapter is None:
            return None
        kok = self.window()
        perde = Backdrop(kok)
        perde.show()
        dialog = PlacementDialog(self._language, self._store, chapter, self._mode, kok, rng=rng)
        self.placement_dialog = dialog
        dialog.finished.connect(lambda _r: self._placement_closed(perde, dialog))
        dialog.open()
        return dialog

    def _placement_closed(self, perde, dialog) -> None:
        perde.deleteLater()
        if dialog.done_sections:
            self._rebuild()
            self.placement_finished.emit()
        dialog.deleteLater()
        self.placement_dialog = None

    def _current_index(self, outline: list, chapter_id: str) -> int:
        # Seviye tespitinde atlanan bölümler "şu an buradasın" olmuyor:
        # işaret bilinen son bölümün arkasındaki ilk tamamlanmamış bölümde.
        from ..core.placement import reach_index

        atla = reach_index(self._store, self._catalog.chapter(chapter_id))
        for index, section in enumerate(outline):
            if isinstance(section, dict) or index <= atla:
                continue
            if self._state_of(chapter_id, section) != "completed":
                return index
        return -1

    def _caption_for(self, section, state: str, blocker=None) -> str:
        progress = self._store.section_state(
            self._chapter_id, section.id, section.exercise_ids
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
    # Karşılama kartındaki "Tekrar et": tekrar kutusu penceresi.
    review_requested = Signal()
    spot_requested = Signal(dict)

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
        self.tracks.review_requested.connect(self.review_requested)
        self.modules.review_requested.connect(self.review_requested)
        self.modules.module_opened.connect(self.open_module)
        self.path.section_opened.connect(self.section_opened)
        self.path.spot_requested.connect(self.spot_requested)

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
        # Karttan da Rotalar'dan da açılınca yeni işareti söner. Bölümü doğrudan
        # açan (arama) patikada etkinlik bırakıyor; başlanmış patika da yeni sayılmıyor.
        self.tracks.note_opened(track_id)
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
