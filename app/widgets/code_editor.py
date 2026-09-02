"""Kod editörü: satır numarası, Python renklendirmesi ve girinti yardımı.

`QTextEdit` üzerine kurulu. `QPlainTextEdit` daha hafif olurdu ama satır
aralığını hiç desteklemiyor — `setLineHeight` de blok kenar boşluğu da
sessizce yok sayılıyor ve satırlar iç içe görünüyor. Bizim dosyalarımız
birkaç yüz satırı geçmeyeceği için `QTextEdit`'in ek maliyeti önemsiz.

Renkler ders metinlerindeki kod bloklarıyla aynı sözlükten geliyor; editörde
turuncu olan anlatımda da turuncu.
"""

from __future__ import annotations

import re

from PySide6.QtCore import QRect, QSize, Qt, QTimer, Signal
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
    QTextFormat,
)
from PySide6.QtWidgets import QTextEdit, QWidget

from ..resources.theme.tokens import FONTS, PALETTES, SYNTAX

INDENT = "    "  # Python'da girinti 4 boşluk

# Satır aralığı. Varsayılan (%100) kodda satırları iç içe gösteriyor.
LINE_HEIGHT_PERCENT = 165

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


class PythonHighlighter(QSyntaxHighlighter):
    """Python sözdizimi renklendirmesi.

    Bilinçli olarak basit tutuldu: anahtar kelimeler, sabitler, hazır
    fonksiyonlar, atanan değişken adları, metinler, sayılar, yorumlar ve
    tanımlar.
    """

    def __init__(self, document, mode: str = "light") -> None:
        super().__init__(document)
        self._rules: list[tuple[object, QTextCharFormat, int]] = []
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
        colors = SYNTAX.get(mode, SYNTAX["light"])
        self._rules = []

        keyword_format = self._format(colors["keyword"], bold=True)
        for word in KEYWORDS:
            self._rules.append((re.compile(rf"\b{word}\b"), keyword_format, 0))

        constant_format = self._format(colors["constant"], bold=True)
        for word in CONSTANTS:
            self._rules.append((re.compile(rf"\b{word}\b"), constant_format, 0))

        builtin_format = self._format(colors["builtin"])
        for word in BUILTINS:
            self._rules.append((re.compile(rf"\b{word}\b(?=\s*\()"), builtin_format, 0))

        # Değer atanan değişken adı: `isim = ...` ve `toplam += ...`
        self._rules.append(
            (
                re.compile(r"\b([A-Za-z_]\w*)\s*(?:[+\-*/%]?=)(?!=)"),
                self._format(colors["variable"]),
                1,
            )
        )

        self._rules.append(
            (re.compile(r"\b(?:def|class)\s+(\w+)"), self._format(colors["definition"], bold=True), 1)
        )
        self._rules.append((re.compile(r"@\w+"), self._format(colors["decorator"]), 0))
        self._rules.append(
            (re.compile(r"\b\d+\.?\d*(?:[eE][+-]?\d+)?\b"), self._format(colors["number"]), 0)
        )

        string_format = self._format(colors["string"])
        self._rules.append((re.compile(r"'[^'\\\n]*(?:\\.[^'\\\n]*)*'"), string_format, 0))
        self._rules.append((re.compile(r'"[^"\\\n]*(?:\\.[^"\\\n]*)*"'), string_format, 0))
        self._string_format = string_format

        # Yorum en sona: metinler önce boyanıyor, yorum kuralı üzerine yazmıyor.
        self._rules.append(
            (re.compile(r"#[^\n]*"), self._format(colors["comment"], italic=True), 0)
        )

        self.rehighlight()

    def highlightBlock(self, text: str) -> None:  # noqa: N802 (Qt adlandırması)
        for pattern, fmt, group in self._rules:
            for match in pattern.finditer(text):
                start, end = match.span(group) if group else match.span()
                if start >= 0:
                    self.setFormat(start, end - start, fmt)

        self._highlight_multiline(text)

    def _highlight_multiline(self, text: str) -> None:
        """Üç tırnaklı metinleri satırlar boyunca takip eder."""
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
            found = text.find(delimiter, start_from)
            if found == -1:
                continue
            end = text.find(delimiter, found + 3)
            if end == -1:
                self.setFormat(found, len(text) - found, self._string_format)
                self.setCurrentBlockState(index + 1)
            else:
                self.setFormat(found, end - found + 3, self._string_format)
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


