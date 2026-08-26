"""Kod editörü: satır numarası, Python renklendirmesi ve girinti yardımı.

QScintilla gibi ağır bir bağımlılık eklemek yerine Qt'nin kendi
`QPlainTextEdit`'i üzerine kuruldu. İhtiyacımız olan şeyler sınırlı:
okunabilir bir yazı tipi, satır numarası, temel renklendirme ve Tab'ın
boşluğa dönmesi.
"""

from __future__ import annotations

from PySide6.QtCore import QRect, QSize, Qt, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QKeyEvent,
    QPainter,
    QSyntaxHighlighter,
    QTextCharFormat,
    QTextCursor,
    QTextFormat,
)
from PySide6.QtWidgets import QPlainTextEdit, QTextEdit, QWidget

from ..resources.theme.tokens import FONTS, PALETTES

INDENT = "    "  # Python'da girinti 4 boşluk

KEYWORDS = [
    "and", "as", "assert", "async", "await", "break", "class", "continue",
    "def", "del", "elif", "else", "except", "finally", "for", "from",
    "global", "if", "import", "in", "is", "lambda", "nonlocal", "not", "or",
    "pass", "raise", "return", "try", "while", "with", "yield",
]

CONSTANTS = ["True", "False", "None"]

BUILTINS = [
    "abs", "all", "any", "bool", "dict", "dir", "enumerate", "filter", "float",
    "format", "input", "int", "len", "list", "map", "max", "min", "open",
    "print", "range", "repr", "reversed", "round", "set", "sorted", "str",
    "sum", "tuple", "type", "zip",
]


def _syntax_colors(mode: str) -> dict[str, str]:
    """Renklendirme renkleri. Tema ile uyumlu kalsın diye paletten türetiliyor."""
    if mode == "dark":
        return {
            "keyword": "#C792EA",
            "constant": "#F78C6C",
            "builtin": "#82AAFF",
            "string": "#C3E88D",
            "number": "#F78C6C",
            "comment": "#5F6773",
            "definition": "#FFCB6B",
            "decorator": "#89DDFF",
        }
    return {
        "keyword": "#8B31C7",
        "constant": "#B45309",
        "builtin": "#1D4ED8",
        "string": "#15803D",
        "number": "#B45309",
        "comment": "#8A9099",
        "definition": "#B8860B",
        "decorator": "#0E7490",
    }


class PythonHighlighter(QSyntaxHighlighter):
    """Python sözdizimi renklendirmesi.

    Bilinçli olarak basit tutuldu: anahtar kelimeler, sabitler, hazır
    fonksiyonlar, metinler, sayılar, yorumlar ve tanımlar. Üç tırnaklı
    metinler blok durumu ile takip ediliyor.
    """

    def __init__(self, document, mode: str = "light") -> None:
        super().__init__(document)
        self._rules: list[tuple[object, QTextCharFormat]] = []
        self._string_format = QTextCharFormat()
        self.set_mode(mode)

    def _format(self, color: str, bold: bool = False, italic: bool = False) -> QTextCharFormat:
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold:
            fmt.setFontWeight(QFont.Weight.DemiBold)
        if italic:
            fmt.setFontItalic(True)
        return fmt

    def set_mode(self, mode: str) -> None:
        """Tema değişince renkleri yenile."""
        import re

        colors = _syntax_colors(mode)
        self._rules = []

        keyword_format = self._format(colors["keyword"], bold=True)
        for word in KEYWORDS:
            self._rules.append((re.compile(rf"\b{word}\b"), keyword_format))

        constant_format = self._format(colors["constant"], bold=True)
        for word in CONSTANTS:
            self._rules.append((re.compile(rf"\b{word}\b"), constant_format))

        builtin_format = self._format(colors["builtin"])
        for word in BUILTINS:
            self._rules.append((re.compile(rf"\b{word}\b(?=\s*\()"), builtin_format))

        # def / class sonrası gelen ad
        self._rules.append(
            (re.compile(r"\b(?:def|class)\s+(\w+)"), self._format(colors["definition"], bold=True))
        )
        self._rules.append((re.compile(r"@\w+"), self._format(colors["decorator"])))
        self._rules.append(
            (re.compile(r"\b\d+\.?\d*([eE][+-]?\d+)?\b"), self._format(colors["number"]))
        )

        string_format = self._format(colors["string"])
        self._rules.append((re.compile(r"'[^'\\\n]*(\\.[^'\\\n]*)*'"), string_format))
        self._rules.append((re.compile(r'"[^"\\\n]*(\\.[^"\\\n]*)*"'), string_format))
        self._string_format = string_format

        # Yorum en sona: metin içindeki # işaretinin yorum sanılmaması için
        # önce metinler boyanıyor, yorum kuralı onların üzerine yazmıyor.
        self._rules.append((re.compile(r"#[^\n]*"), self._format(colors["comment"], italic=True)))

        self.rehighlight()

    def highlightBlock(self, text: str) -> None:  # noqa: N802 (Qt adlandırması)
        for pattern, fmt in self._rules:
            for match in pattern.finditer(text):
                # def/class kuralında yalnızca adı boya, anahtar kelimeyi değil.
                start, end = (match.span(1) if match.lastindex else match.span())
                self.setFormat(start, end - start, fmt)

        self._highlight_multiline(text)

    def _highlight_multiline(self, text: str) -> None:
        """Üç tırnaklı metinleri satırlar boyunca takip eder."""
        import re

        delimiters = ('"""', "'''")

        if self.previousBlockState() > 0:
            index = self.previousBlockState() - 1
            delimiter = delimiters[index]
            end = text.find(delimiter)
            if end == -1:
                self.setFormat(0, len(text), self._string_format)
                self.setCurrentBlockState(self.previousBlockState())
                return
            self.setFormat(0, end + 3, self._string_format)
            start_from = end + 3
        else:
            start_from = 0

        for index, delimiter in enumerate(delimiters):
            match = re.search(re.escape(delimiter), text[start_from:])
            if not match:
                continue
            start = start_from + match.start()
            end = text.find(delimiter, start + 3)
            if end == -1:
                self.setFormat(start, len(text) - start, self._string_format)
                self.setCurrentBlockState(index + 1)
            else:
                self.setFormat(start, end - start + 3, self._string_format)
            return


