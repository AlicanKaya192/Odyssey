"""Not editörü: düz markdown yazılıyor, kod blokları kod gibi görünüyor.

`QTextEdit` üzerine kurulu, `CodeEditor` ile aynı sebepten: `QPlainTextEdit`
satır aralığını hiç desteklemiyor.

Editör zengin metin editörü değil. Kaydedilen şey düz markdown; araç
çubuğundaki düğmeler yalnızca işaretleri yerine koyuyor (`## `, `**`,
`- `, üç ters tırnaklı kod bloğu). Böylece dışa aktarılan bir not başka
bir editörde de aynı okunuyor.

Renklendirme: başlık satırı kalın, liste işareti vurgu renginde,
`**kalın**` kalın, satır içi kod ve kod blokları eş aralıklı yazı tipinde.
Python bloklarının içi alıştırma editörüyle aynı kurallarla boyanıyor
(`code_editor.python_rules`).
"""

from __future__ import annotations

import re

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QKeyEvent,
    QPainter,
    QSyntaxHighlighter,
    QTextBlockFormat,
    QTextCharFormat,
    QTextCursor,
)
from PySide6.QtWidgets import QTextEdit, QWidget

from ..resources.theme.tokens import FONTS, PALETTES
from .code_editor import python_rules

# Satır aralığı. Kod editöründen biraz dar: burada çoğunlukla düz yazı var.
LINE_HEIGHT_PERCENT = 150

INDENT = "    "
FENCE = "```"
MONO_FAMILY = FONTS["mono"].split(",")[0].strip().strip('"')

# Satırın hangi bölgede olduğu; QSyntaxHighlighter'ın blok durumu.
STATE_TEXT = 0
STATE_PYTHON = 1
STATE_CODE = 2  # Python dışında bir dil ya da dil yazılmamış
PYTHON_TAGS = ("python", "py")

HEADING = re.compile(r"^#{1,6}\s")
HEADING_MARKS = re.compile(r"^#{1,6}\s*")
LIST_MARK = re.compile(r"^(\s*)([-*]|\d+\.)\s")
BULLET = re.compile(r"^(\s*)[-*]\s")
BOLD = re.compile(r"\*\*[^*\n]+\*\*")
INLINE_CODE = re.compile(r"`[^`\n]+`")
QUOTE = re.compile(r"^>\s?")


class NoteHighlighter(QSyntaxHighlighter):
    """Markdown'ın göze çarpması gereken parçaları ve kod blokları."""

    def __init__(self, document, mode: str = "light") -> None:
        super().__init__(document)
        self.set_mode(mode)

    def set_mode(self, mode: str) -> None:
        palette = PALETTES.get(mode, PALETTES["light"])
        self._rules, _ = python_rules(mode)

        self._code = QTextCharFormat()
        self._code.setFontFamilies([MONO_FAMILY])

        self._fence = QTextCharFormat(self._code)
        self._fence.setForeground(QColor(palette["text_muted"]))

        self._heading = QTextCharFormat()
        self._heading.setFontWeight(QFont.Weight.Bold)

        self._mark = QTextCharFormat()
        self._mark.setForeground(QColor(palette["accent"]))
        self._mark.setFontWeight(QFont.Weight.Bold)

        self._bold = QTextCharFormat()
        self._bold.setFontWeight(QFont.Weight.Bold)

        self._inline = QTextCharFormat(self._code)
        self._inline.setForeground(QColor(palette["accent"]))

        self._quote = QTextCharFormat()
        self._quote.setForeground(QColor(palette["text_muted"]))
        self._quote.setFontItalic(True)

        self.rehighlight()

    def highlightBlock(self, text: str) -> None:  # noqa: N802 (Qt adlandırması)
        previous = self.previousBlockState()
        in_code = previous in (STATE_PYTHON, STATE_CODE)
        stripped = text.strip()

        # Kod bloğunun açılış ya da kapanış çizgisi.
        if stripped.startswith(FENCE):
            self.setFormat(0, len(text), self._fence)
            if in_code:
                self.setCurrentBlockState(STATE_TEXT)
            else:
                tag = stripped[len(FENCE):].strip().lower()
                self.setCurrentBlockState(STATE_PYTHON if tag in PYTHON_TAGS else STATE_CODE)
            return

        if in_code:
            self.setCurrentBlockState(previous)
            self.setFormat(0, len(text), self._code)
            if previous == STATE_PYTHON:
                for pattern, fmt, group in self._rules:
                    for match in pattern.finditer(text):
                        start, end = match.span(group) if group else match.span()
                        if start >= 0:
                            merged = QTextCharFormat(self._code)
                            merged.merge(fmt)
                            self.setFormat(start, end - start, merged)
            return

        self.setCurrentBlockState(STATE_TEXT)

        if HEADING.match(text):
            self.setFormat(0, len(text), self._heading)
            return
        if QUOTE.match(text):
            self.setFormat(0, len(text), self._quote)

        mark = LIST_MARK.match(text)
        if mark:
            self.setFormat(mark.start(2), len(mark.group(2)), self._mark)
        for match in BOLD.finditer(text):
            self.setFormat(match.start(), match.end() - match.start(), self._bold)
        for match in INLINE_CODE.finditer(text):
            self.setFormat(match.start(), match.end() - match.start(), self._inline)


