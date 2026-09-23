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
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

import html
import json
from pathlib import Path

from ..core.catalog import Exercise
from ..core.grader import Feedback, describe, summarise
from ..core.language import LanguageManager
from ..core.mistakes import explain
from ..core.progress import ProgressStore
from ..core.runner import RunResult, run_code
from ..resources.theme.tokens import FONTS, SPACING
from ..widgets.code_editor import CodeEditor
from ..widgets.common import SegmentedControl
from ..widgets.draw_pad import clean_drawing, empty_drawing
from ..widgets.problem_panel import ProblemPanel

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
from .tables_window import TablesWindow

# Zorluk göstergesi: dolu/boş daire. Renk körlüğü için renge ek olarak biçim.
DIFFICULTY_LABELS = {1: "●○○", 2: "●●○", 3: "●●●"}


def exercise_key(exercise: Exercise) -> str:
    """Alıştırmayı bütün içerik içinde tek olarak adlandırır.

    SQL alıştırmalarının veritabanı bu adla açılıyor. Yalnızca alıştırma
    kimliği yetmiyor: iki farklı bölümde aynı adlı alıştırma olabiliyor ve
    ikisi aynı veritabanını paylaşırsa biri ötekinin tohumunu eziyor.
    """
    parcalar = exercise.directory.parts
    if len(parcalar) >= 4:
        return "/".join((parcalar[-4], parcalar[-3], exercise.id))
    return exercise.id


# Kaç yanlış denemeden sonra çözüm yolları kendiliğinden açılıyor.
REVEAL_AFTER_ATTEMPTS = 2

# Problemde sol paneldeki iki sekme.
BRIEF_PROMPT = 0
BRIEF_SOLUTIONS = 1


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
                language=self._exercise.language,
                exercise_key=exercise_key(self._exercise),
            )
        )