class LineNumberArea(QWidget):
    """Editörün solundaki satır numarası şeridi."""

    def __init__(self, editor: "CodeEditor") -> None:
        super().__init__(editor)
        self._editor = editor

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(self._editor.line_number_width(), 0)

    def paintEvent(self, event) -> None:  # noqa: N802
        self._editor.paint_line_numbers(event)


class CodeEditor(QPlainTextEdit):
    """Alıştırmaların yazıldığı editör."""

    run_requested = Signal()

    def __init__(self, parent: QWidget | None = None, mode: str = "light") -> None:
        super().__init__(parent)
        self._mode = mode
        self._line_area = LineNumberArea(self)
        self._highlighter = PythonHighlighter(self.document(), mode)

        font = QFont()
        font.setFamily(FONTS["mono"].split(",")[0].strip().strip('"'))
        font.setPointSize(11)
        font.setFixedPitch(True)
        self.setFont(font)

        self.setTabStopDistance(QFontMetrics(font).horizontalAdvance(" ") * 4)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setProperty("role", "code")

        self.blockCountChanged.connect(self._update_margin)
        self.updateRequest.connect(self._update_line_area)
        self.cursorPositionChanged.connect(self._highlight_current_line)

        self._update_margin()
        self._highlight_current_line()

    # --- satır numarası ---------------------------------------------------

    def line_number_width(self) -> int:
        digits = max(2, len(str(max(1, self.blockCount()))))
        return 16 + self.fontMetrics().horizontalAdvance("9") * digits

    def _update_margin(self) -> None:
        self.setViewportMargins(self.line_number_width(), 0, 0, 0)

    def _update_line_area(self, rect: QRect, dy: int) -> None:
        if dy:
            self._line_area.scroll(0, dy)
        else:
            self._line_area.update(0, rect.y(), self._line_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self._update_margin()

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        area = self.contentsRect()
        self._line_area.setGeometry(
            QRect(area.left(), area.top(), self.line_number_width(), area.height())
        )

    def paint_line_numbers(self, event) -> None:
        palette = PALETTES.get(self._mode, PALETTES["light"])
        painter = QPainter(self._line_area)
        painter.fillRect(event.rect(), QColor(palette["code_bg"]))

        block = self.firstVisibleBlock()
        number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        current = self.textCursor().blockNumber()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(
                    QColor(palette["text"] if number == current else palette["text_muted"])
                )
                painter.drawText(
                    0,
                    int(top),
                    self._line_area.width() - 8,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    str(number + 1),
                )
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            number += 1

    def _highlight_current_line(self) -> None:
        palette = PALETTES.get(self._mode, PALETTES["light"])
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QColor(palette["surface_hover"]))
        selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        self.setExtraSelections([selection])

    # --- düzenleme kolaylıkları -------------------------------------------

    def set_mode(self, mode: str) -> None:
        """Tema değişince renklendirmeyi ve satır vurgusunu yenile."""
        self._mode = mode
        self._highlighter.set_mode(mode)
        self._highlight_current_line()
        self._line_area.update()

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        key = event.key()
        modifiers = event.modifiers()

        # Ctrl+Enter kodu çalıştırır.
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and modifiers & Qt.KeyboardModifier.ControlModifier:
            self.run_requested.emit()
            return

        # Tab girinti ekler, Shift+Tab geri alır.
        if key == Qt.Key.Key_Tab and not modifiers:
            self.insertPlainText(INDENT)
            return

        if key == Qt.Key.Key_Backtab:
            self._dedent()
            return

        # Enter'da bir önceki satırın girintisini koru, ':' sonrası artır.
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            cursor = self.textCursor()
            line = cursor.block().text()
            indent = line[: len(line) - len(line.lstrip())]
            if line.rstrip().endswith(":"):
                indent += INDENT
            super().keyPressEvent(event)
            self.insertPlainText(indent)
            return

        super().keyPressEvent(event)

    def _dedent(self) -> None:
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        cursor.movePosition(
            QTextCursor.MoveOperation.Right,
            QTextCursor.MoveMode.KeepAnchor,
            len(INDENT),
        )
        if cursor.selectedText() == INDENT:
            cursor.removeSelectedText()
