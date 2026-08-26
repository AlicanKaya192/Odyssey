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
        self._lesson = LessonView(language)
        self._notes = NotesView(language)
        self._pdf = PdfView(language)
        self._quiz = QuizView(language)
        self._exercise = ExerciseView(language, store)

        for widget in (self._lesson, self._notes, self._pdf, self._quiz, self._exercise):
            self._stack.addWidget(widget)

        self._quiz.completed.connect(self._on_quiz_completed)
        self._exercise.solved.connect(self._on_exercise_solved)

        layout.addWidget(self._stack, 1)
        layout.addWidget(self._build_exercise_switcher())

    def _build_exercise_switcher(self) -> QWidget:
        """Birden fazla alıştırma varsa aralarında geçiş şeridi."""
        self._switcher = QFrame()
        self._switcher.setProperty("role", "topbar")
        self._switcher.hide()

        layout = QHBoxLayout(self._switcher)
        layout.setContentsMargins(
            SPACING["lg"], SPACING["sm"], SPACING["lg"], SPACING["sm"]
        )
        layout.setSpacing(SPACING["sm"])

        self._switcher_label = QLabel()
        self._switcher_label.setProperty("role", "muted")
        layout.addWidget(self._switcher_label)
        layout.addStretch(1)

        self._previous_exercise = QPushButton()
        self._previous_exercise.setProperty("variant", "small")
        self._previous_exercise.clicked.connect(lambda: self._step_exercise(-1))
        layout.addWidget(self._previous_exercise)

        self._next_exercise = QPushButton()
        self._next_exercise.setProperty("variant", "small")
        self._next_exercise.clicked.connect(lambda: self._step_exercise(1))
        layout.addWidget(self._next_exercise)

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

        self._store.mark_lesson_read(chapter_id, section_id)
        self._update_progress_box(state)
        self.retranslate()
        self._segments.set_current(0, notify=False)
        self._show_pane(0)

    def _load_exercise(self) -> None:
        if not self._exercises or self._section is None:
            return
        self._exercise.show_exercise(
            self._exercises[self._exercise_index],
            self._section.chapter_id,
            self._section.id,
        )
        self._update_switcher()

    def _step_exercise(self, delta: int) -> None:
        self._exercise_index = max(
            0, min(self._exercise_index + delta, len(self._exercises) - 1)
        )
        self._load_exercise()

    def _update_switcher(self) -> None:
        many = len(self._exercises) > 1
        self._switcher.setVisible(many and self._current_pane() == "exercise")
        if not many:
            return
        self._switcher_label.setText(
            f"{self._language.t('tabs.exercise')} "
            f"{self._exercise_index + 1} / {len(self._exercises)}"
        )
        self._previous_exercise.setEnabled(self._exercise_index > 0)
        self._next_exercise.setEnabled(self._exercise_index < len(self._exercises) - 1)

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

    def _update_progress_box(self, state) -> None:
        if self._section is None:
            return

        parts = []
        if "lesson" in self._panes:
            parts.append(1 if state.lesson_read else 0)
        if "quiz" in self._panes:
            parts.append(1 if state.quiz_passed else 0)
        if self._exercises:
            parts.append(state.exercises_solved / max(len(self._exercises), 1))

        percent = round(sum(parts) * 100 / len(parts)) if parts else 0
        caption = f"{self._language.t('tabs.exercise')}: {state.exercises_solved}/{len(self._exercises)}"
        self._lesson.set_progress(percent, caption)

    # --- olaylar ----------------------------------------------------------

    def _on_quiz_completed(self, score: int, passed: bool) -> None:
        if self._section is None:
            return
        self._store.record_quiz(
            self._section.chapter_id, self._section.id, score, passed
        )
        self.progress_changed.emit()

    def _on_exercise_solved(self, _exercise_id: str) -> None:
        self.progress_changed.emit()

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self.header.set_mode(mode)
        self._lesson.set_mode(mode)
        self._notes.set_mode(mode)
        self._quiz.set_mode(mode)
        self._exercise.set_mode(mode)

    def retranslate(self) -> None:
        labels = {
            "lesson": self._language.t("tabs.lesson"),
            "notes": self._language.t("tabs.pdf"),
            "pdf": self._language.t("tabs.pdf_file"),
            "quiz": self._language.t("tabs.quiz"),
            "exercise": self._language.t("tabs.exercise"),
        }
        self._segments.set_labels([labels[name] for name in self._panes])

        self.header.set_back(True, self._language.t("path.back_to_path"))
        self._previous_exercise.setText(self._language.t("nav.previous"))
        self._next_exercise.setText(self._language.t("nav.next"))

        if self._section is not None:
            chapter = self._catalog.chapter(self._section.chapter_id)
            self.header.set_titles(
                self._language.pick(self._section.title),
                f"{self._language.pick(chapter.title) if chapter else ''} · "
                f"{self._section.estimated_minutes} dk",
            )

        self._lesson.retranslate()
        self._notes.retranslate()
        self._quiz.retranslate()
        self._exercise.retranslate()
        self._update_switcher()
