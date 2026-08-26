"""Alıştırma görünümü: yönerge, kod editörü ve sonuç paneli.

Kod arka planda ayrı bir süreçte çalıştırılır; çalıştırma sırasında arayüz
donmaz. Sonuçlar kontrol kontrol listelenir, başarısız olanlarda beklenen ve
bulunan değer yan yana gösterilir.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ..core.catalog import Exercise
from ..core.grader import Feedback, describe, summarise
from ..core.language import LanguageManager
from ..core.runner import RunResult, run_code
from ..resources.theme.tokens import FONTS, SPACING
from ..widgets.code_editor import CodeEditor
from .lesson_view import LessonView

# Çözüm butonu bu kadar başarısız denemeden sonra kendiliğinden görünür.
SOLUTION_AFTER_ATTEMPTS = 3


class RunWorker(QThread):
    """Kodu arka planda çalıştırır."""

    completed = Signal(object)

    def __init__(self, code: str, exercise: Exercise) -> None:
        super().__init__()
        self._code = code
        self._exercise = exercise

    def run(self) -> None:  # noqa: D102
        result = run_code(
            self._code,
            self._exercise.checks,
            self._exercise.timeout_sec,
            self._exercise.directory,
        )
        self.completed.emit(result)


class CheckRow(QFrame):
    """Sonuç panelindeki tek bir kontrol satırı."""

    def __init__(self, feedback: Feedback, language: LanguageManager) -> None:
        super().__init__()
        self.setProperty("banner", "success" if feedback.passed else "danger")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["md"], SPACING["sm"], SPACING["md"], SPACING["sm"])
        layout.setSpacing(SPACING["xs"])

        header = QHBoxLayout()
        header.setSpacing(SPACING["sm"])

        # Renk körlüğü için renge ek olarak simge de kullanılıyor.
        icon = QLabel("✓" if feedback.passed else "✕")
        icon.setProperty("tone", "success" if feedback.passed else "danger")
        icon.setFixedWidth(16)
        header.addWidget(icon, 0, Qt.AlignmentFlag.AlignTop)

        message = QLabel(feedback.message)
        message.setWordWrap(True)
        header.addWidget(message, 1)
        layout.addLayout(header)

        if feedback.has_comparison:
            layout.addWidget(
                self._comparison(
                    language.t("check.stdout.expected"), feedback.expected
                )
            )
            layout.addWidget(
                self._comparison(language.t("check.stdout.actual"), feedback.actual)
            )

    def _comparison(self, label: str, value: str) -> QWidget:
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(SPACING["lg"], 0, 0, 0)
        layout.setSpacing(SPACING["sm"])

        caption = QLabel(f"{label}:")
        caption.setProperty("role", "muted")
        caption.setFixedWidth(90)
        caption.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(caption)

        # Görünmez boşlukları görünür kılmak için değeri tırnak içinde
        # gösteriyoruz; "neden geçmedi" sorusunun cevabı çoğu zaman burada.
        content = QLabel(repr(value) if value else "—")
        content.setWordWrap(True)
        content.setStyleSheet(f"font-family: {FONTS['mono']};")
        content.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(content, 1)

        return row


class ExerciseView(QWidget):
    """Bir alıştırmanın tamamı."""

    solved = Signal(str)  # alıştırma id'si

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._mode = "light"
        self._exercise: Exercise | None = None
        self._worker: RunWorker | None = None
        self._attempts = 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Sol: yönerge. Dar panel olduğu için sıkışık kip kullanılıyor.
        self._prompt = LessonView(language, compact=True)
        splitter.addWidget(self._prompt)

        # Sağ: editör ve sonuçlar
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(
            SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"]
        )
        right_layout.setSpacing(SPACING["md"])

        self._editor = CodeEditor(mode=self._mode)
        self._editor.run_requested.connect(self.run)
        right_layout.addWidget(self._editor, 3)

        right_layout.addLayout(self._build_toolbar())

        self._summary = QLabel()
        self._summary.setWordWrap(True)
        self._summary.setProperty("role", "subtitle")
        self._summary.hide()
        right_layout.addWidget(self._summary)

        self._results_area = QScrollArea()
        self._results_area.setWidgetResizable(True)
        self._results_area.setFrameShape(QFrame.Shape.NoFrame)
        self._results_container = QWidget()
        self._results_layout = QVBoxLayout(self._results_container)
        self._results_layout.setContentsMargins(0, 0, 0, 0)
        self._results_layout.setSpacing(SPACING["sm"])
        self._results_layout.addStretch(1)
        self._results_area.setWidget(self._results_container)
        right_layout.addWidget(self._results_area, 2)

        self._output = QPlainTextEdit()
        self._output.setReadOnly(True)
        self._output.setProperty("role", "code")
        self._output.setMaximumHeight(140)
        self._output.hide()
        right_layout.addWidget(self._output)

        splitter.addWidget(right)
        splitter.setSizes([420, 680])
        layout.addWidget(splitter)

    def _build_toolbar(self) -> QHBoxLayout:
        toolbar = QHBoxLayout()
        toolbar.setSpacing(SPACING["sm"])

        self._difficulty = QLabel()
        self._difficulty.setProperty("role", "muted")
        toolbar.addWidget(self._difficulty)
        toolbar.addStretch(1)

        self._solution_button = QPushButton()
        self._solution_button.setProperty("variant", "ghost")
        self._solution_button.clicked.connect(self._show_solution)
        self._solution_button.hide()
        toolbar.addWidget(self._solution_button)

        self._reset_button = QPushButton()
        self._reset_button.clicked.connect(self._reset)
        toolbar.addWidget(self._reset_button)

        self._run_button = QPushButton()
        self._run_button.setProperty("variant", "primary")
        self._run_button.setShortcut("Ctrl+Return")
        self._run_button.clicked.connect(self.run)
        toolbar.addWidget(self._run_button)

        return toolbar

    # --- içerik -----------------------------------------------------------

    def show_exercise(self, exercise: Exercise) -> None:
        """Alıştırmayı yükler."""
        self._exercise = exercise
        self._attempts = 0

        prompt = exercise.prompt_for(self._language.language)
        if prompt and prompt.exists:
            self._prompt.show_lesson(prompt.path, prompt.is_fallback)
        else:
            self._prompt.show_text(f"# {self._language.pick(exercise.title)}")

        self._editor.setPlainText(exercise.starter_code)
        self._clear_results()
        self._solution_button.hide()
        self.retranslate()

    def _clear_results(self) -> None:
        while self._results_layout.count() > 1:
            item = self._results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._summary.hide()
        self._output.hide()

    # --- çalıştırma -------------------------------------------------------

    def run(self) -> None:
        """Kodu çalıştırır."""
        if self._exercise is None or (self._worker and self._worker.isRunning()):
            return

        self._run_button.setEnabled(False)
        self._run_button.setText(self._language.t("exercise.running"))
        self._clear_results()

        self._worker = RunWorker(self._editor.toPlainText(), self._exercise)
        self._worker.completed.connect(self._on_completed)
        self._worker.start()

    def _on_completed(self, result: RunResult) -> None:
        self._run_button.setEnabled(True)
        self._run_button.setText(self._language.t("exercise.run"))
        self._attempts += 1

        self._summary.setText(summarise(result, self._language))
        self._summary.setProperty("tone", "success" if result.passed else "danger")
        self._summary.style().unpolish(self._summary)
        self._summary.style().polish(self._summary)
        self._summary.show()

        for feedback in describe(result, self._language):
            row = CheckRow(feedback, self._language)
            self._results_layout.insertWidget(self._results_layout.count() - 1, row)

        combined = result.stdout
        if result.stderr:
            combined = f"{combined}\n{result.stderr}" if combined else result.stderr
        if result.truncated:
            combined += f"\n\n[{self._language.t('exercise.output_truncated')}]"
        if combined.strip():
            self._output.setPlainText(combined)
            self._output.show()

        if result.passed and self._exercise is not None:
            self._solution_button.hide()
            self.solved.emit(self._exercise.id)
        elif self._attempts >= SOLUTION_AFTER_ATTEMPTS:
            self._solution_button.show()

    # --- düğmeler ---------------------------------------------------------

    def _reset(self) -> None:
        if self._exercise is None:
            return
        self._editor.setPlainText(self._exercise.starter_code)
        self._clear_results()

    def _show_solution(self) -> None:
        if self._exercise is None:
            return

        confirm = QMessageBox(self)
        confirm.setWindowTitle(self._language.t("exercise.solution_title"))
        confirm.setText(self._language.t("exercise.show_solution") + "?")
        confirm.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm.exec() != QMessageBox.StandardButton.Yes:
            return

        self._editor.setPlainText(self._exercise.solution_code)

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._editor.set_mode(mode)
        self._prompt.set_mode(mode)

    def retranslate(self) -> None:
        self._run_button.setText(self._language.t("exercise.run"))
        self._reset_button.setText(self._language.t("exercise.reset"))
        self._solution_button.setText(self._language.t("exercise.show_solution"))
        self._prompt.retranslate()

        if self._exercise is not None:
            self._difficulty.setText(
                f"{self._language.t('exercise.difficulty')}: "
                f"{'●' * self._exercise.difficulty}{'○' * (3 - self._exercise.difficulty)}"
            )
            prompt = self._exercise.prompt_for(self._language.language)
            if prompt and prompt.exists:
                self._prompt.show_lesson(prompt.path, prompt.is_fallback)