class CodeEditor(QTextEdit):
    """Alıştırmaların yazıldığı editör."""

    run_requested = Signal()

    def __init__(self, parent: QWidget | None = None, mode: str = "light") -> None:
        super().__init__(parent)
        self._mode = mode
        self._spacing_queued = False
        self._line_area = LineNumberArea(self)
        self._highlighter = PythonHighlighter(self.document(), mode)

        font = QFont()
        font.setFamily(FONTS["mono"].split(",")[0].strip().strip('"'))
        font.setPointSize(11)
        font.setFixedPitch(True)
        self.setFont(font)

        self.setTabStopDistance(QFontMetrics(font).horizontalAdvance(" ") * 4)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.setAcceptRichText(False)
        self.setProperty("role", "code")

        self.document().blockCountChanged.connect(self._on_blocks_changed)
        self.verticalScrollBar().valueChanged.connect(self._line_area.update)
        self.textChanged.connect(self._on_text_changed)
        self.cursorPositionChanged.connect(self._highlight_current_line)

        self._update_margin()
        self._apply_line_spacing()
        self._highlight_current_line()

    # --- satır aralığı ----------------------------------------------------

    def _schedule_line_spacing(self) -> None:
        """Satır aralığını olay bittikten **sonra** uygulanmak üzere sıraya alır.

        **Belge, kendi değişim sinyalinin içinden değiştirilmiyor.** Eskiden
        `textChanged` gelir gelmez blok biçimi uygulanıyordu ve bu, Qt'nin o
        an sürdürdüğü düzenlemeyi bozuyordu: boş bir satırdayken Enter'a
        basmak hiçbir şey yapmıyor, satır arası boşluk bırakılamıyordu
        (ölçüldü: üç Enter, sıfır yeni satır). Biçim artık olay
        tamamlandıktan sonra uygulanıyor.
        """
        if self._spacing_queued:
            return
        self._spacing_queued = True
        QTimer.singleShot(0, self._apply_line_spacing)

    def _apply_line_spacing(self) -> None:
        """Satır aralığını açar.

        `QPlainTextEdit` bu ayarı yok sayıyordu; `QTextEdit` uyguluyor.
        Yeni satırlar da aralığı alsın diye satır sayısı değiştikçe tekrar
        uygulanıyor — her tuş vuruşunda değil, yalnızca satır eklenip
        silindiğinde.
        """
        self._spacing_queued = False

        cursor = self.textCursor()
        position = cursor.position()

        block_format = QTextBlockFormat()
        block_format.setLineHeight(
            LINE_HEIGHT_PERCENT,
            QTextBlockFormat.LineHeightTypes.ProportionalHeight.value,
        )

        # Biçim ayrı bir imleçle uygulanıyor; kullanıcının imleci ve seçimi
        # yerinde kalıyor.
        bicimleyici = QTextCursor(self.document())
        bicimleyici.select(QTextCursor.SelectionType.Document)
        bicimleyici.mergeBlockFormat(block_format)

        if cursor.position() != position:
            cursor.setPosition(min(position, len(self.toPlainText())))
            self.setTextCursor(cursor)

    def setPlainText(self, text: str) -> None:  # noqa: N802
        """Metni yükler ve satır aralığını yeniden uygular.

        Satır sayısı değişmeyen bir yükleme `blockCountChanged` yaymıyor;
        aralık o durumda uygulanmadan kalıyordu.
        """
        super().setPlainText(text)
        self._schedule_line_spacing()

    def _on_text_changed(self) -> None:
        self._line_area.update()

    def _on_blocks_changed(self, _count: int) -> None:
        self._update_margin()
        self._line_area.update()
        self._schedule_line_spacing()

    # --- satır numarası ---------------------------------------------------

    def line_number_width(self) -> int:
        digits = max(2, len(str(max(1, self.document().blockCount()))))
        return 20 + self.fontMetrics().horizontalAdvance("9") * digits

    def _update_margin(self) -> None:
        self.setViewportMargins(self.line_number_width(), 0, 0, 0)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        area = self.contentsRect()
        self._line_area.setGeometry(
            QRect(area.left(), area.top(), self.line_number_width(), area.height())
        )

    def paint_line_numbers(self, event) -> None:
        """Satır numaralarını çizer.

        `QTextEdit`'te `firstVisibleBlock()` yok; blokların yerleri belge
        düzeninden okunup kaydırma miktarı çıkarılıyor.
        """
        palette = PALETTES.get(self._mode, PALETTES["light"])
        painter = QPainter(self._line_area)
        painter.fillRect(event.rect(), QColor(palette["code_bg"]))

        document = self.document()
        layout = document.documentLayout()
        offset = self.verticalScrollBar().value()
        current = self.textCursor().blockNumber()

        block = document.begin()
        while block.isValid():
            rect = layout.blockBoundingRect(block)
            top = rect.top() - offset

            if top > event.rect().bottom():
                break

            if top + rect.height() >= event.rect().top() and block.isVisible():
                painter.setPen(
                    QColor(
                        palette["text"]
                        if block.blockNumber() == current
                        else palette["text_muted"]
                    )
                )
                painter.drawText(
                    0,
                    int(top),
                    self._line_area.width() - 10,
                    int(rect.height()),
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                    str(block.blockNumber() + 1),
                )

            block = block.next()

    def _highlight_current_line(self) -> None:
        palette = PALETTES.get(self._mode, PALETTES["light"])
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QColor(palette["surface_hover"]))
        selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        self.setExtraSelections([selection])
        self._line_area.update()

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
