"""Bir bölümün ekranı: konu anlatımı, ders notları, sınav ve alıştırmalar.

Sekme çubuğu yerine segmented control kullanılıyor. Yalnızca o bölümde
gerçekten var olan parçalar gösteriliyor: ders notu olmayan bir bölümde
"Ders Notları" seçeneği hiç çıkmıyor.

Bölümde birden fazla alıştırma varsa aralarında geçiş düğmeleri beliriyor.

Sağda açılıp kapanan bir not paneli var (`note_panel.py`): başlıktaki
"Not al" düğmesi ya da `Ctrl+N`. Panel hangi sekmede olunursa olsun açık
kalıyor ve bölümden bölüme geçerken de açık kalıyor. Ders, ders notu ve
alıştırma yönergesinde seçilen metin sağ tıkla nota eklenebiliyor.
"""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt, QTimer, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..widgets import motion
from .note_panel import PANEL_WIDTH as NOTE_PANEL_WIDTH
from ..core.catalog import Catalog, Section
from ..core.language import LanguageManager
from ..core.quiz_timing import untimed_quiz
from ..core.progress import ProgressStore
from ..core.unlock import is_unlocked
from ..resources.icons import icon
from ..resources.theme.tokens import PALETTES, RAIL_COLORS, SPACING, mix
from ..widgets.effects import apply_shadow, refresh_shadow
from ..widgets.fade_stack import FadeStack
from ..widgets.stepper import Stepper
from ..widgets.common import SegmentedControl
from ..widgets.document_view import DocumentView
from .exercise_view import ExerciseView
from .header import ScreenHeader
from .lesson_view import LessonView
from .note_panel import NotePanel
from .notes_view import NotesView
from .pdf_view import PdfView
from .quiz_view import QuizView


