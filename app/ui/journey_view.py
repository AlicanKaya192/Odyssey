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

from PySide6.QtCore import QPointF, QRectF, QSize, Qt, Signal
from PySide6.QtGui import (
    QColor,
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
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..core.catalog import Catalog, Chapter, Track
from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..core.unlock import blocking_section
from ..resources.icons import icon, pixmap
from ..resources.theme.tokens import CONTENT_WIDTH, NODE_STATES, PALETTES, RADIUS, SPACING
from ..widgets.common import Card, ElidedText, StatBlock, horizontal_rule, section_label
from ..widgets.streak_flame import flame_pixmap, next_tier, tier_for
from ..widgets.effects import apply_shadow, refresh_shadow, repolish

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

    row.addStretch(1)
    row.addWidget(inner, 10)
    row.addStretch(1)
    return holder


class HeroCard(QFrame):
    """Üstteki karşılama kartı: kaldığın yer ve özet sayılar.

    Zemini kendisi çiziyor: çivit→mor geçiş ve üstünde yarı saydam
    daireler (Alican'ın verdiği örneğe göre). Renkler temadan değil
    logodan geliyor; koyu temanın açık vurgu rengiyle zemin pastel
    kalıyor, beyaz yazı zor okunuyordu.
    """

    resume = Signal()

    GRADIENT = ("#4F46E5", "#7C3AED")

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._name = ""
        self._resume = ""
        self._streak = 0
        self._progress = 0
        self.setProperty("role", "hero")
        apply_shadow(self, "light", strong=True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["xl"], 28, SPACING["xl"], 26)
        layout.setSpacing(SPACING["sm"])

        self._title = QLabel()
        self._title.setStyleSheet(
            "color:#FFFFFF; font-size:22px; font-weight:700; background:transparent;"
        )
        layout.addWidget(self._title)

        self._subtitle = QLabel()
        self._subtitle.setStyleSheet(
            "color:rgba(255,255,255,0.86); font-size:14px; font-weight:500;"
            " background:transparent;"
        )
        self._subtitle.setWordWrap(True)
        layout.addWidget(self._subtitle)
        layout.addSpacing(SPACING["md"])

        stats = QHBoxLayout()
        stats.setSpacing(56)
        self._stats = {
            key: StatBlock("0", "", inverse=True)
            for key in ("sections", "exercises", "streak", "progress")
        }
        for block in self._stats.values():
            # Sayılar etiketleriyle birlikte sola yaslı (örnekteki gibi).
            block.set_centered(False)
            block.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            block.setStyleSheet("background: transparent;")
            stats.addWidget(block)
        stats.addStretch(1)
        layout.addLayout(stats)

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
        # Sağda kartın dışına taşan büyük daire, solda altta küçüğü.
        for cx, cy, r, alpha in (
            (w - 40, h * 0.42, h * 0.95, 20),
            (w - 150, h + 30, h * 0.55, 12),
            (30, h + 10, h * 0.42, 14),
        ):
            color = QColor(255, 255, 255, alpha)
            painter.setBrush(color)
            painter.drawEllipse(QPointF(cx, cy), r, r)

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

        self._stats["sections"].set_value(f"{sections}/{total_sections}")
        self._stats["exercises"].set_value(f"{exercises}/{total_exercises}")
        self._stats["streak"].set_value(str(streak))
        self._progress = progress
        self._streak = streak
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
        self._title.setText(f"{selam} 👋")
        self._subtitle.setText(self._resume)

    def _render_flame(self) -> None:
        """Serinin alevi ve ipucu: şu anki aşama, sonrakine kaç gün kaldı."""
        t = self._language.t
        tier = tier_for(self._streak)
        sonraki = next_tier(self._streak)
        parcalar = [
            t(f"streak.tier_{tier.key}") if tier else t("streak.none"),
        ]
        if sonraki is not None:
            parcalar.append(
                t(
                    "streak.next",
                    days=sonraki.min_days - self._streak,
                    name=t(f"streak.tier_{sonraki.key}"),
                )
            )
        self._stats["streak"].set_icon(
            flame_pixmap(self._streak, self.devicePixelRatioF() or 1.0),
            " · ".join(parcalar),
        )

    def retranslate(self) -> None:
        self._render_greeting()
        for key in self._stats:
            self._stats[key].set_label(self._language.t(f"home.stat_{key}"))
        # Yüzde işareti dile göre: Türkçede önde (%40), İngilizcede sonda (40%).
        self._stats["progress"].set_value(self._language.t("home.percent", value=self._progress))
        self._render_flame()


class ModuleCard(QFrame):
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
        self.setProperty("variant", "module")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        apply_shadow(self, mode)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"])
        layout.setSpacing(SPACING["sm"])

        header = QHBoxLayout()
        header.setSpacing(SPACING["sm"])

        self._icon = QLabel()
        self._icon.setPixmap(pixmap("book", chapter.color, 22))
        self._icon.setFixedWidth(24)
        header.addWidget(self._icon, 0, Qt.AlignmentFlag.AlignTop)

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

        self._bar = QProgressBar()
        self._bar.setTextVisible(False)
        layout.addWidget(self._bar)

        self._caption = QLabel()
        self._caption.setProperty("role", "muted")
        layout.addWidget(self._caption)

    @property
    def chapter_id(self) -> str:
        return self._chapter.id

    def update_progress(self, completed: int, total: int) -> None:
        percent = round(completed * 100 / total) if total else 0
        self._bar.setRange(0, 100)
        self._bar.setValue(percent)
        self._caption.setText(
            self._language.t("module.progress", done=completed, total=total, percent=percent)
        )

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def set_mode(self, mode: str) -> None:
        refresh_shadow(self, mode)

    def retranslate(self) -> None:
        self._title.setText(self._language.pick(self._chapter.title))
        self._description.setText(self._language.pick(self._chapter.description))


class TrackCard(QFrame):
    """Bir öğrenme patikasını temsil eden kart.

    İçeriği henüz yazılmamış patika kilitli: soluk, tıklanmıyor, köşesinde
    kilit simgesi duruyor. Kilitlileri gizlemek yerine göstermek, uygulamanın
    nereye gittiğini baştan anlatıyor.
    """

    clicked = Signal()

    def __init__(
        self,
        track: Track,
        language: LanguageManager,
        mode: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._track = track
        self._language = language
        self._completed = 0
        self._total = 0
        self.setProperty("variant", "module")
        self.setProperty("locked", "true" if track.locked else "false")
        # Bütün kartlar aynı boyda: genişliği ızgaranın eşit sütunları,
        # yüksekliği `_fix_height` veriyor. Önceden içerik boyu belirliyordu
        # ve on üç kartta on bir farklı boy vardı (ölçüldü); uzun başlıklar
        # taşıp kesiliyordu.
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)

        if not track.locked:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            apply_shadow(self, mode)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"]
        )
        layout.setSpacing(SPACING["sm"])

        header = QHBoxLayout()
        header.setSpacing(SPACING["sm"])

        self._icon = QLabel()
        self._icon.setPixmap(pixmap(track.icon, track.color, 26))
        self._icon.setFixedWidth(28)
        header.addWidget(self._icon, 0, Qt.AlignmentFlag.AlignVCenter)

        # Başlığa her kartta iki satırlık yer ayrılıyor ve dikeyde
        # ortalanıyor: "Doğal Dil İşleme" iki satır, "SQL" tek satır olsa da
        # açıklamalar aynı hizadan başlıyor.
        self._title = ElidedText(lines=2)
        self._title.setProperty("role", "subtitle")
        self._title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header.addWidget(self._title, 1)

        if track.locked:
            kilit = QLabel()
            kilit.setPixmap(pixmap("lock", PALETTES[mode]["text_muted"], 18))
            kilit.setFixedWidth(20)
            header.addWidget(kilit, 0, Qt.AlignmentFlag.AlignTop)

        layout.addLayout(header)

        self._description = ElidedText(lines=2)
        self._description.setProperty("role", "muted")
        layout.addWidget(self._description)
        layout.addStretch(1)

        # İlerleme çubuğu yalnızca açık patikada: kilitlide gösterilecek
        # bir ilerleme yok, boş çubuk kafa karıştırıyor.
        self._bar = QProgressBar()
        self._bar.setTextVisible(False)
        self._bar.setVisible(not track.locked)
        layout.addWidget(self._bar)

        # Alt satır: kilitlide durum, açıkta ilerleme.
        self._caption = ElidedText(lines=2)
        self._caption.setProperty("role", "muted")
        layout.addWidget(self._caption)

        if track.locked:
            solukluk = QGraphicsOpacityEffect(self)
            solukluk.setOpacity(LOCKED_OPACITY)
            self.setGraphicsEffect(solukluk)

    def showEvent(self, event) -> None:  # noqa: N802 (Qt adlandırması)
        # Ölçü ekrana gelince alınıyor: kurulurken bazı kartlarda yazı tipi
        # henüz stil dosyasından gelmemişti ve kartlar 186 ile 201 piksel
        # arasında iki farklı boyda çıkıyordu (ölçüldü).
        super().showEvent(event)
        self._fix_height()

    def changeEvent(self, event) -> None:  # noqa: N802
        super().changeEvent(event)
        if event.type() == event.Type.StyleChange and self.isVisible():
            self._fix_height()

    def _fix_height(self) -> None:
        """Kart yüksekliği: en kalabalık hâlin sığacağı sabit boy.

        Başlık 2, açıklama 2, alt satır 2 satır; aradaki boşluklar ve çubuk.
        Her kart aynı hesabı yaptığı için hepsi aynı boyda.
        """
        for label in (self._title, self._description, self._caption):
            label.ensurePolished()
            label._reflow()
        margins = self.layout().contentsMargins()
        spacing = self.layout().spacing()
        bar = self._bar.sizeHint().height()
        height = (
            margins.top() + margins.bottom()
            + self._title.height()
            + self._description.height()
            + bar
            + self._caption.height()
            + spacing * 4
        )
        self.setFixedHeight(height)

    @property
    def track_id(self) -> str:
        return self._track.id

    def update_progress(self, completed: int, total: int) -> None:
        """Patikanın altındaki modüllerin toplam ilerlemesi."""
        self._completed = completed
        self._total = total
        percent = round(completed * 100 / total) if total else 0
        self._bar.setRange(0, 100)
        self._bar.setValue(percent)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if self._track.locked:
            return
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def set_mode(self, mode: str) -> None:
        if not self._track.locked:
            refresh_shadow(self, mode)

    def retranslate(self) -> None:
        self._title.set_full_text(self._language.pick(self._track.title))
        self._description.set_full_text(self._language.pick(self._track.description))

        if self._track.locked:
            # Kilitli patikada ön koşul ipucu daha yararlı: "içerik yok"
            # bilgisini kilit simgesi zaten veriyor.
            self._caption.set_full_text(
                self._language.t("track.prerequisite")
                if self._track.prerequisite
                else self._language.t("track.locked")
            )
        else:
            percent = (
                round(self._completed * 100 / self._total) if self._total else 0
            )
            self._caption.set_full_text(
                self._language.t(
                    "module.progress",
                    done=self._completed,
                    total=self._total,
                    percent=percent,
                )
            )


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
        self._hero.setFixedWidth(CONTENT_WIDTH)
        self._page_layout.addWidget(self._hero, alignment=Qt.AlignmentFlag.AlignHCenter)

        self._label = section_label("")
        self._page_layout.addWidget(self._label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self._grid = QGridLayout()
        self._grid.setSpacing(SPACING["md"])
        self._page_layout.addLayout(self._grid)
        self._page_layout.addStretch(1)

        outer.addWidget(scroll_page(centered_column(column, max_width=1600)))
        self._build_cards()

    def _build_cards(self) -> None:
        for index, track in enumerate(self._catalog.tracks):
            card = TrackCard(track, self._language, self._mode)
            card.clicked.connect(lambda t=track.id: self.track_opened.emit(t))
            self._grid.addWidget(card, index // 4, index % 4)
            self._cards.append(card)
        # Sütunlar eşit paylaşılıyor; yoksa her sütun içindeki en geniş
        # kartın isteğine göre büyüyordu (233 ile 247 piksel arası).
        for column in range(4):
            self._grid.setColumnStretch(column, 1)

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
        )
        self.retranslate()

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
            self._grid.addWidget(card, index // 4, index % 4)
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
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._chapter_id = chapter_id
        self._section_id = section_id

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING["md"])

        # Başlanmamış bölümde simge yerine sıra numarası duruyor: kilit
        # kaldırıldığı için asma kilit yanıltıcı, boş yuvarlak ise bomboş.
        symbol = NODE_STATES.get(state, NODE_STATES["not_started"])["symbol"]
        self.button = QPushButton(symbol or str(order))
        self.button.setProperty("variant", "node")
        self.button.setProperty("state", state)

        if state == "locked" and lock_color:
            # Kilitli bölümde sıra numarası yerine kilit duruyor. Numara
            # bırakıldığında halka "henüz başlanmamış" bölümden ayırt
            # edilemiyordu; kilidin neden kapalı olduğunu okumadan önce
            # kapalı olduğunun görünmesi gerekiyor.
            self.button.setText("")

            # Düğme birazdan devre dışı bırakılıyor; Qt devre dışı bir
            # düğmenin simgesini kendiliğinden grileştiriyor ve kilit
            # #FBBF24 yerine #A5A7AC çiziliyordu (ölçüldü). Aynı görseli
            # "devre dışı" hâl için de vererek bunu kapatıyoruz.
            kilit = icon("lock", lock_color, LOCK_ICON_SIZE)
            kilit.addPixmap(
                kilit.pixmap(LOCK_ICON_SIZE, LOCK_ICON_SIZE),
                QIcon.Mode.Disabled,
                QIcon.State.Off,
            )
            self.button.setIcon(kilit)
            self.button.setIconSize(QSize(LOCK_ICON_SIZE, LOCK_ICON_SIZE))

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

        labels = QVBoxLayout()
        labels.setSpacing(0)
        labels.addSpacing(SPACING["md"])

        self._title = QLabel(title)
        self._title.setProperty("role", "heading")
        self._title.setProperty("muted", "true" if state == "planned" else "false")
        self._title.setWordWrap(True)
        labels.addWidget(self._title)

        self._caption = QLabel(caption)
        self._caption.setProperty("role", "muted")
        self._caption.setWordWrap(True)
        labels.addWidget(self._caption)
        labels.addStretch(1)

        layout.addLayout(labels, 1)

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

    def __init__(self, start: QWidget, color: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._start = start
        self._end: QWidget | None = None
        self._color = color
        self.setFixedSize(BAND_WIDTH, CONNECTOR_HEIGHT)

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

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self._page = QWidget()
        self._layout = QVBoxLayout(self._page)
        self._layout.setContentsMargins(
            SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xxl"]
        )
        self._layout.setSpacing(0)

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
                )
                self._attach(node)
                self._layout.addWidget(self._zigzag_row(node, index))
                if not son and not grup_bitiyor:
                    self._layout.addWidget(self._connector(node, False))
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
            )
            node.opened.connect(self.section_opened)

            self._attach(node)
            self._layout.addWidget(self._zigzag_row(node, index))

            # Bir sonraki bölüm yeni bir grubu açıyorsa bağlayıcı çizgi
            # çizilmiyor: çizgi başlığın içinden geçmiş gibi duruyordu.
            if not son and not grup_bitiyor:
                self._layout.addWidget(self._connector(node, state == "completed"))

        self._layout.addStretch(1)

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
        container.setLayout(row)
        return container

    def _connector(self, node: PathNode, done: bool) -> QWidget:
        # Eğri, bu halkanın dairesinin ortasından bir sonrakininkine gidiyor;
        # sonraki halka kurulunca `_rebuild` ucunu ona bağlıyor.
        palette = PALETTES.get(self._mode, PALETTES["light"])
        curve = PathConnector(
            node.button, palette["success"] if done else palette["border"]
        )
        self._pending_curve = curve

        holder = QWidget()
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


