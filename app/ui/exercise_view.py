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

import html

from ..core.catalog import Exercise
from ..core.grader import Feedback, describe, summarise
from ..core.language import LanguageManager
from ..core.mistakes import explain
from ..core.progress import ProgressStore
from ..core.runner import RunResult, run_code
from ..resources.theme.tokens import FONTS, SPACING
from ..widgets.code_editor import CodeEditor

# Çıktı kutusunun en fazla kaplayacağı yükseklik.
#
# Ölçüldü: bu yazı tipinde satır 14 piksel, dolgu ve kenarlıkla birlikte
# 200 piksel ~13 satır alıyor. İçeriğin beklenen çıktısı en fazla 6 satır;
# kalan yer öğrencinin kendi eklediği `print` satırları ve hata metni için.
# Önce 120 pikseldi (~7 satır) ve panelde alt alta duran "Geçti" satırları
# yüzünden daha da fazlası görünmüyordu.
OUTPUT_MAX_HEIGHT = 200
from ..widgets.effects import repolish
from .lesson_view import LessonView, render_markdown

# Zorluk göstergesi: dolu/boş daire. Renk körlüğü için renge ek olarak biçim.
DIFFICULTY_LABELS = {1: "●○○", 2: "●●○", 3: "●●●"}


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
        # Kaçıncı ipucu kademesine kadar açıldığı. Sıfır: hepsi kapalı.
        self._revealed = 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._build_brief())
        splitter.addWidget(self._build_work())
        # Maketteki oran: yönerge 340-430 arası, kalanı çalışma alanı.
        splitter.setSizes([430, 770])
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter)

    # --- sol: yönerge -----------------------------------------------------

    def _build_brief(self) -> QWidget:
        """Sol panel: başlık, etiketler, yönerge ve ipuçları.

        Hepsi tek bir belge olarak çiziliyor. Önceden başlık ve etiketler Qt
        widget'ı, yönerge ise HTML'di; iki ayrı motorun yazı tipleri ve
        boşlukları tutmadığı için ekran sıkışık ve orantısız duruyordu.
        """
        panel = QFrame()
        panel.setProperty("surface", "plain")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._prompt = LessonView(self._language, compact=True)
        self._prompt.action.connect(self._on_prompt_action)
        layout.addWidget(self._prompt)

        return panel

    def _on_prompt_action(self, action: str) -> None:
        """Yönerge içindeki bağlantılar: ipucu kademelerini açar."""
        if action.startswith("hint-"):
            try:
                level = int(action.split("-", 1)[1])
            except ValueError:
                return
            self._revealed = max(self._revealed, level)
            self._refresh_prompt()

    def _hints_html(self) -> str:
        """İpucu kutusunu maketteki yapıyla üretir.

        Kademeler kapalı başlar; kullanıcı istediği kadarını açar. Açılmış
        kademe metni markdown olarak çevriliyor, böylece içindeki kod
        blokları da renklendiriliyor.
        """
        if self._exercise is None or not self._exercise.hints:
            return ""

        rows = []
        for level, hint in enumerate(self._exercise.hints, start=1):
            text = self._language.pick(hint)
            if not text:
                continue

            if level <= self._revealed:
                body, _ = render_markdown(text)
                inner = f'<div class="tx open">{body}</div>'
                button = ""
            else:
                label = html.escape(self._language.t(f"hint.level{min(level, 3)}"))
                inner = f'<div class="tx">{label}</div>'
                button = (
                    f'<a class="show" href="app:hint-{level}">'
                    f'{html.escape(self._language.t("hint.show"))}</a>'
                )

            rows.append(
                f'<div class="hint"><div class="lv">{level}</div>{inner}{button}</div>'
            )

        if not rows:
            return ""

        title = html.escape(self._language.t("hint.title"))
        return f'<div class="hintbox"><div class="hd">{title}</div>{"".join(rows)}</div>'

    def _chips_html(self) -> str:
        if self._exercise is None:
            return ""

        difficulty = self._exercise.difficulty
        tone = {1: "easy", 2: "mid", 3: "hard"}.get(difficulty, "")
        label = html.escape(
            f"{self._language.t('exercise.difficulty')}: "
            f"{DIFFICULTY_LABELS.get(difficulty, '')}"
        )
        return (
            f'<div class="chips"><span class="chip {tone}">{label}</span></div>'
        )

    def _refresh_prompt(self) -> None:
        """Yönergeyi başlık, etiket ve ipuçlarıyla birlikte yeniden çizer."""
        if self._exercise is None:
            return

        prompt = self._exercise.prompt_for(self._language.language)
        body = prompt.path.read_text(encoding="utf-8") if prompt and prompt.exists else ""
        title = self._language.pick(self._exercise.title)

        self._prompt.set_extra(self._hints_html())
        self._prompt.show_text(f"# {title}\n\n{self._chips_html()}\n\n{body}")

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
        # Sonuç panelinde artık tek bir "Geçti" satırı var (önce her kontrol
        # için bir tane çiziliyordu); açılan yer çıktıya verildi.
        self._output.setMaximumHeight(OUTPUT_MAX_HEIGHT)
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
        self._reset_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._reset_button.clicked.connect(self._reset)
        layout.addWidget(self._reset_button)

        self._run_button = QPushButton()
        self._run_button.setCursor(Qt.CursorShape.PointingHandCursor)
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

        # Yeni alıştırmada ipuçları kapalı başlar.
        self._revealed = 0
        self._refresh_prompt()

        saved = self._store.exercise_code(chapter_id, section_id, exercise.id)
        self._editor.setPlainText(
            saved or exercise.starter_code_for(self._language.language)
        )

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
        self._editor.setPlainText(
            self._exercise.starter_code_for(self._language.language)
        )
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

        # Başlık, etiketler ve ipuçları belgenin içinde olduğu için dil
        # değişince yönergeyi baştan çizmek yeterli.
        if self._exercise is not None:
            self._refresh_prompt()