class TopicView(QWidget):
    """Tek bir alt bölümün tüm içeriği."""

    back_requested = Signal()
    progress_changed = Signal()
    # Paneldeki "Notlarım'da aç": notun id'si.
    open_notebook = Signal(int)
    # Panelde ilk kez yazılı bir not kaydedildi (rozet koşulu).
    notes_changed = Signal()

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
        self._section: Section | None = None
        self._panes: list[str] = []
        self._exercises: list = []
        self._exercise_index = 0
        # Ders metninin hangi dilde okunduğu; dil değişince yeniden okumak
        # için gerekiyor.
        self._lesson_language = ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.header = ScreenHeader(language)
        self.header.back_clicked.connect(self.back_requested)

        # Sekmeler başlığın altında, ortalanmış bir şeritte (ui-taslak.md F1).
        # Sağdaydılar ve uzun bölüm adlarında başlıkla çakışıyorlardı.
        self._segments = SegmentedControl()
        self._segments.changed.connect(self._show_pane)
        self._subbar = QFrame()
        self._subbar.setProperty("role", "subbar")
        alt = QHBoxLayout(self._subbar)
        alt.setContentsMargins(SPACING["lg"], SPACING["sm"] + 2, SPACING["lg"], SPACING["sm"] + 2)
        alt.addStretch(1)
        alt.addWidget(self._segments)
        alt.addStretch(1)

        self._note_button = QPushButton()
        self._note_button.setProperty("variant", "ghost")
        self._note_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._note_button.setIconSize(QSize(18, 18))
        self._note_button.clicked.connect(lambda: self.toggle_note())
        self.header.add_widget(self._note_button)

        layout.addWidget(self.header)
        layout.addWidget(self._subbar)

        # Sekmeler arası kısa çapraz sönme (ui-taslak.md C4).
        self._stack = FadeStack(subtle=True)
        self._lesson = LessonView(language, track_reading=True)
        self._notes = NotesView(language)
        self._pdf = PdfView(language)
        self._quiz = QuizView(language)
        self._exercise = ExerciseView(language, store)

        for widget in (self._lesson, self._notes, self._pdf, self._quiz, self._exercise):
            self._stack.addWidget(widget)

        self._lesson.action.connect(self._on_lesson_action)
        self._quiz.completed.connect(self._on_quiz_completed)
        self._exercise.solved.connect(self._on_exercise_solved)
        self._notes.advance.connect(self._on_notes_advance)
        self._quiz.advance.connect(self._on_quiz_advance)
        self._exercise.advance.connect(self._on_exercise_advance)

        # İçerik solda, not paneli sağda.
        body = QWidget()
        row = QHBoxLayout(body)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)

        column = QWidget()
        column_layout = QVBoxLayout(column)
        column_layout.setContentsMargins(0, 0, 0, 0)
        column_layout.setSpacing(0)
        # Geçiş şeridi içeriğin üstünde: altta, sonuç panelinin de altında
        # dururken görülmüyordu ve ikinci alıştırmanın varlığı fark
        # edilmiyordu.
        column_layout.addWidget(self._build_exercise_switcher())
        column_layout.addWidget(self._stack, 1)
        row.addWidget(column, 1)

        # Not paneli içeriği itmiyor: sağda, içeriğin üstünde yüzen bir
        # çekmece (prototip `.drawer`). Konumu gövdenin boyutundan.
        self._body = body
        self._note_panel = NotePanel(language, store, body)
        self._note_panel.hide()
        self._note_panel.close_requested.connect(lambda: self.toggle_note(False))
        self._note_panel.open_in_notebook.connect(self.open_notebook)
        self._note_panel.changed.connect(self.notes_changed)
        self._note_slide = 0.0
        apply_shadow(self._note_panel, "dark", strong=True, blur=44, offset_y=18, radius=20)
        body.installEventFilter(self)
        layout.addWidget(body, 1)

        # Seçimi nota ekleme: bölümdeki bütün belge alanları (ders, ders
        # notu, alıştırma yönergesi).
        self._documents = self.findChildren(DocumentView)
        for document in self._documents:
            document.quote_requested.connect(self._on_quote)

        kisayol = QShortcut(QKeySequence("Ctrl+N"), self, lambda: self.toggle_note())
        kisayol.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        self._mode = "light"

    def _build_exercise_switcher(self) -> QWidget:
        """Birden fazla alıştırma varsa aralarında geçiş şeridi.

        Sayı düz bir yazı olarak duruyordu ve kimse fark etmiyordu. Artık
        numaralar birer düğme: hem "burada üç alıştırma var" bilgisini
        bakar bakmaz veriyor, hem de istediğine doğrudan atlatıyor.
        """
        self._switcher = QFrame()
        self._switcher.setProperty("role", "topbar")
        self._switcher.hide()

        layout = QHBoxLayout(self._switcher)
        layout.setContentsMargins(
            SPACING["lg"], SPACING["sm"], SPACING["lg"], SPACING["sm"]
        )
        layout.setSpacing(SPACING["sm"])

        self._switcher_label = QLabel()
        self._switcher_label.setProperty("role", "heading")
        layout.addWidget(self._switcher_label)

        layout.addStretch(1)

        # İlerleme şeridi sağda: çözülenler patika renginde dolu ve onaylı,
        # açık olan halkalı, aralarında çizgi (ui-taslak.md C6).
        self._stepper = Stepper()
        self._stepper.clicked.connect(self._go_exercise)
        layout.addWidget(self._stepper, 0, Qt.AlignmentFlag.AlignVCenter)

        return self._switcher

    # --- içerik -----------------------------------------------------------

    def show_section(self, chapter_id: str, section_id: str) -> None:
        """Bölümü yükler; açılacak sekmenin belgesi `when_ready`'de çiziliyor."""
        self._show_section(chapter_id, section_id)

    def _show_section(self, chapter_id: str, section_id: str) -> None:
        section = self._catalog.section(chapter_id, section_id)
        if section is None:
            return

        self._section = section
        self._exercises = section.exercises
        self._exercise_index = 0
        # Sekme çizgisi patika renginde; yeni bölümde adım şeridi baştan
        # (önceki bölümün çözümleri "yeni çözüldü" diye oynamasın).
        chapter = self._catalog.chapter(chapter_id)
        self._segments.set_accent(chapter.color if chapter else None)
        self._stepper.reset()
        self._panes = []

        language_code = self._language.language
        state = self._store.section_state(chapter_id, section_id, self._exercises)
        completed = state.status(section.requires_quiz, section.requires_exercises) == "completed"

        for block in section.blocks:
            if block.type == "lesson":
                self._load_lesson(block, completed)
                self._panes.append("lesson")

            elif block.type == "notes":
                if block.documents:
                    self._notes.show_notes(block)
                    self._panes.append("notes")

            elif block.type == "pdf":
                # Henüz metne çevrilmemiş modüllerde not PDF olarak duruyor.
                # Çeviri kademeli ilerlediği için iki biçim bir arada yaşıyor.
                resolved = block.file_for(language_code)
                if resolved and resolved.exists:
                    self._pdf.show_pdf(resolved.path, self._language.pick(block.title))
                    self._panes.append("pdf")

            elif block.type == "quiz":
                resolved = block.file_for(language_code)
                if resolved and resolved.exists:
                    # Önceki deneme başlangıç ekranında gösteriliyor:
                    # "geçen sefer 60 almıştın" bilgisi, sınava girmeden
                    # önce insanın neye hazırlandığını bilmesini sağlıyor.
                    self._quiz.show_quiz(
                        resolved.path,
                        block.pass_score,
                        time_limit_sec=block.time_limit_sec,
                        previous_score=state.quiz_score,
                        previous_passed=state.quiz_passed,
                        untimed=untimed_quiz(self._store),
                    )
                    self._panes.append("quiz")

        if self._exercises:
            self._panes.append("exercise")
            self._load_exercise()

        self._note_panel.set_section(chapter_id, section_id, self._language.pick(section.title))

        self._lesson.set_meta(self._meta_items(section))
        self._lesson.set_footer(self._footer_items())
        # Bölümü açmak okumak değil: "okundu" işareti, kullanıcı metnin
        # sonuna indiğinde `lesson-read` bildirimiyle konuyor.
        self.retranslate()
        # Sekme adları kurulduktan sonra: onaylar yeni sekmelere yazılsın.
        self._update_progress_box(state)
        self._segments.set_current(0, notify=False)
        self._show_pane(0)

    def _load_lesson(self, block, completed: bool) -> None:
        """Ders metnini seçili dilde yükler."""
        resolved = block.file_for(self._language.language)
        self._lesson_language = self._language.language
        self._lesson.show_lesson(
            resolved.path if resolved else None,
            resolved.is_fallback if resolved else False,
            completed=completed,
        )

    def _reload_lesson_language(self) -> None:
        """Dil değiştiyse ders metnini yeniden okur.

        Ders anlatımı **dosyadan** geliyor (`lesson.tr.md` / `lesson.en.md`)
        ve bir kez okunup bellekte tutuluyor. `retranslate` yalnızca o
        metni yeniden çiziyordu; dil değişince etiketler çevriliyor ama
        ders eski dilde kalıyordu ve kullanıcının bölümden çıkıp girmesi
        gerekiyordu.

        Aynı sınıf hata daha önce alıştırmanın başlangıç kodunda da
        çıkmıştı: **dosyadan gelen dile bağlı içerik `retranslate` ile
        tazelenmeli.**
        """
        if self._section is None or self._lesson_language == self._language.language:
            return

        state = self._store.section_state(
            self._section.chapter_id, self._section.id, self._exercises
        )
        completed = state.status(
            self._section.requires_quiz, self._section.requires_exercises
        ) == "completed"

        for block in self._section.blocks:
            if block.type == "lesson":
                self._load_lesson(block, completed)
                break

    def refresh_quiz_timing(self) -> None:
        """Sınav süresi ayarı değişti; açık sınav o an güncelleniyor.

        Kilit ayarında olduğu gibi burada da ayar yalnızca ekran
        **açılırken** okunuyordu; sınav açıkken değiştirmek hiçbir şey
        yapmıyor, çıkıp girmek gerekiyordu.
        """
        self._quiz.set_untimed(untimed_quiz(self._store))

    def warm_up(self) -> None:
        """Bölümün panolarını bir kez çizdirir.

        Ders, notlar ve alıştırma yönergesi ayrı birer belge alanı
        (Chromium). Her biri **ilk kez gösterildiğinde** yüzeyi oluşana
        kadar siyah kalıyor; bu tur o ilk çizimi kullanıcı görmeden yapıyor.
        """
        from PySide6.QtWidgets import QApplication

        onceki = self._stack.currentIndex()
        for index in range(self._stack.count()):
            self._stack.setCurrentIndex(index)
            QApplication.processEvents()
        self._stack.setCurrentIndex(onceki)
        QApplication.processEvents()

    def _meta_items(self, section) -> list[str]:
        """Ders başlığının altındaki bilgi satırının parçaları.

        Başına simge konuyor; makette de öyle ve satır bir metin yığını
        olmaktan çıkıp okunabilir hâle geliyor.
        """
        items = [f"📖  {section.estimated_minutes} {self._language.t('common.minutes')}"]

        if self._exercises:
            items.append(
                f"✏️  {len(self._exercises)} {self._exercise_word().lower()}"
            )
        if "quiz" in self._panes:
            items.append(
                f"📝  {self._quiz_length()} {self._language.t('quiz.questions_short')}"
            )

        return items

    def _quiz_length(self) -> int:
        """Sınavdaki soru sayısı."""
        import json

        for block in (self._section.blocks if self._section else []):
            if block.type != "quiz":
                continue
            resolved = block.file_for(self._language.language)
            if resolved and resolved.exists:
                with resolved.path.open(encoding="utf-8") as handle:
                    return len(json.load(handle).get("questions", []))
        return 0

    def _all_problems(self) -> bool:
        """Bölümün alıştırmalarının hepsi matematik problemi mi?"""
        return bool(self._exercises) and all(e.is_problem for e in self._exercises)

    def _exercise_word(self) -> str:
        """Sekmenin adı: kod alıştırmasında "Alıştırma", matematikte "Problem"."""
        return self._language.t("tabs.problem" if self._all_problems() else "tabs.exercise")

    def _pane_labels(self) -> dict[str, str]:
        """Bölüm sekmelerinin seçili dildeki adları."""
        return {
            "lesson": self._language.t("tabs.lesson"),
            "notes": self._language.t("tabs.pdf"),
            "pdf": self._language.t("tabs.pdf_file"),
            "quiz": self._language.t("tabs.quiz"),
            "exercise": self._exercise_word(),
        }

    def _pane_after(self, name: str) -> str | None:
        """Verilen sekmeden sonra gelen sekme; sonuncuysa `None`."""
        if name not in self._panes:
            return None
        index = self._panes.index(name) + 1
        return self._panes[index] if index < len(self._panes) else None

    def _footer_items(self) -> list[tuple[str, str, bool]]:
        """Ders metninin altındaki gezinme düğmeleri.

        İleri düğmesi bölümün **bir sonraki sekmesine** yollar. Sırayı
        `section.json` belirlediği için, ders notu olan bir bölümde önce ders
        notuna gidiliyor; sınava atlamıyor. Bölümde ders metninden sonra
        hiçbir şey yoksa sonraki bölüme geçiliyor.
        """
        if self._section is None:
            return []

        previous, following = self._catalog.neighbours(
            self._section.chapter_id, self._section.id
        )
        buttons: list[tuple[str, str, bool]] = [
            (
                "previous-section" if previous else "",
                f"←  {self._language.t('nav.previous')}",
                False,
            )
        ]

        sonraki = self._pane_after("lesson")
        if sonraki:
            label = self._pane_labels()[sonraki]
            buttons.append((f"go-{sonraki}", f"{label}  →", True))
        elif following and self._unlocked(following):
            # Sonraki bölüm kilitliyse düğme hiç çizilmiyor. Soluk ama
            # tıklanamaz bir düğme bırakmak kullanıcıyı boşuna uğraştırıyor;
            # bu bölüm bitince düğme kendiliğinden beliriyor.
            buttons.append(("next-section", f"{self._language.t('nav.next')}  →", True))

        return buttons

    def refresh_navigation(self) -> None:
        """Alt gezinme düğmelerini yeniden kurar.

        Kilit ayarı değiştiğinde çağrılıyor: "sonraki bölüm" düğmesi
        kilitliyken hiç çizilmiyor, ayar açılınca o an belirmesi gerekiyor.
        """
        if self._section is None:
            return
        self._lesson.set_footer(self._footer_items())
        self._refresh_advance_labels()

    def _unlocked(self, section) -> bool:
        """Bu bölüme girilebilir mi? Kural `app/core/unlock.py` içinde."""
        return is_unlocked(self._catalog, self._store, section.chapter_id, section.id)

    def _mark_lesson_read(self) -> None:
        """Ders metnini okunmuş işaretler.

        İki yerden çağrılıyor: metnin sonuna inildiğinde gelen `lesson-read`
        bildiriminden ve metnin en altındaki ileri düğmesinden. İkisi de
        kullanıcının sayfanın sonuna ulaştığı anlamına geliyor; bölümü açmak
        tek başına yetmiyor.
        """
        if self._section is None:
            return
        self._store.mark_lesson_read(self._section.chapter_id, self._section.id)
        self._refresh_progress()
        self.progress_changed.emit()

    def _on_lesson_action(self, action: str) -> None:
        if action == "lesson-read":
            self._mark_lesson_read()
        elif action.startswith("go-"):
            hedef = action[3:]
            if hedef in self._panes:
                # Bu düğme ders metninin en altında duruyor; oraya ulaşıp
                # basmak konuyu okumuş olmak demek.
                self._mark_lesson_read()
                self._segments.set_current(self._panes.index(hedef))
        elif action in ("next-section", "previous-section") and self._section is not None:
            if action == "next-section":
                self._mark_lesson_read()
            previous, following = self._catalog.neighbours(
                self._section.chapter_id, self._section.id
            )
            target = following if action == "next-section" else previous
            # Geri gitmek her zaman serbest; ileri gitmek kilide bakıyor.
            # Düğme zaten çizilmiyor ama kilit kuralı tek yerde durmalı:
            # klavye kısayolu ya da başka bir yol buraya düşerse de geçerli.
            if target and (action == "previous-section" or self._unlocked(target)):
                self.show_section(target.chapter_id, target.id)

    def _on_notes_advance(self) -> None:
        """Son ders notunun altındaki düğme: bölümün sonraki adımına geç."""
        hedef = self._pane_after("notes")
        if hedef and hedef in self._panes:
            self._segments.set_current(self._panes.index(hedef))

    def _next_section_if_open(self):
        """Sonraki bölüm, girilebiliyorsa; yoksa `None`."""
        if self._section is None:
            return None
        _, following = self._catalog.neighbours(
            self._section.chapter_id, self._section.id
        )
        return following if following and self._unlocked(following) else None

    def _refresh_advance_labels(self) -> None:
        """Sınav sonucunun ve alıştırmanın altındaki "devam" düğmeleri.

        Ders ve not sayfalarının altında ileri düğmesi vardı; sınavda ve
        alıştırmada yoktu. Sınavı bitiren ya da alıştırmayı çözen kişi
        bir sonraki adıma geçmek için sağ üstteki sekmeleri ve numaraları
        aramak zorunda kalıyordu.

        Sıra ders sayfasınınkiyle aynı: önce bölümün sonraki sekmesi, sonra
        sonraki alıştırma, en sonda sonraki bölüm. Sonraki bölüm kilitliyse
        düğme çizilmiyor; bölüm bitince (son alıştırma çözülünce, sınav
        geçilince) bu metot yeniden çağrılıyor ve düğme o an beliriyor.
        """
        labels = self._pane_labels()
        genel = self._language.t("nav.next") if self._next_section_if_open() else None

        sonraki = self._pane_after("quiz")
        self._quiz.set_advance_label(labels[sonraki] if sonraki else genel)

        if self._exercises:
            if self._exercise_index < len(self._exercises) - 1:
                self._exercise.set_advance_label(
                    self._language.t("problem.next" if self._all_problems() else "exercise.next")
                )
            else:
                self._exercise.set_advance_label(genel)

    def _on_quiz_advance(self) -> None:
        """Sınav sonucundaki düğme: sonraki sekme, yoksa sonraki bölüm."""
        hedef = self._pane_after("quiz")
        if hedef and hedef in self._panes:
            self._segments.set_current(self._panes.index(hedef))
            return
        self._go_next_section()

    def _on_exercise_advance(self) -> None:
        """Alıştırmanın altındaki düğme: sonraki alıştırma, yoksa bölüm."""
        if self._exercise_index < len(self._exercises) - 1:
            self._go_exercise(self._exercise_index + 1)
            return
        self._go_next_section()

    def _go_next_section(self) -> None:
        # Kilit kuralı burada da uygulanıyor: düğme kilitliyken zaten
        # çizilmiyor, ama başka bir yol buraya düşerse de geçerli olmalı.
        target = self._next_section_if_open()
        if target is not None:
            self.show_section(target.chapter_id, target.id)

    def _load_exercise(self) -> None:
        if not self._exercises or self._section is None:
            return
        self._exercise.show_exercise(
            self._exercises[self._exercise_index],
            self._section.chapter_id,
            self._section.id,
        )
        self._update_switcher()
        self._refresh_advance_labels()

    def _update_switcher(self) -> None:
        many = len(self._exercises) > 1
        self._switcher.setVisible(many and self._current_pane() == "exercise")
        if not many:
            return

        self._switcher_label.setText(
            f"{self._exercise_word()} "
            f"{self._exercise_index + 1} / {len(self._exercises)}"
        )
        self._rebuild_numbers()

    def _rebuild_numbers(self) -> None:
        """Alıştırma numaralarını yeniden çizer.

        Çözülmüş alıştırmanın numarasının yanında onay işareti duruyor;
        böylece kaç tanesini bitirdiğin de aynı yerden görünüyor.
        """
        if self._section is None:
            return
        cozuldu = [
            self._store.exercise_solved(self._section.chapter_id, self._section.id, e.id)
            for e in self._exercises
        ]
        chapter = self._catalog.chapter(self._section.chapter_id)
        if chapter is not None:
            self._stepper.set_color(chapter.color)
        self._stepper.set_steps(cozuldu, self._exercise_index,
                                [self._language.pick(e.title) for e in self._exercises])

    def _go_exercise(self, index: int) -> None:
        if 0 <= index < len(self._exercises) and index != self._exercise_index:
            self._exercise_index = index
            self._load_exercise()

    def _current_pane(self) -> str:
        if not self._panes:
            return ""
        return self._panes[min(self._segments.current, len(self._panes) - 1)]

    def _show_pane(self, index: int) -> None:
        if not self._panes:
            return
        name = self._panes[min(index, len(self._panes) - 1)]
        widget = {
            "lesson": self._lesson,
            "notes": self._notes,
            "pdf": self._pdf,
            "quiz": self._quiz,
            "exercise": self._exercise,
        }[name]
        # Sekmedeki belge hazır olunca girsin (içerik sonradan belirmesin).
        self._stack.slide_to(widget, wait=lambda basla: self.when_ready(basla, 250))
        self._update_switcher()
        # "Kodumu ekle" yalnızca alıştırmadayken anlamlı.
        self._note_panel.set_code_source(
            self._exercise.code_for_note if name == "exercise" else None
        )

    def focus(self, pane: str, index: int = 0, anchor: str = "") -> None:
        """Arama sonucunun gösterdiği yere götürür.

        `pane` sekme ("lesson", "notes", "exercise"); ders notunda `index`
        kaçıncı not, alıştırmada kaçıncı alıştırma; konu anlatımında
        `anchor` başlığın çapası.
        """
        if pane not in self._panes:
            return
        self._segments.set_current(self._panes.index(pane))
        if pane == "notes":
            self._notes.select(index)
        elif pane == "exercise":
            self._go_exercise(index)
        elif pane == "lesson" and anchor:
            self._lesson.scroll_to(anchor)

    def when_ready(self, callback, timeout: int = 600) -> None:
        """Açık sekmedeki belge hazır olunca `callback` (bkz. `when_documents_ready`)."""
        from ..widgets.document_view import when_documents_ready
        when_documents_ready(self._stack.currentWidget(), callback, timeout)

    # --- not paneli -------------------------------------------------------

    def toggle_note(self, visible: bool | None = None) -> None:
        """Not panelini açar ya da kapatır; açılınca imleç notta."""
        if visible is None:
            visible = self._note_panel.isHidden()
        self._note_button.setProperty("active", "true" if visible else "false")
        # Panel sağdan açılıp kapanıyor (ui-taslak F3): genişlik yayla büyüyor.
        # Çekmece sağdan yayla kayarak giriyor, kısa ve hızlanarak çıkıyor.
        panel = self._note_panel
        if visible:
            if panel.isHidden():
                self._note_slide = 0.0
                self._place_note_panel()
                panel.show()
                panel.raise_()
            motion.animate(panel, "slide", self._note_slide, 1.0, self._set_note_slide, "spring", "spring")
            panel.focus_editor()
        elif not panel.isHidden():
            motion.animate(panel, "slide", self._note_slide, 0.0, self._set_note_slide, "short", "in",
                           on_done=panel.hide)

    def _set_note_slide(self, value: float) -> None:
        self._note_slide = value
        self._place_note_panel()

    def _place_note_panel(self) -> None:
        """Çekmecenin yeri: sağdan 18, üstten 14, alttan 18 piksel boşluk."""
        body = self._body
        genislik = NOTE_PANEL_WIDTH
        hedef = body.width() - genislik - 18
        disari = body.width() + 30
        x = round(disari + (hedef - disari) * self._note_slide)
        self._note_panel.setGeometry(x, 14, genislik, max(0, body.height() - 32))

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        if obj is getattr(self, "_body", None) and event.type() == event.Type.Resize:
            self._place_note_panel()
        return super().eventFilter(obj, event)

    def _on_quote(self, text: str) -> None:
        """Belgede seçilip "Nota ekle" denen metin."""
        self.toggle_note(True)
        self._note_panel.add_quote(text)

    def flush_note(self) -> None:
        """Panelde yazılıp henüz kaydedilmemiş son harfler."""
        self._note_panel.flush()

    def _refresh_progress(self) -> None:
        """İlerlemeyi veritabanından tazeleyip kutuya yazar."""
        if self._section is None:
            return
        state = self._store.section_state(
            self._section.chapter_id, self._section.id, self._exercises
        )
        self._update_progress_box(state)

    def _update_progress_box(self, state) -> None:
        """Sağdaki ilerleme kutusunu gerçek duruma göre yazar.

        Her parça kendi durumunu gösteriyor: bitmişse ✓, bitmemişse ○.
        Önceden bölüm açılır açılmaz ders "okundu" sayıldığı için hiçbir şey
        yapılmadan tik görünüyordu.
        """
        if self._section is None:
            return

        steps: list[tuple[str, bool, str]] = []

        if "lesson" in self._panes:
            steps.append((self._language.t("progress.lesson"), bool(state.lesson_read), ""))

        if "quiz" in self._panes:
            score = f"{state.quiz_score}" if state.quiz_score is not None else ""
            steps.append((self._language.t("progress.quiz"), bool(state.quiz_passed), score))

        if self._exercises:
            total = len(self._exercises)
            solved = state.exercises_solved
            steps.append((self._language.t("progress.exercises"), solved >= total, f"{solved}/{total}"))

        self._lesson.set_progress(steps)
        # Sekmelerde tamamlanma onayı (ui-taslak.md F1).
        bitti = {
            "lesson": bool(state.lesson_read),
            "quiz": bool(state.quiz_passed),
            "exercise": bool(self._exercises) and state.exercises_solved >= len(self._exercises),
        }
        self._segments.set_done([bitti.get(name, False) for name in self._panes])

    # --- olaylar ----------------------------------------------------------

    def _on_quiz_completed(self, score: int, passed: bool) -> None:
        if self._section is None:
            return
        self._store.record_quiz(
            self._section.chapter_id, self._section.id, score, passed
        )
        self._refresh_progress()
        # Sınav bölümü bitirmiş olabilir: sonraki bölüm açıldıysa "devam"
        # düğmeleri o an güncelleniyor.
        self._refresh_advance_labels()
        self.progress_changed.emit()

    def _on_exercise_solved(self, _exercise_id: str) -> None:
        self._refresh_progress()
        # Numara düğmelerindeki onay işareti veritabanından okunuyor;
        # çözüldüğü anda yenilenmezse tik ancak başka bir alıştırmaya
        # geçince ya da bölüm yeniden açılınca beliriyordu.
        self._update_switcher()
        # Son alıştırma bölümü bitirmiş olabilir; sonraki bölüm açıldıysa
        # alttaki düğme o an beliriyor.
        self._refresh_advance_labels()
        self.progress_changed.emit()

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._stack.set_background(PALETTES[mode]["bg"])
        self._mode = mode
        self.header.set_mode(mode)
        renk = RAIL_COLORS.get(mode, RAIL_COLORS["light"])["notes"]
        self._note_button.setIcon(icon("notebook", renk, 18))
        # Prototip `.notebtn`: notların yeşili, ince çerçeveli düğme.
        palette = PALETTES[mode]
        self._note_button.setStyleSheet(
            f"QPushButton {{ color: {renk}; background: transparent; font-weight: 600;"
            f" font-size: 13px; padding: 8px 12px; border-radius: 10px;"
            f" border: 1px solid {mix(renk, palette['border'], 0.7)}; }}"
            f"QPushButton:hover, QPushButton[active=\"true\"] {{"
            f" background: {mix(renk, palette['bg'], 0.88)}; }}")
        self._note_panel.set_mode(mode)
        refresh_shadow(self._note_panel, "dark", True)
        self._lesson.set_mode(mode)
        self._notes.set_mode(mode)
        self._quiz.set_mode(mode)
        self._exercise.set_mode(mode)

    def retranslate(self) -> None:
        labels = self._pane_labels()
        self._segments.set_labels([labels[name] for name in self._panes])
        simgeler = {"lesson": "book", "notes": "file-text", "pdf": "file-text", "quiz": "clipboard",
                    "exercise": "sigma" if self._all_problems() else "terminal"}
        self._segments.set_icons([simgeler.get(name, "") for name in self._panes])

        # Son ders notunun altındaki düğme, notlardan sonra ne geliyorsa
        # onun adını taşıyor. Dil değişince etiketi de değişiyor.
        sonraki = self._pane_after("notes")
        self._notes.set_advance_label(labels[sonraki] if sonraki else None)
        self._refresh_advance_labels()

        self.header.set_back(True, self._language.t("path.back_to_path"))

        t = self._language.t
        self._note_button.setText(f" {t('notebook.take_note')}")
        self._note_button.setToolTip("Ctrl+N")
        for document in self._documents:
            document.enable_quote(t("notebook.add_selection"), t("notebook.copy"))
        self._note_panel.retranslate()
        if self._section is not None:
            self._note_panel.set_section_title(self._language.pick(self._section.title))

        if self._section is not None:
            chapter = self._catalog.chapter(self._section.chapter_id)
            self.header.set_titles(
                self._language.pick(self._section.title),
                f"{self._language.pick(chapter.title) if chapter else ''} · "
                f"{self._section.estimated_minutes} "
                f"{self._language.t('common.minutes')}",
            )

        self._reload_lesson_language()
        self._lesson.retranslate()
        self._notes.retranslate()
        self._quiz.retranslate()
        self._exercise.retranslate()
        self._update_switcher()