class SnapshotWorker(QThread):
    """Kod çalıştırmadan yalnızca tabloların hâlini alır.

    Boş SQL gönderiliyor: hiçbir toplu iş çalışmıyor ama veritabanı
    kuruluyor ve anlık görüntü alınıyor. Normal çalıştırma yolundan
    geçirilmiyor, çünkü orası ilerlemeyi kaydediyor ve deneme sayıyor —
    "Tablolar"a basmak bir deneme değil.
    """

    completed = Signal(object)

    def __init__(self, exercise: Exercise) -> None:
        super().__init__()
        self._exercise = exercise

    def run(self) -> None:  # noqa: D102
        self.completed.emit(
            run_code(
                "",
                [],
                self._exercise.timeout_sec,
                self._exercise.directory,
                language=self._exercise.language,
                exercise_key=exercise_key(self._exercise),
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


class ArtifactRow(QFrame):
    """Kullanıcının kodunun ürettiği görsel.

    Alıştırma bir grafik kaydediyorsa o grafik burada görünüyor. Önceden
    dosya üretiliyor, doğrulanıyor ve çalışma klasörüyle birlikte
    siliniyordu: "eksen sıfırdan başlamalı" diyen bir ders, öğrencinin
    çizdiği grafiği gösteremiyordu.

    Görsel panele sığacak şekilde küçültülüyor ama **oranı korunuyor**;
    ezilmiş bir grafik yanlış bir şey öğretir.
    """

    MAX_HEIGHT = 320

    def __init__(
        self, path: Path, caption: str, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setProperty("role", "artifact")
        self._path = path

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            SPACING["md"], SPACING["md"], SPACING["md"], SPACING["md"]
        )
        layout.setSpacing(SPACING["xs"])

        baslik = QLabel(caption)
        baslik.setProperty("role", "muted")
        layout.addWidget(baslik)

        self._image = QLabel()
        self._image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._pixmap = QPixmap(str(path))
        layout.addWidget(self._image)

        ad = QLabel(path.name)
        ad.setProperty("role", "muted")
        ad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(ad)

        self._rescale()

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._rescale()

    def _rescale(self) -> None:
        """Görseli panele sığdırır.

        Panelin genişliği ders okurken de alıştırma çözerken de değişiyor;
        ölçek her seferinde yeniden hesaplanıyor.
        """
        if self._pixmap.isNull():
            self._image.setText(self._path.name)
            return

        alan = max(120, self.width() - 2 * SPACING["md"])
        olcekli = self._pixmap.scaled(
            alan,
            self.MAX_HEIGHT,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._image.setPixmap(olcekli)


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
    # Yönergenin altındaki "devam" düğmesi: sonraki alıştırma ya da bölüm.
    advance = Signal()

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
        self._snapshot: SnapshotWorker | None = None
        # Son çalıştırmanın sonundaki tablo hâli ve onu gösteren pencere.
        self._tables: list[dict] = []
        self._tables_window: TablesWindow | None = None
        # Açılmış ipucu kademeleri. Her kademe kendi başına açılıyor:
        # "kaçıncıya kadar açık" diye tek bir sayı tutulduğunda son
        # kademeye basmak öncekileri de açıyor ve kademeli yardım fikri
        # ortadan kalkıyor.
        self._revealed: set[int] = set()
        self._advance_label: str | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._build_brief())
        # Sağ taraf alıştırmanın türüne göre: kod alıştırmasında editör,
        # matematik probleminde cevap alanları.
        self._work_stack = QStackedWidget()
        self._code_work = self._build_work()
        self._work_stack.addWidget(self._code_work)
        self._work_stack.addWidget(self._build_problem_work())
        splitter.addWidget(self._work_stack)
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

        # Problemde çözüm açılınca "Yönerge / Çözüm yolları" sekmeleri
        # beliriyor. Çözüm sağdaki kâğıdın altına açıldığında kâğıdı
        # eziyordu (Alican bildirdi); solda açılınca kişi kendi kâğıdı sağda
        # dururken çözümü okuyup satır satır karşılaştırabiliyor.
        self._brief_tabs = SegmentedControl()
        self._brief_tabs.changed.connect(self._on_brief_tab)
        tabs_row = QHBoxLayout()
        tabs_row.setContentsMargins(SPACING["lg"], SPACING["sm"], SPACING["lg"], 0)
        tabs_row.addWidget(self._brief_tabs)
        tabs_row.addStretch(1)
        self._brief_tabs_holder = QWidget()
        self._brief_tabs_holder.setProperty("role", "bare")
        self._brief_tabs_holder.setLayout(tabs_row)
        self._brief_tabs_holder.hide()
        layout.addWidget(self._brief_tabs_holder)

        self._brief_stack = QStackedWidget()
        self._prompt = LessonView(self._language, compact=True)
        self._prompt.action.connect(self._on_prompt_action)
        self._brief_stack.addWidget(self._prompt)
        self._solutions = LessonView(self._language, compact=True)
        self._brief_stack.addWidget(self._solutions)
        layout.addWidget(self._brief_stack)

        return panel

    def _on_brief_tab(self, index: int) -> None:
        self._brief_stack.setCurrentIndex(index)

    def _on_prompt_action(self, action: str) -> None:
        """Yönerge içindeki bağlantılar: ipucu kademeleri ve alttaki
        "devam" düğmesi."""
        if action == "advance":
            self.advance.emit()
            return
        if action.startswith("hint-"):
            try:
                level = int(action.split("-", 1)[1])
            except ValueError:
                return
            self._revealed.add(level)
            self._prompt.update_extra(self._hints_html())

    def set_advance_label(self, label: str | None) -> None:
        """Yönergenin en altındaki "devam" düğmesi.

        Ders ve not sayfalarının altında ileri düğmesi vardı, alıştırmada
        yoktu; bir alıştırmayı bitiren kişi sonrakine geçmek için sağ
        üstteki numaraları aramak zorunda kalıyordu. `None` verilirse
        düğme çizilmiyor (son alıştırmadayken sonraki bölüm kilitli).
        """
        self._advance_label = label
        self._prompt.set_footer(
            [("advance" if label else "", f"{label or ''}  →", True)]
        )

    def _hint_label(self, level: int) -> str:
        """Kapalı bir kademenin etiketi.

        Etiket kademenin **sırasına** göre seçiliyor, numarasına göre değil:
        dört ipuçlu bir alıştırmada üçüncü kademe "çözümün tamamı" değil,
        yalnızca sonuncusu öyle.
        """
        toplam = len(self._exercise.hints) if self._exercise else 0
        # Problemde çözüm ipuçlarda değil, çözüm yollarında; son ipucu da
        # yalnızca bir yönlendirme.
        if self._exercise is not None and self._exercise.is_problem:
            return "hint.level1" if level == 1 else "hint.level2"
        if level >= toplam:
            return "hint.level3"
        if level == 1:
            return "hint.level1"
        return "hint.level2"

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

            if level in self._revealed:
                body, _ = render_markdown(text)
                inner = f'<div class="tx open">{body}</div>'
                button = ""
            else:
                label = html.escape(self._language.t(self._hint_label(level)))
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

        self._prompt.set_base_dir(self._exercise.directory)
        self._prompt.show_text(
            f"# {title}\n\n{self._chips_html()}\n\n{body}", extra=self._hints_html()
        )

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

    def _build_problem_work(self) -> QWidget:
        """Problemin sağ tarafı: çalışma kâğıdı ve cevap. Tamamı kâğıda ait;
        çözüm yolları sol panelde açılıyor."""
        self._problem = ProblemPanel(self._language)
        self._problem.checked.connect(self._on_problem_checked)
        self._problem.work_changed.connect(self._save_problem_state)
        self._problem.reveal_requested.connect(lambda: self._reveal_solutions(True))

        # Çözüm açık mı; kayıtta da tutuluyor, bölüme dönünce açık kalsın.
        self._revealed_solution = False
        return self._problem

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

        # Yalnızca SQL alıştırmalarında görünüyor: Python alıştırmasında
        # gösterilecek bir tablo yok.
        self._tables_button = QPushButton()
        self._tables_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._tables_button.clicked.connect(self._show_tables)
        self._tables_button.hide()
        layout.addWidget(self._tables_button)

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

    def code_for_note(self) -> tuple[str, str] | None:
        """Nota eklenecek kod ve dili: seçim varsa seçim, yoksa editörün tamamı.

        Dil etiketi markdown'ın tanıdığı ad: T-SQL alıştırması `sql`.
        """
        if self._exercise is None or self._exercise.is_problem:
            return None
        cursor = self._editor.textCursor()
        if cursor.hasSelection():
            code = cursor.selectedText().replace(" ", "\n")
        else:
            code = self._editor.toPlainText()
        if not code.strip():
            return None
        return code, "sql" if self._exercise.language == "tsql" else "python"

    def show_exercise(self, exercise: Exercise, chapter_id: str, section_id: str) -> None:
        """Alıştırmayı yükler ve varsa daha önce yazılan kodu geri getirir."""
        self._exercise = exercise
        self._chapter_id = chapter_id
        self._section_id = section_id

        # Yeni alıştırmada ipuçları kapalı başlar.
        self._revealed = set()
        self._refresh_prompt()

        if exercise.is_problem:
            state = problem_state(self._store.exercise_code(chapter_id, section_id, exercise.id))
            self._problem.show_problem(
                exercise.answers, state["answers"], state["drawing"], exercise.symbols
            )
            # Yeni problem her zaman yönergeyle açılıyor; önceki problemin
            # çözüm sekmesi açık kalırsa kişi yanlış problemin çözümünü görür.
            # Bu problemin çözümü daha önce açıldıysa sekmesi hazır bekliyor.
            self._revealed_solution = False
            self._show_brief_tabs(False)
            self._reveal_solutions(state["revealed"], save=False, focus=False)
            self._work_stack.setCurrentIndex(1)
            self.retranslate()
            return
        self._work_stack.setCurrentIndex(0)
        self._revealed_solution = False
        self._show_brief_tabs(False)

        # Kaydedilen kod hâlâ başlangıç kodunun kendisiyse (kullanıcı bir
        # şey yazmadan çalıştırmış) o kayda tutunmuyoruz: dili şimdiki dile
        # göre seçiyoruz. Yazılmış bir kod varsa dokunulmuyor.
        saved = self._store.exercise_code(chapter_id, section_id, exercise.id)
        if saved and exercise.is_untouched(saved):
            saved = ""
        self._editor.set_language(exercise.language)
        self._editor.setPlainText(
            saved or exercise.starter_code_for(self._language.language)
        )

        # Tablolar önceki alıştırmanın verisini göstermesin.
        self._tables = []
        self._tables_button.setVisible(exercise.language == "tsql")
        if self._tables_window is not None:
            self._tables_window.set_tables(
                [], self._language.t("tables.not_run")
            )

        self._clear_results()
        self.retranslate()

    def _show_tables(self) -> None:
        """Tablolar penceresini açar; veri yoksa önce anlık görüntü alır."""
        if self._exercise is None:
            return

        if self._tables_window is None:
            self._tables_window = TablesWindow(
                self._language, self, self._mode
            )
        pencere = self._tables_window
        pencere.set_tables(self._tables, "" if self._tables else
                           self._language.t("tables.loading"))
        pencere.show()
        pencere.raise_()
        pencere.activateWindow()

        # Henüz çalıştırılmamışsa hazır verinin hâlini getiriyoruz:
        # sorguyu yazmadan önce "elimde ne var" sorusunun cevabı gerekiyor.
        if not self._tables and (
            self._snapshot is None or not self._snapshot.isRunning()
        ):
            self._snapshot = SnapshotWorker(self._exercise)
            self._snapshot.completed.connect(self._on_snapshot)
            self._snapshot.start()

    def _on_snapshot(self, result) -> None:
        self._tables = result.tables
        if self._tables_window is None:
            return
        if result.tables:
            self._tables_window.set_tables(result.tables)
        else:
            hata = (result.error or {}).get("message", "")
            self._tables_window.set_tables([], hata or self._language.t("tables.empty"))

    def _clear_results(self) -> None:
        while self._results_layout.count() > 2:
            item = self._results_layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
        self._summary.hide()
        self._output.hide()

    # --- çalıştırma -------------------------------------------------------

    def run(self) -> None:
        if self._exercise is not None and self._exercise.is_problem:
            # Ctrl+Enter problemde cevabı denetliyor.
            self._problem.check()
            return
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

        # Ürettiği görsel varsa **kontrollerden önce** geliyor: kullanıcının
        # ilk bakacağı şey çizdiği grafik, "üçüncü kontrol geçti" değil.
        baslik = self._language.t("exercise.produced")
        for yol in result.artifacts:
            self._insert(ArtifactRow(yol, baslik))

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

        # Tablolar penceresi açıksa çalıştırmanın bıraktığı hâli gösteriyor.
        if result.tables:
            self._tables = result.tables
            if self._tables_window is not None:
                self._tables_window.set_tables(result.tables)

        if result.passed and self._exercise is not None:
            self.solved.emit(self._exercise.id)

    def _on_problem_checked(self, answers: list, passed: bool) -> None:
        """Cevap denetlendi: kaydet, gerekiyorsa çözümü aç, çözüldüyse haber ver.

        Çözüm yolları kendiliğinden iki durumda açılıyor: problem çözüldüğünde
        (kişi kendi yolunu başka yollarla karşılaştırsın) ve iki yanlış
        denemeden sonra (takılan kişi nerede ayrıldığını görsün).
        """
        if self._exercise is None:
            return
        self._save_problem_state(solved=passed, count_attempt=True)
        attempts = self._store.attempts(self._chapter_id, self._section_id, self._exercise.id)
        if passed or attempts >= REVEAL_AFTER_ATTEMPTS:
            self._reveal_solutions(True)
        if passed:
            self.solved.emit(self._exercise.id)

    def _save_problem_state(self, solved: bool | None = None, count_attempt: bool = False) -> None:
        """Cevaplar, çalışma alanı ve çözümün açık olup olmadığı tek kayıtta.

        Kod alıştırmasının `code` sütununa JSON olarak yazılıyor; ilerleme ve
        rozet hesabı iki türü ayırt etmiyor.
        """
        if self._exercise is None or not self._exercise.is_problem:
            return
        state = {
            "answers": self._problem.answers(),
            "drawing": self._problem.drawing(),
            "revealed": self._revealed_solution,
        }
        self._store.save_exercise(
            self._chapter_id,
            self._section_id,
            self._exercise.id,
            json.dumps(state, ensure_ascii=False),
            solved=solved,
            count_attempt=count_attempt,
        )

    def _show_brief_tabs(self, visible: bool) -> None:
        self._brief_tabs_holder.setVisible(visible)
        if not visible:
            self._brief_tabs.set_current(BRIEF_PROMPT, notify=False)
            self._brief_stack.setCurrentIndex(BRIEF_PROMPT)

    def _reveal_solutions(self, revealed: bool, save: bool = True, focus: bool = True) -> None:
        """Çözüm yollarını sol panelde açar (ya da kapatır).

        Yeni açıldığında doğrudan çözüm sekmesine geçiliyor; bölüme geri
        dönüşte (`focus=False`) yönerge önde kalıyor.
        """
        was_open = self._revealed_solution
        self._revealed_solution = revealed
        self._problem.set_revealed(revealed)
        self._show_brief_tabs(revealed)
        if revealed:
            self._render_solutions()
            if focus and not was_open:
                self._brief_tabs.set_current(BRIEF_SOLUTIONS, notify=False)
                self._brief_stack.setCurrentIndex(BRIEF_SOLUTIONS)
        if save:
            self._save_problem_state()

    def _render_solutions(self) -> None:
        """Çözüm yolları; birden fazlaysa hepsi, sırayla."""
        if self._exercise is None:
            return
        t = self._language.t
        language = self._language.language

        parts = [
            f"# {t('problem.solutions_title')}",
            t("problem.compare_intro"),
        ]
        solutions = self._exercise.solutions
        for index, solution in enumerate(solutions, start=1):
            title = self._language.pick(solution.get("title"))
            if len(solutions) > 1:
                heading = t("problem.path", number=index, title=title)
            else:
                heading = title or t("problem.solution")
            parts.append(f"## {heading}")
            parts.append(self._exercise.solution_text(index - 1, language))

        self._solutions.set_base_dir(self._exercise.directory)
        self._solutions.show_text("\n\n".join(parts))

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
        self._solutions.set_mode(mode)
        self._problem.set_mode(mode)
        if self._tables_window is not None:
            self._tables_window.set_mode(mode)

    def retranslate(self) -> None:
        self._run_button.setText(self._language.t("exercise.run"))
        self._reset_button.setText(self._language.t("exercise.reset"))
        self._tables_button.setText(self._language.t("tables.button"))
        self._shortcut_hint.setText("Ctrl + Enter")
        if self._tables_window is not None:
            self._tables_window.retranslate()

        # Başlık, etiketler ve ipuçları belgenin içinde olduğu için dil
        # değişince yönergeyi baştan çizmek yeterli.
        self._problem.retranslate()
        self._brief_tabs.set_labels(
            [self._language.t("problem.tab_prompt"), self._language.t("problem.tab_solutions")]
        )
        if self._exercise is not None and self._exercise.is_problem and self._revealed_solution:
            self._render_solutions()
        if self._exercise is not None:
            self._refresh_prompt()
            if not self._exercise.is_problem:
                self._sync_starter_language()

    def _sync_starter_language(self) -> None:
        """Başlangıç kodunun yorum satırlarını şimdiki dile çevirir.

        Yalnızca kullanıcı koda dokunmadıysa yapılıyor. Yazılmış bir kod
        varsa yerinde bırakılıyor: dil değiştirmek kimsenin yazdığını
        silmemeli.
        """
        if self._exercise is None:
            return

        current = self._editor.toPlainText()
        if not self._exercise.is_untouched(current):
            return

        wanted = self._exercise.starter_code_for(self._language.language)
        if wanted.strip() != current.strip():
            self._editor.setPlainText(wanted)


def problem_state(saved: str) -> dict:
    """Kaydedilmiş problem durumu; kayıt yoksa ya da bozuksa boş durum."""
    state = {"answers": [], "drawing": empty_drawing(), "revealed": False}
    if not saved:
        return state
    try:
        value = json.loads(saved)
    except ValueError:
        return state
    if not isinstance(value, dict):
        return state
    state["answers"] = [str(item) for item in value.get("answers", [])]
    state["drawing"] = clean_drawing(value.get("drawing"))
    state["revealed"] = bool(value.get("revealed", False))
    return state
