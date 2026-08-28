"""Öğrenme yolu: modül kartları ve bölüm düğümleri.

İki katmanlı bir yapı var. Ana ekranda modüller kart hâlinde duruyor; bir
modüle girince o modülün bölümleri zigzag bir yol üzerinde sıralanıyor.

Neden iki katman: müfredat tamamlandığında 23 modül ve ~180 bölüm olacak.
Hepsini tek bir yola dizmek dakikalarca kaydırma demek. Modül kartları hem
düzeni koruyor hem de "nerede ne kadar ilerledim" sorusunu tek bakışta
cevaplıyor.

Bölümler kilitli değil: sıra önerilir ama istenen bölüme her zaman girilir,
tamamlanmış bölümlere tekrar dönülebilir.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
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
from ..resources.icons import icon, pixmap
from ..resources.theme.tokens import CONTENT_WIDTH, NODE_STATES, PALETTES, SPACING
from ..widgets.common import Card, StatBlock, section_label
from ..widgets.effects import apply_shadow, refresh_shadow, repolish

# Düğümlerin soldan uzaklıkları — yol bu değerlerle zigzag çiziyor.
ZIGZAG = [30, 120, 170, 120, 30]

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


def centered_column(inner: QWidget) -> QWidget:
    """İçeriği sabit genişlikte bir sütuna alıp ekranın ortasına yerleştirir.

    Makette yol ve modül kartları uçlara yayılmıyor, ortada toplanıyor.
    Geniş ekranda içeriğin sağa sola dağılması hem dağınık duruyor hem de
    göz her satırda uzun bir yol kat ediyor.
    """
    holder = QWidget()
    row = QHBoxLayout(holder)
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(0)

    inner.setMaximumWidth(CONTENT_WIDTH)
    inner.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    row.addStretch(1)
    row.addWidget(inner, 10)
    row.addStretch(1)
    return holder


class HeroCard(QFrame):
    """Üstteki karşılama kartı: kaldığın yer ve özet sayılar."""

    resume = Signal()

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self.setProperty("role", "hero")
        apply_shadow(self, "light", strong=True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["xl"], SPACING["lg"], SPACING["xl"], SPACING["lg"])
        layout.setSpacing(SPACING["xs"])

        self._title = QLabel()
        self._title.setStyleSheet("color:#FFFFFF; font-size:23px; font-weight:700;")
        layout.addWidget(self._title)

        self._subtitle = QLabel()
        self._subtitle.setStyleSheet(
            "color:rgba(255,255,255,0.92); font-size:14px; font-weight:600;"
        )
        self._subtitle.setWordWrap(True)
        layout.addWidget(self._subtitle)
        layout.addSpacing(SPACING["md"])

        stats = QHBoxLayout()
        stats.setSpacing(SPACING["xl"])
        self._stats = {
            key: StatBlock("0", "", inverse=True)
            for key in ("sections", "exercises", "streak", "progress")
        }
        for block in self._stats.values():
            stats.addWidget(block)
        stats.addStretch(1)
        layout.addLayout(stats)

    def update_stats(
        self,
        name: str,
        resume_text: str,
        sections: int,
        exercises: int,
        streak: int,
        progress: int,
    ) -> None:
        self._title.setText(
            self._language.t("home.welcome_named", name=name)
            if name
            else self._language.t("home.welcome")
        )
        self._subtitle.setText(resume_text)

        self._stats["sections"].set_value(str(sections))
        self._stats["exercises"].set_value(str(exercises))
        self._stats["streak"].set_value(str(streak))
        self._stats["progress"].set_value(f"%{progress}")
        self.retranslate()

    def set_mode(self, mode: str) -> None:
        refresh_shadow(self, mode, strong=True)

    def retranslate(self) -> None:
        for key in self._stats:
            self._stats[key].set_label(self._language.t(f"home.stat_{key}"))


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
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(164)

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
        header.addWidget(self._icon, 0, Qt.AlignmentFlag.AlignTop)

        self._title = QLabel()
        self._title.setProperty("role", "subtitle")
        self._title.setWordWrap(True)
        header.addWidget(self._title, 1)

        if track.locked:
            kilit = QLabel()
            kilit.setPixmap(pixmap("lock", PALETTES[mode]["text_muted"], 18))
            kilit.setFixedWidth(20)
            header.addWidget(kilit, 0, Qt.AlignmentFlag.AlignTop)
        header.addLayout(QVBoxLayout())

        layout.addLayout(header)

        self._description = QLabel()
        self._description.setProperty("role", "muted")
        self._description.setWordWrap(True)
        layout.addWidget(self._description)
        layout.addStretch(1)

        # İlerleme çubuğu yalnızca açık patikada: kilitlide gösterilecek
        # bir ilerleme yok, boş çubuk kafa karıştırıyor.
        self._bar = QProgressBar()
        self._bar.setTextVisible(False)
        self._bar.setVisible(not track.locked)
        layout.addWidget(self._bar)

        # Alt satır: kilitlide durum, açıkta ilerleme.
        self._caption = QLabel()
        self._caption.setProperty("role", "muted")
        self._caption.setWordWrap(True)
        layout.addWidget(self._caption)

        if track.locked:
            solukluk = QGraphicsOpacityEffect(self)
            solukluk.setOpacity(LOCKED_OPACITY)
            self.setGraphicsEffect(solukluk)

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
        self._title.setText(self._language.pick(self._track.title))
        self._description.setText(self._language.pick(self._track.description))

        if self._track.locked:
            # Kilitli patikada ön koşul ipucu daha yararlı: "içerik yok"
            # bilgisini kilit simgesi zaten veriyor.
            self._caption.setText(
                self._language.t("track.prerequisite")
                if self._track.prerequisite
                else self._language.t("track.locked")
            )
        else:
            percent = (
                round(self._completed * 100 / self._total) if self._total else 0
            )
            self._caption.setText(
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
        self._page_layout.addWidget(self._hero)

        self._label = section_label("")
        self._page_layout.addWidget(self._label)

        self._grid = QGridLayout()
        self._grid.setSpacing(SPACING["md"])
        self._page_layout.addLayout(self._grid)
        self._page_layout.addStretch(1)

        outer.addWidget(scroll_page(centered_column(column)))
        self._build_cards()

    def _build_cards(self) -> None:
        for index, track in enumerate(self._catalog.tracks):
            card = TrackCard(track, self._language, self._mode)
            card.clicked.connect(lambda t=track.id: self.track_opened.emit(t))
            self._grid.addWidget(card, index // 2, index % 2)
            self._cards.append(card)

    def _chapter_progress(self, chapter) -> tuple[int, int]:
        """Bir modülde kaç bölüm tamamlandı, kaç bölüm var."""
        biten = 0
        for section in chapter.sections:
            state = self._store.section_state(
                chapter.id, section.id, len(section.exercises)
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
            exercises=self._store.solved_exercise_count(),
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
        page = centered_column(column)

        self._hero = HeroCard(language)
        self._page_layout.addWidget(self._hero)

        self._modules_label = section_label("")
        self._page_layout.addWidget(self._modules_label)

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
            self._grid.addWidget(card, index // 2, index % 2)
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
                    chapter.id, section.id, len(section.exercises)
                )
                if state.status(section.requires_quiz, section.requires_exercises) == "completed":
                    done += 1

            card.update_progress(done, len(chapter.sections))
            card.retranslate()
            total_sections += len(chapter.sections)
            completed_sections += done

        self._hero.update_stats(
            name=self._store.profile().get("first_name", ""),
            resume_text=self._resume_text(),
            sections=completed_sections,
            exercises=self._store.solved_exercise_count(),
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

        if state == "planned":
            # Henüz içeriği yok: tıklanmıyor, imleç değişmiyor. Boş bir
            # bölüm açmak, "bozuk" izlenimi veriyor.
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
            solukluk = QGraphicsOpacityEffect(self)
            solukluk.setOpacity(PLANNED_OPACITY)
            self.setGraphicsEffect(solukluk)


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

        header = QLabel(self._language.pick(chapter.title))
        header.setProperty("role", "title")
        self._layout.addWidget(header)

        description = QLabel(self._language.pick(chapter.description))
        description.setProperty("role", "muted")
        description.setWordWrap(True)
        self._layout.addWidget(description)
        self._layout.addSpacing(SPACING["xl"])

        # "Şu an buradasın" işareti: tamamlanmamış ilk bölüm.
        current_index = self._current_index(chapter)

        for index, section in enumerate(chapter.sections):
            state = self._state_of(chapter.id, section)
            if index == current_index and state != "completed":
                state = "current"

            node = PathNode(
                chapter.id,
                section.id,
                self._language.pick(section.title),
                self._caption_for(section, state),
                state,
                order=index + 1,
            )
            node.opened.connect(self.section_opened)

            row = QHBoxLayout()
            row.setContentsMargins(ZIGZAG[index % len(ZIGZAG)], 0, 0, 0)
            row.addWidget(node)
            row.addStretch(1)
            container = QWidget()
            container.setLayout(row)
            self._layout.addWidget(container)

            son_gercek = index == len(chapter.sections) - 1
            if not son_gercek or chapter.planned:
                self._layout.addWidget(self._connector(index, state == "completed"))

        # Henüz yazılmamış bölümler: soluk, tıklanmayan halkalar. Modülün
        # nereye gittiğini baştan göstermek, "burası bu kadarmış" izlenimini
        # önlüyor.
        taban = len(chapter.sections)
        for offset, planlanan in enumerate(chapter.planned):
            index = taban + offset

            node = PathNode(
                chapter.id,
                planlanan.get("id", ""),
                self._language.pick(planlanan.get("title")),
                self._language.t("path.planned"),
                "planned",
                order=index + 1,
            )

            row = QHBoxLayout()
            row.setContentsMargins(ZIGZAG[index % len(ZIGZAG)], 0, 0, 0)
            row.addWidget(node)
            row.addStretch(1)
            container = QWidget()
            container.setLayout(row)
            self._layout.addWidget(container)

            if offset < len(chapter.planned) - 1:
                self._layout.addWidget(self._connector(index, False))

        self._layout.addStretch(1)

    def _connector(self, index: int, done: bool) -> QWidget:
        holder = QWidget()
        layout = QHBoxLayout(holder)
        layout.setContentsMargins(ZIGZAG[index % len(ZIGZAG)] + 35, 0, 0, 0)

        line = QFrame()
        line.setProperty("role", "connector")
        line.setProperty("done", "true" if done else "false")
        line.setFixedHeight(30)
        layout.addWidget(line)
        layout.addStretch(1)
        return holder

    def _state_of(self, chapter_id: str, section) -> str:
        state = self._store.section_state(chapter_id, section.id, len(section.exercises))
        return state.status(section.requires_quiz, section.requires_exercises)

    def _current_index(self, chapter: Chapter) -> int:
        for index, section in enumerate(chapter.sections):
            if self._state_of(chapter.id, section) != "completed":
                return index
        return -1

    def _caption_for(self, section, state: str) -> str:
        progress = self._store.section_state(
            self._chapter_id, section.id, len(section.exercises)
        )
        minutes = section.estimated_minutes

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

        if len(chapters) == 1:
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
    def showing_tracks(self) -> bool:
        return self.currentWidget() is self.tracks

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
