"""Bir bölümün ekranı: konu anlatımı, ders notları, sınav ve alıştırmalar.

Sekme çubuğu yerine segmented control kullanılıyor. Yalnızca o bölümde
gerçekten var olan parçalar gösteriliyor: ders notu olmayan bir bölümde
"Ders Notları" seçeneği hiç çıkmıyor.

Bölümde birden fazla alıştırma varsa aralarında geçiş düğmeleri beliriyor.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..core.catalog import Catalog, Section
from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..resources.theme.tokens import SPACING
from ..widgets.common import SegmentedControl
from .exercise_view import ExerciseView
from .header import ScreenHeader
from .lesson_view import LessonView
from .notes_view import NotesView
from .pdf_view import PdfView
from .quiz_view import QuizView


class TopicView(QWidget):
    """Tek bir alt bölümün tüm içeriği."""

    back_requested = Signal()
    progress_changed = Signal()

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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.header = ScreenHeader(language)
        self.header.back_clicked.connect(self.back_requested)

        self._segments = SegmentedControl()
        self._segments.changed.connect(self._show_pane)
        self.header.add_widget(self._segments)

        layout.addWidget(self.header)

        self._stack = QStackedWidget()
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

        # Geçiş şeridi içeriğin üstünde: altta, sonuç panelinin de altında
        # dururken görülmüyordu ve ikinci alıştırmanın varlığı fark
        # edilmiyordu.
        layout.addWidget(self._build_exercise_switcher())
        layout.addWidget(self._stack, 1)

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

        # Numara düğmeleri sağda, eskiden Önceki/Sonraki'nin durduğu yerde.
        # O iki düğme kaldırıldı: numaralar onların yaptığı her şeyi yapıyor
        # ve üstüne kaç alıştırma olduğunu, hangisinin çözüldüğünü gösteriyor.
        self._number_row = QHBoxLayout()
        self._number_row.setSpacing(SPACING["xs"])
        self._number_buttons: list[QPushButton] = []
        layout.addLayout(self._number_row)

        return self._switcher

    # --- içerik -----------------------------------------------------------

    def show_section(self, chapter_id: str, section_id: str) -> None:
        """Bölümü yükler ve mevcut parçalara göre seçenekleri kurar."""
        section = self._catalog.section(chapter_id, section_id)
        if section is None:
            return

        self._section = section
        self._exercises = section.exercises
        self._exercise_index = 0
        self._panes = []

        language_code = self._language.language
        state = self._store.section_state(chapter_id, section_id, len(self._exercises))
        completed = state.status(section.requires_quiz, section.requires_exercises) == "completed"

        for block in section.blocks:
            if block.type == "lesson":
                resolved = block.file_for(language_code)
                self._lesson.show_lesson(
                    resolved.path if resolved else None,
                    resolved.is_fallback if resolved else False,
                    completed=completed,
                )
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
                    self._quiz.show_quiz(resolved.path, block.pass_score)
                    self._panes.append("quiz")

        if self._exercises:
            self._panes.append("exercise")
            self._load_exercise()

        self._lesson.set_meta(self._meta_items(section))
        self._lesson.set_footer(self._footer_items())
        # Bölümü açmak okumak değil: "okundu" işareti, kullanıcı metnin
        # sonuna indiğinde `lesson-read` bildirimiyle konuyor.
        self._update_progress_box(state)
        self.retranslate()
        self._segments.set_current(0, notify=False)
        self._show_pane(0)

    def _meta_items(self, section) -> list[str]:
        """Ders başlığının altındaki bilgi satırının parçaları.

        Başına simge konuyor; makette de öyle ve satır bir metin yığını
        olmaktan çıkıp okunabilir hâle geliyor.
        """
        items = [f"📖  {section.estimated_minutes} {self._language.t('common.minutes')}"]

        if self._exercises:
            items.append(
                f"✏️  {len(self._exercises)} {self._language.t('tabs.exercise').lower()}"
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

    def _pane_labels(self) -> dict[str, str]:
        """Bölüm sekmelerinin seçili dildeki adları."""
        return {
            "lesson": self._language.t("tabs.lesson"),
            "notes": self._language.t("tabs.pdf"),
            "pdf": self._language.t("tabs.pdf_file"),
            "quiz": self._language.t("tabs.quiz"),
            "exercise": self._language.t("tabs.exercise"),
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
        elif following:
            buttons.append(("next-section", f"{self._language.t('nav.next')}  →", True))

        return buttons

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
            if target:
                self.show_section(target.chapter_id, target.id)

    def _on_notes_advance(self) -> None:
        """Son ders notunun altındaki düğme: bölümün sonraki adımına geç."""
        hedef = self._pane_after("notes")
        if hedef and hedef in self._panes:
            self._segments.set_current(self._panes.index(hedef))

    def _load_exercise(self) -> None:
        if not self._exercises or self._section is None:
            return
        self._exercise.show_exercise(
            self._exercises[self._exercise_index],
            self._section.chapter_id,
            self._section.id,
        )
        self._update_switcher()

    def _update_switcher(self) -> None:
        many = len(self._exercises) > 1
        self._switcher.setVisible(many and self._current_pane() == "exercise")
        if not many:
            return

        self._switcher_label.setText(
            f"{self._language.t('tabs.exercise')} "
            f"{self._exercise_index + 1} / {len(self._exercises)}"
        )
        self._rebuild_numbers()

    def _rebuild_numbers(self) -> None:
        """Alıştırma numaralarını yeniden çizer.

        Çözülmüş alıştırmanın numarasının yanında onay işareti duruyor;
        böylece kaç tanesini bitirdiğin de aynı yerden görünüyor.
        """
        while self._number_row.count():
            item = self._number_row.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
                item.widget().deleteLater()
        self._number_buttons = []

        if self._section is None:
            return

        for index, exercise in enumerate(self._exercises):
            solved = self._store.exercise_solved(
                self._section.chapter_id, self._section.id, exercise.id
            )
            button = QPushButton(f"{index + 1} ✓" if solved else str(index + 1))
            button.setProperty("variant", "number")
            button.setProperty("active", "true" if index == self._exercise_index else "false")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setToolTip(self._language.pick(exercise.title))
            button.clicked.connect(lambda _=False, i=index: self._go_exercise(i))
            self._number_row.addWidget(button)
            self._number_buttons.append(button)

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
        self._stack.setCurrentWidget(widget)
        self._update_switcher()

    def _refresh_progress(self) -> None:
        """İlerlemeyi veritabanından tazeleyip kutuya yazar."""
        if self._section is None:
            return
        state = self._store.section_state(
            self._section.chapter_id, self._section.id, len(self._exercises)
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

        parts: list[float] = []
        labels: list[str] = []

        if "lesson" in self._panes:
            done = bool(state.lesson_read)
            parts.append(1.0 if done else 0.0)
            labels.append(
                f"{'✓' if done else '○'} {self._language.t('progress.lesson')}"
            )

        if "quiz" in self._panes:
            done = bool(state.quiz_passed)
            parts.append(1.0 if done else 0.0)
            score = f" ({state.quiz_score})" if state.quiz_score is not None else ""
            labels.append(
                f"{'✓' if done else '○'} {self._language.t('progress.quiz')}{score}"
            )

        if self._exercises:
            total = len(self._exercises)
            solved = state.exercises_solved
            parts.append(solved / total)
            labels.append(
                f"{'✓' if solved >= total else '○'} "
                f"{self._language.t('progress.exercises')} {solved}/{total}"
            )

        percent = round(sum(parts) * 100 / len(parts)) if parts else 0
        self._lesson.set_progress(percent, "  ·  ".join(labels))

    # --- olaylar ----------------------------------------------------------

    def _on_quiz_completed(self, score: int, passed: bool) -> None:
        if self._section is None:
            return
        self._store.record_quiz(
            self._section.chapter_id, self._section.id, score, passed
        )
        self._refresh_progress()
        self.progress_changed.emit()

    def _on_exercise_solved(self, _exercise_id: str) -> None:
        self._refresh_progress()
        # Numara düğmelerindeki onay işareti veritabanından okunuyor;
        # çözüldüğü anda yenilenmezse tik ancak başka bir alıştırmaya
        # geçince ya da bölüm yeniden açılınca beliriyordu.
        self._update_switcher()
        self.progress_changed.emit()

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self.header.set_mode(mode)
        self._lesson.set_mode(mode)
        self._notes.set_mode(mode)
        self._quiz.set_mode(mode)
        self._exercise.set_mode(mode)

    def retranslate(self) -> None:
        labels = self._pane_labels()
        self._segments.set_labels([labels[name] for name in self._panes])

        # Son ders notunun altındaki düğme, notlardan sonra ne geliyorsa
        # onun adını taşıyor. Dil değişince etiketi de değişiyor.
        sonraki = self._pane_after("notes")
        self._notes.set_advance_label(labels[sonraki] if sonraki else None)

        self.header.set_back(True, self._language.t("path.back_to_path"))

        if self._section is not None:
            chapter = self._catalog.chapter(self._section.chapter_id)
            self.header.set_titles(
                self._language.pick(self._section.title),
                f"{self._language.pick(chapter.title) if chapter else ''} · "
                f"{self._section.estimated_minutes} "
                f"{self._language.t('common.minutes')}",
            )

        self._lesson.retranslate()
        self._notes.retranslate()
        self._quiz.retranslate()
        self._exercise.retranslate()
        self._update_switcher()
