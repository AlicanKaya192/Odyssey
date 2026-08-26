"""Alıştırma görünümü: yönerge, kademeli ipuçları, kod editörü ve sonuçlar.

Kod arka planda ayrı bir süreçte çalıştırılır; çalışırken arayüz donmaz.

İki tasarım kararı burada belirleyici:

- **Kademeli ipucu.** Tek bir "çözümü göster" düğmesi kullanıcıyı ya hiç
  yardım almamaya ya da doğrudan cevabı görmeye zorluyor. Üç kademe, tıkanan
  kişinin ihtiyacı kadar yardım almasını sağlıyor.
- **Hata açıklaması.** Python'un hata mesajları doğru ama öğretmiyor. Hatanın
  altında ne anlama geldiği ve nasıl düzeltileceği yazıyor.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ..core.catalog import Exercise
from ..core.grader import Feedback, describe, summarise
from ..core.language import LanguageManager
from ..core.mistakes import explain
from ..core.progress import ProgressStore
from ..core.runner import RunResult, run_code
from ..resources.theme.tokens import FONTS, SPACING
from ..widgets.code_editor import CodeEditor
from ..widgets.common import Chip, section_label
from ..widgets.effects import repolish
from .lesson_view import LessonView

DIFFICULTY_TONES = {1: "success", 2: "warning", 3: "danger"}


class RunWorker(QThread):
    """Kodu arka planda çalıştırır."""

    completed = Signal(object)

    def __init__(self, code: str, exercise: Exercise) -> None:
        super().__init__()
        self._code = code
        self._exercise = exercise

    def run(self) -> None:  # noqa: D102
        self.completed.emit(
            run_code(
                self._code,
                self._exercise.checks,
                self._exercise.timeout_sec,
                self._exercise.directory,
            )
        )


class HintRow(QFrame):
    """Tek bir ipucu kademesi. Kapalıyken yalnızca başlığı görünür."""

    revealed = Signal(int)

    def __init__(
        self,
        level: int,
        text: str,
        language: LanguageManager,
        revealed: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._text = text
        self._language = language
        self._level = level
        self._revealed = revealed

        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            SPACING["md"], SPACING["sm"], SPACING["md"], SPACING["sm"]
        )
        layout.setSpacing(SPACING["sm"])

        self._badge = QLabel(str(level))
        self._badge.setProperty("role", "chip")
        self._badge.setProperty("tone", "accent")
        self._badge.setFixedWidth(26)
        layout.addWidget(self._badge, 0, Qt.AlignmentFlag.AlignTop)

        self._label = QLabel()
        self._label.setWordWrap(True)
        self._label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self._label, 1)

        self._button = QPushButton()
        self._button.setProperty("variant", "small")
        self._button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._button.clicked.connect(self.reveal)
        layout.addWidget(self._button, 0, Qt.AlignmentFlag.AlignTop)

        self._refresh()

    def reveal(self) -> None:
        self._revealed = True
        self._refresh()
        self.revealed.emit(self._level)

    def _refresh(self) -> None:
        if self._revealed:
            self._label.setText(self._text)
            self._label.setProperty("role", "")
            self._button.hide()
        else:
            self._label.setText(self._language.t(f"hint.level{min(self._level, 3)}"))
            self._label.setProperty("role", "muted")
            self._button.setText(self._language.t("hint.show"))
            self._button.show()
        repolish(self._label)


class HintBox(QFrame):
    """İpucu kademelerini taşıyan kutu."""

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self.setProperty("surface", "card")

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(
            SPACING["md"], SPACING["sm"], SPACING["md"], SPACING["sm"]
        )
        self._title = section_label("")
        header_layout.addWidget(self._title)
        header_layout.addStretch(1)
        self._layout.addWidget(header)

        self._rows: list[HintRow] = []
        # Dil değişince satırlar yeniden kuruluyor; kullanıcının açtığı
        # kademeler kapanmasın diye kaçıncıya kadar açtığı hatırlanıyor.
        self._revealed_upto = 1

    def reset(self) -> None:
        """Yeni bir alıştırmaya geçerken açılmış ipuçlarını sıfırlar."""
        self._revealed_upto = 1

    def note_revealed(self, level: int) -> None:
        self._revealed_upto = max(self._revealed_upto, level)

    def set_hints(self, hints: list[dict]) -> None:
        # `deleteLater()` tek başına yetmiyor: widget yerleşimden hemen
        # çıkmadığı için satırlar üst üste birikiyordu. Önce yerleşimden
        # koparıp sonra siliyoruz.
        for row in self._rows:
            self._layout.removeWidget(row)
            row.setParent(None)
            row.deleteLater()
        self._rows = []

        if not hints:
            self.hide()
            return

        for index, hint in enumerate(hints, start=1):
            text = self._language.pick(hint)
            if not text:
                continue
            # İlk kademe kendiliğinden açık: yardım isteyen kişiyi bir tık
            # daha uğraştırmanın öğretici bir tarafı yok.
            row = HintRow(
                index, text, self._language, revealed=(index <= self._revealed_upto)
            )
            row.revealed.connect(self.note_revealed)
            self._layout.addWidget(row)
            self._rows.append(row)

        self.setVisible(bool(self._rows))

    def retranslate(self) -> None:
        self._title.setText(self._language.t("hint.title").upper())
        for row in self._rows:
            row._refresh()


class CheckRow(QFrame):
    """Sonuç panelindeki tek bir kontrol satırı."""

    def __init__(
        self,
        feedback: Feedback,
        language: LanguageManager,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setProperty("check", "passed" if feedback.passed else "failed")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            SPACING["md"], SPACING["sm"], SPACING["md"], SPACING["sm"]
        )
        layout.setSpacing(SPACING["xs"])

        header = QHBoxLayout()
        header.setSpacing(SPACING["sm"])

        # Renk körlüğü için renge ek olarak simge de var.
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
                self._comparison(language.t("check.stdout.expected"), feedback.expected)
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
        caption.setFixedWidth(86)
        caption.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(caption)

        # Değeri tırnak içinde gösteriyoruz: "neden geçmedi" sorusunun cevabı
        # çoğu zaman görünmeyen bir boşluk oluyor.
        content = QLabel(repr(value) if value else "—")
        content.setWordWrap(True)
        content.setStyleSheet(f"font-family: {FONTS['mono']};")
        content.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(content, 1)

        return row


class MistakeRow(QFrame):
    """Hatanın ne anlama geldiğini anlatan kutu."""

    def __init__(self, text: str, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("banner", "accent")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            SPACING["md"], SPACING["sm"], SPACING["md"], SPACING["sm"]
        )
        layout.setSpacing(SPACING["xs"])

        heading = QLabel(title)
        heading.setProperty("tone", "accent")
        heading.setProperty("role", "heading")
        layout.addWidget(heading)

        body = QLabel(text)
        body.setWordWrap(True)
        body.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(body)


class ExerciseView(QWidget):
    """Bir alıştırmanın tamamı."""

    solved = Signal(str)

    def __init__(
        self,
        language: LanguageManager,
        store: ProgressStore,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._store = store
        self._mode = "light"
        self._exercise: Exercise | None = None
        self._chapter_id = ""
        self._section_id = ""
        self._worker: RunWorker | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._build_brief())
        splitter.addWidget(self._build_work())
        splitter.setSizes([420, 720])
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter)

    # --- sol: yönerge -----------------------------------------------------

    def _build_brief(self) -> QWidget:
        """Sol panel: başlık, etiketler, yönerge ve ipuçları.

        Dışarıya ayrıca bir kaydırma alanı konmuyor: yönergenin kendi
        kaydırması var, iç içe iki kaydırma alanı yüksekliği belirsiz
        bırakıp ipucu kutusunun taşmasına yol açıyordu.
        """
        panel = QFrame()
        panel.setProperty("surface", "plain")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(
            SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"]
        )
        layout.setSpacing(SPACING["sm"])

        self._title = QLabel()
        self._title.setProperty("role", "subtitle")
        self._title.setWordWrap(True)
        layout.addWidget(self._title)

        chips = QHBoxLayout()
        chips.setSpacing(SPACING["xs"])
        self._difficulty_chip = Chip()
        self._time_chip = Chip()
        chips.addWidget(self._difficulty_chip)
        chips.addWidget(self._time_chip)
        chips.addStretch(1)
        layout.addLayout(chips)

        self._prompt = LessonView(self._language, compact=True)
        layout.addWidget(self._prompt, 1)

        self._hints = HintBox(self._language)
        self._hints.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum
        )
        layout.addWidget(self._hints, 0)

        return panel

    # --- sağ: editör ve sonuçlar -----------------------------------------

    def _build_work(self) -> QWidget:
        holder = QWidget()
        layout = QVBoxLayout(holder)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._editor = CodeEditor(mode=self._mode)
        self._editor.run_requested.connect(self.run)
        layout.addWidget(self._editor, 3)

        layout.addWidget(self._build_runbar())

        self._results_area = QScrollArea()
        self._results_area.setWidgetResizable(True)
        self._results_area.setFrameShape(QFrame.Shape.NoFrame)

        results_holder = QWidget()
        self._results_layout = QVBoxLayout(results_holder)
        self._results_layout.setContentsMargins(
            SPACING["lg"], SPACING["md"], SPACING["lg"], SPACING["lg"]
        )
        self._results_layout.setSpacing(SPACING["sm"])

        self._summary = QLabel()
        self._summary.setWordWrap(True)
        self._summary.setProperty("role", "subtitle")
        self._summary.hide()
        self._results_layout.addWidget(self._summary)

        self._results_layout.addStretch(1)
        self._results_area.setWidget(results_holder)
        layout.addWidget(self._results_area, 2)

        self._output = QPlainTextEdit()
        self._output.setReadOnly(True)
        self._output.setProperty("role", "output")
        self._output.setMaximumHeight(120)
        self._output.hide()
        layout.addWidget(self._output)

        return holder

    def _build_runbar(self) -> QWidget:
        bar = QFrame()
        bar.setProperty("role", "topbar")

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(
            SPACING["lg"], SPACING["sm"], SPACING["lg"], SPACING["sm"]
        )
        layout.setSpacing(SPACING["sm"])

        self._shortcut_hint = QLabel()
        self._shortcut_hint.setProperty("role", "muted")
        layout.addWidget(self._shortcut_hint)
        layout.addStretch(1)

        self._reset_button = QPushButton()
        self._reset_button.clicked.connect(self._reset)
        layout.addWidget(self._reset_button)

        self._run_button = QPushButton()
        self._run_button.setProperty("variant", "primary")
        self._run_button.clicked.connect(self.run)
        layout.addWidget(self._run_button)

        return bar

    # --- içerik -----------------------------------------------------------

    def show_exercise(self, exercise: Exercise, chapter_id: str, section_id: str) -> None:
        """Alıştırmayı yükler ve varsa daha önce yazılan kodu geri getirir."""
        self._exercise = exercise
        self._chapter_id = chapter_id
        self._section_id = section_id

        prompt = exercise.prompt_for(self._language.language)
        if prompt and prompt.exists:
            self._prompt.show_lesson(prompt.path, prompt.is_fallback)
        else:
            self._prompt.show_text("")

        saved = self._store.exercise_code(chapter_id, section_id, exercise.id)
        self._editor.setPlainText(saved or exercise.starter_code)

        self._hints.reset()
        self._hints.set_hints(exercise.hints)
        self._clear_results()
        self.retranslate()

    def _clear_results(self) -> None:
        while self._results_layout.count() > 2:
            item = self._results_layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
        self._summary.hide()
        self._output.hide()

    # --- çalıştırma -------------------------------------------------------

    def run(self) -> None:
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

        if self._exercise is not None:
            self._store.save_exercise(
                self._chapter_id,
                self._section_id,
                self._exercise.id,
                self._editor.toPlainText(),
                solved=result.passed,
                count_attempt=True,
            )

        self._summary.setText(summarise(result, self._language))
        self._summary.setProperty("tone", "success" if result.passed else "danger")
        repolish(self._summary)
        self._summary.show()

        # Hata varsa önce ne anlama geldiğini anlat, sonra kontrolleri listele.
        explanation = explain(result.error)
        if explanation is not None:
            self._insert(
                MistakeRow(
                    self._language.t(explanation.key, **explanation.values),
                    self._language.t("mistake.title"),
                )
            )

        for feedback in describe(result, self._language):
            self._insert(CheckRow(feedback, self._language))

        combined = result.stdout
        if result.stderr:
            combined = f"{combined}\n{result.stderr}" if combined else result.stderr
        if result.truncated:
            combined += f"\n\n[{self._language.t('exercise.output_truncated')}]"
        if combined.strip():
            self._output.setPlainText(combined)
            self._output.show()

        if result.passed and self._exercise is not None:
            self.solved.emit(self._exercise.id)

    def _insert(self, widget: QWidget) -> None:
        self._results_layout.insertWidget(self._results_layout.count() - 1, widget)

    def _reset(self) -> None:
        if self._exercise is None:
            return
        self._editor.setPlainText(self._exercise.starter_code)
        self._clear_results()

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._editor.set_mode(mode)
        self._prompt.set_mode(mode)

    def retranslate(self) -> None:
        self._run_button.setText(self._language.t("exercise.run"))
        self._reset_button.setText(self._language.t("exercise.reset"))
        self._shortcut_hint.setText("Ctrl + Enter")
        self._hints.retranslate()
        self._prompt.retranslate()

        if self._exercise is None:
            return

        self._title.setText(self._language.pick(self._exercise.title))

        difficulty = self._exercise.difficulty
        self._difficulty_chip.setText(
            f"{self._language.t('exercise.difficulty')}: "
            f"{'●' * difficulty}{'○' * max(0, 3 - difficulty)}"
        )
        self._difficulty_chip.set_tone(DIFFICULTY_TONES.get(difficulty, ""))
        self._time_chip.setText(f"~{self._exercise.timeout_sec * 30 // 60 or 5} dk")

        prompt = self._exercise.prompt_for(self._language.language)
        if prompt and prompt.exists:
            self._prompt.show_lesson(prompt.path, prompt.is_fallback)
        self._hints.set_hints(self._exercise.hints)
