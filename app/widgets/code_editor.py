"""Kod editörü: satır numarası, renklendirme ve yazma kolaylıkları.

`QTextEdit` üzerine kurulu. `QPlainTextEdit` daha hafif olurdu ama satır
aralığını hiç desteklemiyor — `setLineHeight` de blok kenar boşluğu da
sessizce yok sayılıyor ve satırlar iç içe görünüyor. Bizim dosyalarımız
birkaç yüz satırı geçmeyeceği için `QTextEdit`'in ek maliyeti önemsiz.

Renkler ders metinlerindeki kod bloklarıyla aynı sözlükten geliyor; editörde
turuncu olan anlatımda da turuncu.

Aynı editör Python ve SQL (T-SQL) alıştırmalarında kullanılıyor;
`set_language` renklendirmeyi ve yorum işaretini değiştiriyor.
"""

from __future__ import annotations

import re

from PySide6.QtCore import QRect, QSize, Qt, QTimer, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QFontMetricsF,
    QKeyEvent,
    QPainter,
    QSyntaxHighlighter,
    QTextBlockFormat,
    QTextCharFormat,
    QTextCursor,
    QTextFormat,
)
from PySide6.QtWidgets import QTextEdit, QWidget

from ..core.highlight import SQL_FUNCTIONS, SQL_KEYWORDS, SQL_TYPES
from ..resources.theme.tokens import FONTS, PALETTES, SYNTAX

INDENT = "    "  # Python'da girinti 4 boşluk
INDENT_WIDTH = len(INDENT)

# Satır aralığı. Varsayılan (%100) kodda satırları iç içe gösteriyor.
LINE_HEIGHT_PERCENT = 165

LANGUAGE_PYTHON = "python"
LANGUAGE_SQL = "tsql"

COMMENT_PREFIX = {LANGUAGE_PYTHON: "#", LANGUAGE_SQL: "--"}

BRACKET_PAIRS = {"(": ")", "[": "]", "{": "}"}
CLOSING_BRACKETS = set(BRACKET_PAIRS.values())
QUOTES = ('"', "'")

# Otomatik kapatma yalnızca imlecin sağında bunlardan biri (ya da satır
# sonu) varken yapılıyor. Bir kelimenin önüne parantez yazan kişi
# kapatanın oraya eklenmesini beklemiyor: `(|x` → `()x` olmamalı.
CLOSE_BEFORE = set(" \t)]},:;")

# Tırnaktan hemen önce bu önekler varsa tırnak yine kapatılıyor: `f"`,
# `rb"`, SQL'de `N'`. Başka bir harften sonra kapatılmıyor; `don't` yazan
# kişiye ikinci bir kesme işareti eklemek yanlış olur.
STRING_PREFIXES = {
    LANGUAGE_PYTHON: {"f", "r", "b", "u", "rb", "br", "fr", "rf"},
    LANGUAGE_SQL: {"n"},
}

# Bu kelimelerle başlayan satırdan sonra blok bitmiş demek; Enter girintiyi
# bir kademe azaltıyor.
DEDENT_AFTER = ("return", "pass", "break", "continue", "raise")

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

def _char_format(color: str, bold: bool = False, italic: bool = False) -> QTextCharFormat:
    fmt = QTextCharFormat()
    fmt.setForeground(QColor(color))
    if bold:
        fmt.setFontWeight(QFont.Weight.DemiBold)
    if italic:
        fmt.setFontItalic(True)
    return fmt


def _words(words, flags: int = 0, before_paren: bool = False) -> re.Pattern:
    tail = r"(?=\s*\()" if before_paren else ""
    return re.compile(rf"\b(?:{'|'.join(sorted(words))})\b{tail}", flags)