class NoteEditor(QTextEdit):
    """Notun yazıldığı alan."""

    def __init__(self, parent: QWidget | None = None, mode: str = "light") -> None:
        super().__init__(parent)
        self._spacing_queued = False
        self._mode = mode
        self._placeholder = ""
        self._was_empty = True

        self.setAcceptRichText(False)
        self.setProperty("role", "note-editor")
        self._highlighter = NoteHighlighter(self.document(), mode)
        self.setTabStopDistance(QFontMetrics(self.font()).horizontalAdvance(" ") * 4)

        self.document().blockCountChanged.connect(self._schedule_line_spacing)
        self.textChanged.connect(self._on_emptiness_changed)
        self._apply_line_spacing()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._highlighter.set_mode(mode)
        self.viewport().update()

    # --- yer tutucu -------------------------------------------------------

    def setPlaceholderText(self, text: str) -> None:  # noqa: N802
        """Yer tutucuyu Qt'ye değil kendimize çizdiriyoruz.

        Qt, `QTextEdit`'in yer tutucusunu ilk (boş) satırın yüksekliğine
        kırpıyor. Satır aralığı %150 olunca sarılan ikinci satır yarıya
        kadar görünüp kesiliyordu — bölümdeki not panelinde, dar sütunda
        görüldü (Alican bildirdi). Burada editörün tamamına sarılarak
        çiziliyor.
        """
        self._placeholder = text
        self.viewport().update()

    def placeholderText(self) -> str:  # noqa: N802
        return self._placeholder

    def _on_emptiness_changed(self) -> None:
        # Boş ↔ dolu geçişinde alanın tamamı yeniden çiziliyor. Qt yalnızca
        # değişen satırı çizdiği için ilk harfte yer tutucunun alt satırları
        # ekranda kalıyordu.
        bos = self.document().isEmpty()
        if bos != self._was_empty:
            self._was_empty = bos
            self.viewport().update()

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        if not self._placeholder or not self.document().isEmpty():
            return
        painter = QPainter(self.viewport())
        painter.setPen(QColor(PALETTES.get(self._mode, PALETTES["light"])["text_muted"]))
        # Belgenin yazı tipi: stil dosyasının verdiği boyut orada. Widget'ın
        # kendi yazı tipiyle çizilince yazılan metinden küçük duruyordu.
        painter.setFont(self.document().defaultFont())
        margin = int(self.document().documentMargin())
        alan = self.viewport().rect().adjusted(margin, margin, -margin, -margin)
        painter.drawText(
            alan,
            int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop | Qt.TextFlag.TextWordWrap),
            self._placeholder,
        )
        painter.end()

    # --- satır aralığı ----------------------------------------------------

    def _schedule_line_spacing(self) -> None:
        """Belge kendi değişim sinyalinin içinden değiştirilmiyor.

        `CodeEditor`'da yaşandı: biçim `textChanged` içinde uygulanınca
        Qt'nin sürdürdüğü düzenleme bozuluyor ve boş satırda Enter
        yutuluyordu. Biçim olay bittikten sonra uygulanıyor.
        """
        if self._spacing_queued:
            return
        self._spacing_queued = True
        QTimer.singleShot(0, self._apply_line_spacing)

    def _apply_line_spacing(self) -> None:
        self._spacing_queued = False
        target = QTextBlockFormat.LineHeightTypes.ProportionalHeight.value

        block = self.document().begin()
        while block.isValid():
            fmt = block.blockFormat()
            if (
                int(fmt.lineHeightType()) != target
                or int(fmt.lineHeight()) != LINE_HEIGHT_PERCENT
            ):
                cursor = QTextCursor(block)
                new_fmt = QTextBlockFormat()
                new_fmt.setLineHeight(LINE_HEIGHT_PERCENT, target)
                cursor.mergeBlockFormat(new_fmt)
            block = block.next()

    def setPlainText(self, text: str) -> None:  # noqa: N802
        """Metni yükler; önceki notun geri alma geçmişi taşınmıyor."""
        super().setPlainText(text)
        self._apply_line_spacing()
        self.document().clearUndoRedoStacks()

    # --- tuşlar -----------------------------------------------------------

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        key = event.key()
        mods = event.modifiers()
        ctrl = bool(mods & Qt.KeyboardModifier.ControlModifier)

        if key == Qt.Key.Key_Tab and not ctrl and not mods & Qt.KeyboardModifier.AltModifier:
            self.textCursor().insertText(INDENT)
            return
        if ctrl and key == Qt.Key.Key_B:
            self.toggle_bold()
            return
        # Enter Qt'ye hiç bırakılmıyor, satır sonu elle ekleniyor. Qt'nin
        # kendi Enter'ı, satır aralığı verilmiş boş bir satırda yutuluyordu
        # (ölçüldü: üç Enter, iki satır) — `CodeEditor` de aynı yüzden
        # kendisi ekliyor. Shift+Enter de düz satır sonu; Qt'nin yumuşak
        # satır sonu (U+2028) markdown'da bir anlam taşımıyor.
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if mods & Qt.KeyboardModifier.ShiftModifier or not self._continue_line():
                self.insertPlainText("\n")
            return
        super().keyPressEvent(event)

    def _in_code_block(self, block) -> bool:
        if block.text().strip().startswith(FENCE):
            return False
        return block.previous().userState() in (STATE_PYTHON, STATE_CODE)

    def _continue_line(self) -> bool:
        """Enter: kodda girintiyi, listede işareti sürdürür.

        Kendi başına bir şey yapmadıysa `False` döndürüyor ve tuş Qt'nin
        olağan yoluna gidiyor.
        """
        cursor = self.textCursor()
        if cursor.hasSelection():
            return False

        block = cursor.block()
        line = block.text()
        column = cursor.positionInBlock()
        before = line[:column]

        if self._in_code_block(block):
            indent = re.match(r"\s*", before).group()
            if before.rstrip().endswith(":"):
                indent += INDENT
            cursor.insertText("\n" + indent)
            self.setTextCursor(cursor)
            return True

        mark = LIST_MARK.match(line)
        if mark is None or column < mark.end():
            return False

        if not line[mark.end():].strip():
            # Boş madde: liste bitiyor, işaret siliniyor.
            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
            cursor.movePosition(
                QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor
            )
            cursor.removeSelectedText()
            self.setTextCursor(cursor)
            return True

        marker = mark.group(2)
        if marker.endswith("."):
            marker = f"{int(marker[:-1]) + 1}."
        cursor.insertText(f"\n{mark.group(1)}{marker} ")
        self.setTextCursor(cursor)
        return True

    # --- araç çubuğu ------------------------------------------------------

    def toggle_heading(self) -> None:
        """Satırı başlık yapar ya da başlıktan çıkarır (`## `)."""
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        marks = HEADING_MARKS.match(cursor.block().text())
        if marks:
            cursor.movePosition(
                QTextCursor.MoveOperation.Right,
                QTextCursor.MoveMode.KeepAnchor,
                len(marks.group()),
            )
            cursor.removeSelectedText()
        else:
            cursor.insertText("## ")
        cursor.endEditBlock()
        self.setFocus()

    def toggle_bold(self) -> None:
        """Seçimi `**` ile sarar; seçim yoksa imleci iki işaretin arasına koyar."""
        cursor = self.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText().replace(" ", "\n")
            if len(text) >= 4 and text.startswith("**") and text.endswith("**"):
                cursor.insertText(text[2:-2])
            else:
                cursor.insertText(f"**{text}**")
        else:
            cursor.insertText("****")
            cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.MoveAnchor, 2)
            self.setTextCursor(cursor)
        self.setFocus()

    def toggle_list(self) -> None:
        """Seçili satırları madde yapar; hepsi zaten maddeyse işareti kaldırır."""
        cursor = self.textCursor()
        document = self.document()
        first = document.findBlock(cursor.selectionStart())
        last = document.findBlock(cursor.selectionEnd())

        blocks = []
        block = first
        while block.isValid():
            blocks.append(block)
            if block == last:
                break
            block = block.next()

        dolu = [b for b in blocks if b.text().strip()]
        hepsi_madde = bool(dolu) and all(BULLET.match(b.text()) for b in dolu)

        cursor.beginEditBlock()
        for block in blocks:
            text = block.text()
            edit = QTextCursor(block)
            if hepsi_madde:
                mark = BULLET.match(text)
                if mark:
                    edit.setPosition(block.position() + len(mark.group(1)))
                    edit.setPosition(block.position() + mark.end(), QTextCursor.MoveMode.KeepAnchor)
                    edit.removeSelectedText()
            elif (text.strip() or len(blocks) == 1) and not BULLET.match(text):
                edit.insertText("- ")
        cursor.endEditBlock()
        self.setFocus()

    def insert_code(self, language: str) -> None:
        """Kod bloğu ekler. Seçim varsa onu bloğun içine alır.

        Açılış çizgisi her zaman kendi satırında başlıyor: satırın ortasına
        yazılan ```` ``` ```` markdown'da kod bloğu açmıyor.
        """
        cursor = self.textCursor()
        selected = cursor.selectedText().replace(" ", "\n") if cursor.hasSelection() else ""

        cursor.beginEditBlock()
        if cursor.hasSelection():
            cursor.removeSelectedText()
        before = "" if cursor.positionInBlock() == 0 else "\n"
        cursor.insertText(f"{before}{FENCE}{language}\n{selected}")
        caret = cursor.position()
        rest = cursor.block().text()[cursor.positionInBlock():]
        cursor.insertText(f"\n{FENCE}" + ("\n" if rest else ""))
        cursor.endEditBlock()

        cursor.setPosition(caret)
        self.setTextCursor(cursor)
        self.setFocus()
