"""Matematik probleminin sağ tarafı: çalışma alanı, cevap ve denetim.

Alıştırma ekranının sağ tarafı kod alıştırmasında editör; problemde bu
panel. Sol taraf (yönerge ve kademeli ipuçları) iki türde de aynı.

Akış üç adım:

1. **Çalışma alanı.** Kişi adımlarını buraya yazıyor. Puanlanmıyor —
   serbest yazılmış bir matematik çözümünü yapay zeka olmadan güvenilir
   biçimde değerlendirmek mümkün değil — ama saklanıyor ve çözüm açılınca
   yanında gösteriliyor.
2. **Cevap.** Yalnızca sonuç denetleniyor (`core/problem_check.py`), alan
   alan: iki bilinmeyenli bir problemde hangisinin yanlış olduğunu söylemek
   "yanlış" deyip bırakmaktan daha öğretici.
3. **Çözüm yolları.** Panel yalnızca istek sinyali yayıyor; açma kararı ve
   çözümün çizimi `ExerciseView`'da.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core import problem_check
from ..core.language import LanguageManager
from ..resources.theme.tokens import SPACING
from .effects import repolish

# Bir alanın yanındaki durum işareti.
MARK_OK = "✓"
MARK_WRONG = "✕"

# Çalışma alanı yazılırken kayıt, yazma durduktan bu kadar sonra yapılıyor;
# her tuşta veritabanına gitmek gereksiz.
WORK_SAVE_DELAY_MS = 700


class ProblemPanel(QWidget):
    """Çalışma alanı, cevap alanları, Kontrol et ve Çözümü göster."""

    # (girilen cevaplar, hepsi doğru mu)
    checked = Signal(list, bool)
    # Çalışma alanının metni değişti (gecikmeli).
    work_changed = Signal(str)
    reveal_requested = Signal()

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._specs: list[dict] = []
        self._fields: list[QLineEdit] = []
        self._labels: list[QLabel] = []
        self._marks: list[QLabel] = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(SPACING["xl"], SPACING["lg"], SPACING["xl"], SPACING["lg"])
        outer.setSpacing(SPACING["sm"])

        self._work_title = QLabel()
        self._work_title.setProperty("role", "subtitle")
        outer.addWidget(self._work_title)

        self._work = QPlainTextEdit()
        self._work.setMinimumHeight(110)
        self._work.textChanged.connect(self._schedule_work_save)
        outer.addWidget(self._work, 1)

        self._work_timer = QTimer(self)
        self._work_timer.setSingleShot(True)
        self._work_timer.setInterval(WORK_SAVE_DELAY_MS)
        self._work_timer.timeout.connect(
            lambda: self.work_changed.emit(self._work.toPlainText())
        )

        outer.addSpacing(SPACING["sm"])
        self._answer_title = QLabel()
        self._answer_title.setProperty("role", "subtitle")
        outer.addWidget(self._answer_title)

        card = QFrame()
        card.setProperty("surface", "card")
        self._grid = QGridLayout(card)
        self._grid.setContentsMargins(SPACING["md"], SPACING["md"], SPACING["md"], SPACING["md"])
        self._grid.setHorizontalSpacing(SPACING["md"])
        self._grid.setVerticalSpacing(SPACING["sm"])
        self._grid.setColumnStretch(1, 1)
        outer.addWidget(card)

        buttons = QHBoxLayout()
        buttons.setSpacing(SPACING["sm"])
        self._check_button = QPushButton()
        self._check_button.setProperty("variant", "primary")
        self._check_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._check_button.clicked.connect(self.check)
        buttons.addWidget(self._check_button)

        self._reveal_button = QPushButton()
        self._reveal_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._reveal_button.clicked.connect(self.reveal_requested)
        buttons.addWidget(self._reveal_button)
        buttons.addStretch(1)
        outer.addLayout(buttons)

        self._result = QLabel()
        self._result.setWordWrap(True)
        self._result.setProperty("role", "subtitle")
        self._result.hide()
        outer.addWidget(self._result)

        self.retranslate()

    # --- içerik -----------------------------------------------------------

    def show_problem(self, specs: list[dict], answers: list[str], work: str) -> None:
        """Alanları kurar ve daha önce yazılanları geri koyar."""
        while self._grid.count():
            item = self._grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._specs = specs
        self._fields, self._labels, self._marks = [], [], []

        for row, spec in enumerate(specs):
            label = QLabel()
            field = QLineEdit()
            field.setText(answers[row] if row < len(answers) else "")
            field.returnPressed.connect(self.check)
            field.textEdited.connect(lambda _=None, r=row: self._clear_mark(r))
            mark = QLabel()
            mark.setFixedWidth(22)
            self._grid.addWidget(label, row, 0)
            self._grid.addWidget(field, row, 1)
            self._grid.addWidget(mark, row, 2)
            self._labels.append(label)
            self._fields.append(field)
            self._marks.append(mark)

        # Geri yüklenen metin bir "değişiklik" sayılıp kayda gitmesin.
        self._work.blockSignals(True)
        self._work.setPlainText(work)
        self._work.blockSignals(False)
        self._work_timer.stop()

        self._result.hide()
        self.retranslate()

    def answers(self) -> list[str]:
        return [field.text() for field in self._fields]

    def work(self) -> str:
        return self._work.toPlainText()

    # --- denetim ----------------------------------------------------------

    def check(self) -> None:
        if not self._specs:
            return
        answers = self.answers()

        if not any(answer.strip() for answer in answers):
            self._show_result(self._language.t("problem.empty"), "warning")
            return

        unreadable = any(
            answer.strip() and not problem_check.is_readable(spec, answer)
            for spec, answer in zip(self._specs, answers)
        )
        if unreadable:
            # Okunamayan cevap bir deneme sayılmıyor: "üç" yazan kişi yanlış
            # cevap vermedi, yazım biçimini tutturamadı.
            self._show_result(self._language.t("problem.unreadable"), "warning")
            return

        results = problem_check.check_all(self._specs, answers)
        for index, ok in enumerate(results):
            self._set_mark(index, ok)

        passed = all(results)
        if passed:
            self._show_result(self._language.t("problem.correct"), "success")
        elif len(results) > 1:
            self._show_result(
                self._language.t("problem.partly", right=sum(results), total=len(results)),
                "danger",
            )
        else:
            self._show_result(self._language.t("problem.wrong"), "danger")

        self.checked.emit(answers, passed)

    def _schedule_work_save(self) -> None:
        self._work_timer.start()

    def _set_mark(self, index: int, ok: bool) -> None:
        mark = self._marks[index]
        mark.setText(MARK_OK if ok else MARK_WRONG)
        mark.setProperty("tone", "success" if ok else "danger")
        repolish(mark)

    def _clear_mark(self, index: int) -> None:
        """Cevap değişince eski işaret yanıltmasın."""
        if index < len(self._marks):
            self._marks[index].setText("")

    def _show_result(self, text: str, tone: str) -> None:
        self._result.setText(text)
        self._result.setProperty("tone", tone)
        repolish(self._result)
        self._result.show()

    def set_revealed(self, revealed: bool) -> None:
        """Çözüm açıkken "Çözümü göster" düğmesi gereksiz."""
        self._reveal_button.setVisible(not revealed)

    # --- dil --------------------------------------------------------------

    def retranslate(self) -> None:
        self._work_title.setText(self._language.t("problem.work_title"))
        self._work.setPlaceholderText(self._language.t("problem.work_placeholder"))
        self._answer_title.setText(self._language.t("problem.title"))
        self._check_button.setText(self._language.t("problem.check"))
        self._reveal_button.setText(self._language.t("problem.show_solution"))
        for label, field, spec in zip(self._labels, self._fields, self._specs):
            label.setText(self._language.pick(spec.get("label")) or self._language.t("problem.answer"))
            field.setPlaceholderText(self._language.t("problem.placeholder"))