def python_rules(mode: str) -> tuple[list[tuple[object, QTextCharFormat, int]], QTextCharFormat]:
    """Python renklendirme kuralları ve metin (string) biçimi.

    Alıştırma editörü ve not editöründeki kod blokları aynı kuralları
    kullanıyor; iki yerde aynı kod turuncu/mor görünsün diye tek yerde.
    """
    colors = SYNTAX.get(mode, SYNTAX["light"])
    rules: list[tuple[object, QTextCharFormat, int]] = []

    keyword_format = _char_format(colors["keyword"], bold=True)
    for word in KEYWORDS:
        rules.append((re.compile(rf"\b{word}\b"), keyword_format, 0))

    constant_format = _char_format(colors["constant"], bold=True)
    for word in CONSTANTS:
        rules.append((re.compile(rf"\b{word}\b"), constant_format, 0))

    builtin_format = _char_format(colors["builtin"])
    for word in BUILTINS:
        rules.append((re.compile(rf"\b{word}\b(?=\s*\()"), builtin_format, 0))

    # Değer atanan değişken adı: `isim = ...` ve `toplam += ...`
    rules.append(
        (
            re.compile(r"\b([A-Za-z_]\w*)\s*(?:[+\-*/%]?=)(?!=)"),
            _char_format(colors["variable"]),
            1,
        )
    )

    rules.append(
        (re.compile(r"\b(?:def|class)\s+(\w+)"), _char_format(colors["definition"], bold=True), 1)
    )
    rules.append((re.compile(r"@\w+"), _char_format(colors["decorator"]), 0))
    rules.append(
        (re.compile(r"\b\d+\.?\d*(?:[eE][+-]?\d+)?\b"), _char_format(colors["number"]), 0)
    )

    string_format = _char_format(colors["string"])
    rules.append((re.compile(r"'[^'\\\n]*(?:\\.[^'\\\n]*)*'"), string_format, 0))
    rules.append((re.compile(r'"[^"\\\n]*(?:\\.[^"\\\n]*)*"'), string_format, 0))

    # Yorum en sona: metinler önce boyanıyor, yorum kuralı üzerine yazmıyor.
    rules.append(
        (re.compile(r"#[^\n]*"), _char_format(colors["comment"], italic=True), 0)
    )
    return rules, string_format


def sql_rules(mode: str) -> tuple[list[tuple[object, QTextCharFormat, int]], QTextCharFormat]:
    """T-SQL renklendirme kuralları ve çok satırlı yorum biçimi.

    SQL büyük/küçük harfe duyarsız; kurallar da öyle. Aynı kelime hem
    anahtar kelime hem fonksiyon olabiliyor (`LEFT JOIN` / `LEFT(ad, 1)`):
    fonksiyon kuralı sonra geldiği için parantezden önceki kullanım
    fonksiyon rengini alıyor.
    """
    colors = SYNTAX.get(mode, SYNTAX["light"])
    i = re.IGNORECASE
    comment_format = _char_format(colors["comment"], italic=True)
    rules: list[tuple[object, QTextCharFormat, int]] = [
        (_words(SQL_KEYWORDS, i), _char_format(colors["keyword"], bold=True), 0),
        (_words(SQL_TYPES, i), _char_format(colors["definition"]), 0),
        (re.compile(r"\bnull\b", i), _char_format(colors["constant"], bold=True), 0),
        (_words(SQL_FUNCTIONS, i, before_paren=True), _char_format(colors["builtin"]), 0),
        (re.compile(r"@@?\w+"), _char_format(colors["variable"]), 0),
        (re.compile(r"\b\d+\.?\d*\b"), _char_format(colors["number"]), 0),
        # SQL'de metin içindeki tırnak iki kez yazılıyor: 'O''Brien'.
        # `\b` yalnızca N önekine: boşluktan sonra gelen tırnakta kelime
        # sınırı yok ve kural hiç eşleşmiyordu (metindeki `and` boyanıyordu).
        (re.compile(r"(?:\bN)?'(?:[^']|'')*'", i), _char_format(colors["string"]), 0),
        (re.compile(r"--[^\n]*"), comment_format, 0),
    ]
    return rules, comment_format


