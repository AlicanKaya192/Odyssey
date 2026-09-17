"""Matematik probleminin sağ tarafı: çalışma alanı, cevap ve denetim.

Alıştırma ekranının sağ tarafı kod alıştırmasında editör; problemde bu
panel. Sol taraf (yönerge ve kademeli ipuçları) iki türde de aynı.

Akış üç adım:

1. **Çalışma kâğıdı.** Kişi adımlarını fareyle **çiziyor** (`DrawPad`);
   klavyede kök, kesir ya da üs yazmak zor ve kısayolları bilinmiyor.
   Soldaki paletten sembol konabiliyor. Çizim puanlanmıyor — serbest bir
   matematik çözümünü yapay zeka olmadan güvenilir biçimde değerlendirmek
   mümkün değil — ama saklanıyor ve çözüm açılınca yanında gösteriliyor.
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
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ..core import problem_check
from ..core.language import LanguageManager
from ..resources.theme.tokens import SPACING
from .draw_pad import ERASER, PEN, DrawPad
from .effects import repolish
from .symbol_palette import SymbolPalette

# Bir alanın yanındaki durum işareti.
MARK_OK = "✓"
MARK_WRONG = "✕"

# Çizim kaydı, kalem durduktan bu kadar sonra yapılıyor; her çizgide
# veritabanına gitmek gereksiz.
WORK_SAVE_DELAY_MS = 700

# Sembol paletinin genişliği: dört sütun düğme ve kaydırma çubuğu.
PALETTE_WIDTH = 190

# Kâğıdın en küçük yüksekliği; sembol paletinin sekiz satırı da bu boya sığıyor.
PAD_MIN_HEIGHT = 340


class ProblemPanel(QWidget):
    """Çalışma alanı, cevap alanları, Kontrol et ve Çözümü göster."""

    # (girilen cevaplar, hepsi doğru mu)
    checked = Signal(list, bool)
    # Çalışma kâğıdı değişti (gecikmeli).
    work_changed = Signal()
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

        header = QHBoxLayout()
        header.setSpacing(SPACING["xs"])
        self._work_title = QLabel()
        self._work_title.setProperty("role", "subtitle")
        header.addWidget(self._work_title)
        header.addStretch(1)
        self._pen_button = self._tool_button(lambda: self._set_tool(PEN))
        self._eraser_button = self._tool_button(lambda: self._set_tool(ERASER))
        self._undo_button = self._tool_button(lambda: self._pad.undo())
        self._clear_button = self._tool_button(lambda: self._pad.clear())
        for button in (self._pen_button, self._eraser_button, self._undo_button, self._clear_button):
            header.addWidget(button)
        outer.addLayout(header)

        work_row = QHBoxLayout()
        work_row.setSpacing(SPACING["md"])

        self._palette = SymbolPalette()
        self._palette.picked.connect(self._on_symbol)
        palette_scroll = QScrollArea()
        palette_scroll.setWidget(self._palette)
        palette_scroll.setWidgetResizable(True)
        palette_scroll.setFrameShape(QFrame.Shape.NoFrame)
        palette_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        palette_scroll.setFixedWidth(PALETTE_WIDTH)
        work_row.addWidget(palette_scroll)

        self._pad = DrawPad()
        # Çözüm açılınca alt tarafa yer veriliyor ama kâğıt yazılamayacak
        # kadar küçülmemeli.
        self._pad.setMinimumHeight(PAD_MIN_HEIGHT)
        self._pad.changed.connect(self._schedule_work_save)
        self._pad.stamp_finished.connect(self._palette.clear_selection)
        work_row.addWidget(self._pad, 1)
        outer.addLayout(work_row, 1)

        self._work_timer = QTimer(self)
        self._work_timer.setSingleShot(True)
        self._work_timer.setInterval(WORK_SAVE_DELAY_MS)
        self._work_timer.timeout.connect(self.work_changed)
        self._set_tool(PEN)

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

    def _tool_button(self, action) -> QPushButton:
        button = QPushButton()
        button.setProperty("variant", "tool")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(action)
        return button

    def _set_tool(self, tool: str, keep_symbol: bool = False) -> None:
        self._pad.set_tool(tool)
        if not keep_symbol:
            self._palette.clear_selection()
        for button, name in ((self._pen_button, PEN), (self._eraser_button, ERASER)):
            button.setProperty("active", "true" if tool == name else "false")
            repolish(button)

    def _on_symbol(self, symbol: str) -> None:
        # Sembol konunca kalemle devam edilir; silgi açıkken sembol seçmek
        # silgiyi bırakıyor.
        self._set_tool(PEN, keep_symbol=True)
        self._pad.arm_stamp(symbol)

    def show_problem(
        self, specs: list[dict], answers: list[str], drawing: dict, symbols: list[str]
    ) -> None:
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

        self._pad.set_drawing(drawing)
        self._palette.set_special(symbols)
        self._set_tool(PEN)
        self._work_timer.stop()

        self._result.hide()
        self.retranslate()

    def answers(self) -> list[str]:
        return [field.text() for field in self._fields]

    def drawing(self) -> dict:
        return self._pad.drawing()

    def ink(self):
        """Çizimin mürekkep rengi; çözüm sayfasına konan görsel aynı renkte."""
        return self._pad.ink()

    def set_mode(self, mode: str) -> None:
        self._pad.set_mode(mode)

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
        t = self._language.t
        self._work_title.setText(t("problem.work_title"))
        self._pad.set_placeholder(t("problem.work_placeholder"))
        self._pen_button.setText(t("problem.pen"))
        self._eraser_button.setText(t("problem.eraser"))
        self._undo_button.setText(t("problem.undo"))
        self._clear_button.setText(t("problem.clear"))
        self._palette.set_labels(t("problem.symbols_special"), t("problem.symbols"))
        self._answer_title.setText(self._language.t("problem.title"))
        self._check_button.setText(self._language.t("problem.check"))
        self._reveal_button.setText(self._language.t("problem.show_solution"))
        for label, field, spec in zip(self._labels, self._fields, self._specs):
            label.setText(self._language.pick(spec.get("label")) or self._language.t("problem.answer"))
            field.setPlaceholderText(self._language.t("problem.placeholder"))