class JourneyView(QStackedWidget):
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
        self.modules.module_opened.connect(self.open_module)
        self.path.section_opened.connect(self.section_opened)

        self._track_id = ""
        self._skipped_modules = False

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
        self.setCurrentWidget(self.modules)
        self.view_changed.emit()

    def open_module(self, chapter_id: str) -> None:
        self.path.show_chapter(chapter_id)
        self.setCurrentWidget(self.path)
        self.view_changed.emit()

    def show_modules(self) -> None:
        """Patika ekranına döner: şeritteki "Öğrenme Yolu" buraya gidiyor."""
        self.tracks.refresh()
        self.setCurrentWidget(self.tracks)
        self.view_changed.emit()

    def back(self) -> None:
        """Bir seviye yukarı çıkar.

        Modül listesi atlanmışsa geri de atlıyor; yoksa kullanıcı gelirken
        görmediği bir ekrana düşüyor.
        """
        if self.currentWidget() is self.path and not self._skipped_modules:
            self.modules.refresh()
            self.setCurrentWidget(self.modules)
        else:
            self.tracks.refresh()
            self.setCurrentWidget(self.tracks)
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
        self.tracks.set_mode(mode)
        self.modules.set_mode(mode)
        self.path.set_mode(mode)

    def retranslate(self) -> None:
        self.tracks.retranslate()
        self.modules.retranslate()
        self.path.retranslate()