class _RuleHighlighter(QSyntaxHighlighter):
    """Kural listesiyle boyayan ortak gövde; alt sınıflar kuralları verir."""

    def __init__(self, document, mode: str = "light") -> None:
        super().__init__(document)
        self._rules: list[tuple[object, QTextCharFormat, int]] = []
        self._span_format = QTextCharFormat()
        self.set_mode(mode)

    def _build(self, mode: str) -> tuple[list, QTextCharFormat]:
        raise NotImplementedError

    def set_mode(self, mode: str) -> None:
        """Tema değişince renkleri yenile."""
        self._rules, self._span_format = self._build(mode)
        self.rehighlight()

    def highlightBlock(self, text: str) -> None:  # noqa: N802 (Qt adlandırması)
        for pattern, fmt, group in self._rules:
            for match in pattern.finditer(text):
                start, end = match.span(group) if group else match.span()
                if start >= 0:
                    self.setFormat(start, end - start, fmt)

        self._highlight_multiline(text)

    def _highlight_multiline(self, text: str) -> None:
        """Satırlar boyunca süren parçalar (metin ya da yorum)."""


class PythonHighlighter(_RuleHighlighter):
    """Python sözdizimi renklendirmesi.

    Bilinçli olarak basit tutuldu: anahtar kelimeler, sabitler, hazır
    fonksiyonlar, atanan değişken adları, metinler, sayılar, yorumlar ve
    tanımlar.
    """

    def _build(self, mode: str) -> tuple[list, QTextCharFormat]:
        return python_rules(mode)

    def _highlight_multiline(self, text: str) -> None:
        """Üç tırnaklı metinleri satırlar boyunca takip eder."""
        delimiters = ('"""', "'''")

        if self.previousBlockState() > 0:
            index = self.previousBlockState() - 1
            delimiter = delimiters[index]
            end = text.find(delimiter)
            if end == -1:
                self.setFormat(0, len(text), self._span_format)
                self.setCurrentBlockState(self.previousBlockState())
                return
            self.setFormat(0, end + 3, self._span_format)
            start_from = end + 3
        else:
            start_from = 0

        for index, delimiter in enumerate(delimiters):
            found = text.find(delimiter, start_from)
            if found == -1:
                continue
            end = text.find(delimiter, found + 3)
            if end == -1:
                self.setFormat(found, len(text) - found, self._span_format)
                self.setCurrentBlockState(index + 1)
            else:
                self.setFormat(found, end - found + 3, self._span_format)
            return


class SqlHighlighter(_RuleHighlighter):
    """T-SQL renklendirmesi.

    SQL alıştırmaları önce Python kurallarıyla boyanıyordu: `SELECT`
    renksiz kalıyor, `--` yorumu yorum gibi görünmüyor, `in` ve `and` ise
    Python anahtar kelimesi olarak boyanıyordu.
    """

    def _build(self, mode: str) -> tuple[list, QTextCharFormat]:
        return sql_rules(mode)

    def _highlight_multiline(self, text: str) -> None:
        """`/* ... */` yorumlarını satırlar boyunca takip eder."""
        self.setCurrentBlockState(0)
        if self.previousBlockState() == 1:
            start, search_from = 0, 0
        else:
            start = text.find("/*")
            search_from = start + 2
        while start >= 0:
            end = text.find("*/", search_from)
            if end == -1:
                self.setFormat(start, len(text) - start, self._span_format)
                self.setCurrentBlockState(1)
                return
            self.setFormat(start, end + 2 - start, self._span_format)
            start = text.find("/*", end + 2)
            search_from = start + 2


HIGHLIGHTERS = {LANGUAGE_PYTHON: PythonHighlighter, LANGUAGE_SQL: SqlHighlighter}


class CodeEditing:
    """Kod yazma kolaylıkları; `QTextEdit` tabanlı editörlere karışır.

    Alıştırma editörü (`CodeEditor`) her yerde, not editörü (`NoteEditor`)
    yalnızca kod bloklarının içinde kullanıyor. Önce yalnızca alıştırma
    editöründe vardı; notlardaki kod bloğunda parantez kapanmıyordu (Alican
    bildirdi).

    Alt sınıf `_code_language` ile o anki dili veriyor: `python`, `tsql` ya
    da tanınmayan bir blok için boş metin (yorum işareti yok, tırnak öneki
    yok; parantez ve girinti yine çalışıyor).
    """

    def _code_language(self) -> str:
        return LANGUAGE_PYTHON

    def handle_code_key(self, event: QKeyEvent) -> bool:
        """Kod yazma kolaylıkları. Tuşu işlediyse `True` döndürür.

        `Ctrl+Enter` burada işlenmiyor; onun ne yapacağı (çalıştırmak ya da
        hiçbir şey) editöre bağlı.
        """
        key = event.key()
        modifiers = event.modifiers()
        # Windows AltGr'yi Ctrl+Alt olarak bildiriyor; Türkçe klavyede
        # `{ [ ] }` AltGr ile yazılıyor. Onlar kısayol değil, karakter.
        ctrl = bool(modifiers & Qt.KeyboardModifier.ControlModifier) and not (
            modifiers & Qt.KeyboardModifier.AltModifier
        )
        text = event.text()

        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if ctrl:
                return False
            self._newline()
            return True

        # Türkçe klavyede `/` Shift+7 ile yazılıyor; Ctrl+Shift+7 de kabul.
        if ctrl and (key == Qt.Key.Key_Slash or (key == Qt.Key.Key_7 and modifiers & Qt.KeyboardModifier.ShiftModifier)):
            self._toggle_comment()
            return True

        if key == Qt.Key.Key_Tab and not modifiers:
            self._indent()
            return True

        if key == Qt.Key.Key_Backtab:
            self._dedent()
            return True

        if key == Qt.Key.Key_Backspace and not modifiers and self._smart_backspace():
            return True

        if not ctrl and text:
            if text in BRACKET_PAIRS and self._open_bracket(text):
                return True
            if text in QUOTES and self._quote(text):
                return True
            if text in CLOSING_BRACKETS and self._skip_closing(text):
                return True

        return False

    # İmlecin solundaki ve sağındaki satır parçası.
    def _around_cursor(self) -> tuple[str, str]:
        cursor = self.textCursor()
        line = cursor.block().text()
        column = cursor.positionInBlock()
        return line[:column], line[column:]

    def _move(self, steps: int) -> None:
        cursor = self.textCursor()
        operation = (
            QTextCursor.MoveOperation.Right if steps > 0 else QTextCursor.MoveOperation.Left
        )
        cursor.movePosition(operation, QTextCursor.MoveMode.MoveAnchor, abs(steps))
        self.setTextCursor(cursor)

    def _wrap_selection(self, opening: str, closing: str) -> None:
        """Seçili metni iki işaretin arasına alır, seçim içeride kalır."""
        cursor = self.textCursor()
        selected = cursor.selectedText()
        start = cursor.selectionStart()
        cursor.insertText(f"{opening}{selected}{closing}")
        cursor.setPosition(start + len(opening))
        cursor.setPosition(start + len(opening) + len(selected), QTextCursor.MoveMode.KeepAnchor)
        self.setTextCursor(cursor)

    def _open_bracket(self, opening: str) -> bool:
        cursor = self.textCursor()
        closing = BRACKET_PAIRS[opening]
        if cursor.hasSelection():
            if " " in cursor.selectedText():
                return False
            self._wrap_selection(opening, closing)
            return True
        _before, after = self._around_cursor()
        if after and after[0] not in CLOSE_BEFORE:
            return False
        cursor.insertText(opening + closing)
        self._move(-1)
        return True

    def _quote(self, quote: str) -> bool:
        cursor = self.textCursor()
        if cursor.hasSelection():
            if " " in cursor.selectedText():
                return False
            self._wrap_selection(quote, quote)
            return True

        before, after = self._around_cursor()
        if after.startswith(quote):
            self._move(1)
            return True
        if after and after[0] not in CLOSE_BEFORE:
            return False
        if before.endswith(quote):
            # Üçlü tırnak yazılıyor ya da boş bir metin kapatılıyor.
            return False
        word = re.search(r"(\w+)$", before)
        if word:
            prefix = word.group(1).lower()
            if prefix not in STRING_PREFIXES.get(self._code_language(), set()):
                return False
        cursor.insertText(quote + quote)
        self._move(-1)
        return True

    def _skip_closing(self, closing: str) -> bool:
        if self.textCursor().hasSelection():
            return False
        _before, after = self._around_cursor()
        if not after.startswith(closing):
            return False
        self._move(1)
        return True

    def _smart_backspace(self) -> bool:
        """Boş çifti birlikte, girintiyi kademe kademe siler."""
        cursor = self.textCursor()
        if cursor.hasSelection():
            return False
        before, after = self._around_cursor()
        if not before:
            return False

        pairs = {**BRACKET_PAIRS, '"': '"', "'": "'"}
        if before[-1] in pairs and after.startswith(pairs[before[-1]]):
            cursor.movePosition(QTextCursor.MoveOperation.Left)
            cursor.movePosition(
                QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 2
            )
            cursor.removeSelectedText()
            return True

        if before.strip(" ") == "":
            remove = len(before) % INDENT_WIDTH or INDENT_WIDTH
            cursor.movePosition(
                QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor, remove
            )
            cursor.removeSelectedText()
            return True
        return False

    def _newline(self) -> None:
        """Enter: girintiyi korur, bloğa göre artırır ya da azaltır.

        **Satır sonu Qt'ye bırakılmıyor.** Satır aralığı verilmiş boş bir
        satırda Qt'nin kendi Enter'ı yutuluyordu; `insertPlainText("\\n")`
        her durumda çalışıyor (not editöründe de aynısı yapılıyor).
        """
        cursor = self.textCursor()
        before, after = self._around_cursor()
        line = cursor.block().text()
        indent = line[: len(line) - len(line.lstrip(" "))]
        stripped = before.rstrip()

        if self._code_language() == LANGUAGE_PYTHON and stripped.endswith(":"):
            indent += INDENT
        elif (
            self._code_language() == LANGUAGE_PYTHON
            and not after.strip()
            and stripped.lstrip().split(" ")[0] in DEDENT_AFTER
        ):
            indent = indent[:-INDENT_WIDTH]

        cursor.beginEditBlock()
        # İmlecin sağındaki boşluklar yeni satırın başına taşınmasın.
        spaces_after = len(after) - len(after.lstrip(" "))
        if spaces_after:
            eraser = self.textCursor()
            eraser.movePosition(
                QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, spaces_after
            )
            eraser.removeSelectedText()
            after = after[spaces_after:]

        opener = stripped[-1:] if stripped else ""
        if opener in BRACKET_PAIRS and after.startswith(BRACKET_PAIRS[opener]):
            # `(|)` → açan satırda kalır, içerik bir kademe içeride, kapatan
            # kendi satırında.
            self.insertPlainText("\n" + indent + INDENT + "\n" + indent)
            self._move(-(len(indent) + 1))
        else:
            if opener in BRACKET_PAIRS:
                indent += INDENT
            self.insertPlainText("\n" + indent)
        cursor.endEditBlock()

    # --- satır işlemleri --------------------------------------------------

    def _selected_blocks(self) -> tuple[int, int]:
        """Seçimin kapsadığı ilk ve son satır numarası.

        Seçim bir satırın en başında bitiyorsa o satır dahil edilmiyor:
        satırları fareyle aşağı doğru seçen kişi imleci bir sonraki satırın
        başına bırakıyor.
        """
        cursor = self.textCursor()
        document = self.document()
        first = document.findBlock(cursor.selectionStart()).blockNumber()
        end_block = document.findBlock(cursor.selectionEnd())
        last = end_block.blockNumber()
        if cursor.hasSelection() and last > first and cursor.selectionEnd() == end_block.position():
            last -= 1
        return first, last

    def _edit_lines(self, change) -> None:
        """Seçili satırların her birine `change(metin) -> metin` uygular.

        Seçim işlemden sonra aynı satırları kapsayacak şekilde yeniden
        kuruluyor; art arda Tab ya da yorum işlemi yapılabiliyor.
        """
        first, last = self._selected_blocks()
        had_selection = self.textCursor().hasSelection()
        column = self.textCursor().positionInBlock()
        document = self.document()
        cursor = QTextCursor(document)
        cursor.beginEditBlock()
        shift = 0
        for number in range(first, last + 1):
            block = document.findBlockByNumber(number)
            original = block.text()
            updated = change(original)
            if updated == original:
                continue
            shift = len(updated) - len(original)
            line = QTextCursor(block)
            line.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
            line.insertText(updated)
        cursor.endEditBlock()

        result = self.textCursor()
        if not had_selection:
            # Seçim yoksa imleç satırda kalıyor, eklenen/silinen kadar kayıyor.
            block = document.findBlockByNumber(first)
            result.setPosition(block.position() + max(0, min(column + shift, block.length() - 1)))
        else:
            last_block = document.findBlockByNumber(last)
            result.setPosition(document.findBlockByNumber(first).position())
            result.setPosition(
                last_block.position() + last_block.length() - 1, QTextCursor.MoveMode.KeepAnchor
            )
        self.setTextCursor(result)

    def _indent(self) -> None:
        if self.textCursor().hasSelection():
            self._edit_lines(lambda text: INDENT + text if text.strip() else text)
            return
        # Tek satır: bir sonraki girinti durağına kadar boşluk.
        before, _after = self._around_cursor()
        self.insertPlainText(" " * (INDENT_WIDTH - len(before) % INDENT_WIDTH))

    def _dedent(self) -> None:
        def remove(text: str) -> str:
            leading = len(text) - len(text.lstrip(" "))
            return text[min(leading, INDENT_WIDTH):]

        self._edit_lines(remove)

    def _toggle_comment(self) -> None:
        """Seçili satırları yoruma alır; hepsi yorumsa yorumdan çıkarır."""
        prefix = COMMENT_PREFIX.get(self._code_language(), "")
        if not prefix:
            return
        first, last = self._selected_blocks()
        document = self.document()
        lines = [document.findBlockByNumber(n).text() for n in range(first, last + 1)]
        filled = [line for line in lines if line.strip()]
        if not filled:
            return

        commented = all(line.lstrip(" ").startswith(prefix) for line in filled)
        column = min(len(line) - len(line.lstrip(" ")) for line in filled)

        def change(text: str) -> str:
            if not text.strip():
                return text
            if commented:
                leading = len(text) - len(text.lstrip(" "))
                rest = text[leading + len(prefix):]
                if rest.startswith(" "):
                    rest = rest[1:]
                return text[:leading] + rest
            return text[:column] + prefix + " " + text[column:]

        self._edit_lines(change)


class LineNumberArea(QWidget):
    """Editörün solundaki satır numarası şeridi."""

    def __init__(self, editor: "CodeEditor") -> None:
        super().__init__(editor)
        self._editor = editor

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(self._editor.line_number_width(), 0)

    def paintEvent(self, event) -> None:  # noqa: N802
        self._editor.paint_line_numbers(event)


class CodeEditor(CodeEditing, QTextEdit):
    """Alıştırmaların yazıldığı editör."""

    run_requested = Signal()

    def __init__(self, parent: QWidget | None = None, mode: str = "light") -> None:
        super().__init__(parent)
        self._mode = mode
        self._language = LANGUAGE_PYTHON
        self._spacing_queued = False
        self._line_area = LineNumberArea(self)
        self._highlighter: _RuleHighlighter = PythonHighlighter(self.document(), mode)

        font = QFont()
        font.setFamily(FONTS["mono"].split(",")[0].strip().strip('"'))
        font.setPointSize(11)
        font.setFixedPitch(True)
        self.setFont(font)

        self.setTabStopDistance(QFontMetrics(font).horizontalAdvance(" ") * INDENT_WIDTH)
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

    # --- dil --------------------------------------------------------------

    def set_language(self, language: str) -> None:
        """Renklendirmeyi ve yorum işaretini alıştırmanın diline göre seçer."""
        language = language if language in HIGHLIGHTERS else LANGUAGE_PYTHON
        if language == self._language:
            return
        self._language = language
        self._highlighter.setDocument(None)
        self._highlighter = HIGHLIGHTERS[language](self.document(), self._mode)

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
        """Satır aralığı eksik olan bloklara uygular.

        `QPlainTextEdit` bu ayarı yok sayıyordu; `QTextEdit` uyguluyor.
        Yeni satırlar da aralığı alsın diye satır sayısı değiştikçe tekrar
        uygulanıyor — her tuş vuruşunda değil, yalnızca satır eklenip
        silindiğinde.

        Eskiden tüm belge seçilip `mergeBlockFormat` çağrılıyordu; bu,
        Enter'a basıldığında yeni satırın bir an aralıksız görünmesine
        yol açıyordu (satır numaraları birbirine yapışıyor, sonraki
        olay turunda düzeliyordu). Şimdi yalnızca doğru aralığa sahip
        olmayan bloklar düzeltiliyor.
        """
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

    # --- girinti çizgileri ------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        self._paint_indent_guides(event)

    def _line_indents(self) -> list[int]:
        """Her satırın girinti kademesi.

        Boş satır iki komşusundan küçük olanın kademesini alıyor: bir
        fonksiyonun içindeki boş satırda çizgi kesilmiyor, fonksiyon
        bitince de uzamıyor.
        """
        raw: list[int | None] = []
        block = self.document().begin()
        while block.isValid():
            text = block.text()
            if text.strip():
                raw.append((len(text) - len(text.lstrip(" "))) // INDENT_WIDTH)
            else:
                raw.append(None)
            block = block.next()

        levels = [0] * len(raw)
        previous = 0
        for index, value in enumerate(raw):
            if value is not None:
                previous = value
            levels[index] = previous if value is None else value
        following = 0
        for index in range(len(raw) - 1, -1, -1):
            if raw[index] is not None:
                following = raw[index]
            else:
                levels[index] = min(levels[index], following)
        return levels

    def _paint_indent_guides(self, event) -> None:
        palette = PALETTES.get(self._mode, PALETTES["light"])
        painter = QPainter(self.viewport())
        painter.setPen(QColor(palette["border"]))

        document = self.document()
        layout = document.documentLayout()
        space = QFontMetricsF(self.font()).horizontalAdvance(" ")
        left = document.documentMargin() - self.horizontalScrollBar().value()
        offset = self.verticalScrollBar().value()
        area = event.rect()

        levels = self._line_indents()
        block = document.begin()
        while block.isValid():
            rect = layout.blockBoundingRect(block)
            top = rect.top() - offset
            if top > area.bottom():
                break
            if top + rect.height() >= area.top():
                for level in range(levels[block.blockNumber()]):
                    x = int(left + level * INDENT_WIDTH * space) + 1
                    painter.drawLine(x, int(top), x, int(top + rect.height()))
            block = block.next()

    # --- düzenleme kolaylıkları -------------------------------------------

    def set_mode(self, mode: str) -> None:
        """Tema değişince renklendirmeyi, satır vurgusunu ve çizgileri yenile."""
        self._mode = mode
        self._highlighter.set_mode(mode)
        self._highlight_current_line()
        self._line_area.update()
        self.viewport().update()

    def _code_language(self) -> str:
        return self._language

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        modifiers = event.modifiers()
        ctrl = bool(modifiers & Qt.KeyboardModifier.ControlModifier) and not (
            modifiers & Qt.KeyboardModifier.AltModifier
        )
        if ctrl and event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.run_requested.emit()
            return
        if self.handle_code_key(event):
            return
        super().keyPressEvent(event)
