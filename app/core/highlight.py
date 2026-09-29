"""Kod bloklarını HTML olarak renklendirir.

Ders metinlerindeki ``` ile açılan kod blokları, maketteki renklerle
boyanmış HTML'e çevriliyor. Pygments gibi bir bağımlılık eklemedim; kurallar
editördekiyle aynı olsun diye tek yerden yönetiliyor.

İki dil tanınıyor: Python ve SQL (T-SQL). Kod bloğunun etiketi (```` ```sql ````)
hangisinin kullanılacağını söylüyor; etiketsiz blok Python sayılıyor, başka
bir etiket boyanmıyor. SQL kelime listeleri burada duruyor ve kod
editörü de (`widgets/code_editor.py`) buradan alıyor: ders metni, not,
sınav ve editör aynı kelimeyi aynı renkte gösteriyor.

Renkler `tokens.SYNTAX` sözlüğünden geliyor, yani tema değişince kod da
değişiyor.
"""

from __future__ import annotations

import html
import re
from collections.abc import Iterator

from ..resources.theme.tokens import SYNTAX

LANGUAGE_PYTHON = "python"
LANGUAGE_SQL = "sql"

# Kod bloğu etiketinden dile.
LANGUAGE_TAGS = {
    "": LANGUAGE_PYTHON,
    "python": LANGUAGE_PYTHON,
    "py": LANGUAGE_PYTHON,
    "sql": LANGUAGE_SQL,
    "tsql": LANGUAGE_SQL,
    "t-sql": LANGUAGE_SQL,
}

KEYWORDS = {
    "and", "as", "assert", "async", "await", "break", "class", "continue",
    "def", "del", "elif", "else", "except", "finally", "for", "from",
    "global", "if", "import", "in", "is", "lambda", "nonlocal", "not", "or",
    "pass", "raise", "return", "try", "while", "with", "yield",
}

CONSTANTS = {"True", "False", "None"}

BUILTINS = {
    "abs", "all", "any", "bool", "dict", "dir", "enumerate", "filter", "float",
    "format", "input", "int", "len", "list", "map", "max", "min", "open",
    "print", "range", "repr", "reversed", "round", "set", "sorted", "str",
    "sum", "tuple", "type", "zip",
}

SQL_KEYWORDS = {
    "add", "all", "alter", "and", "as", "asc", "begin", "between", "by",
    "case", "catch", "check", "commit", "constraint", "create", "cross",
    "current", "database", "declare", "default", "delete", "desc", "distinct",
    "drop", "else", "end", "exec", "execute", "exists", "fetch", "following",
    "for", "foreign", "from", "full", "go", "group", "having", "identity",
    "if", "in", "index", "inner", "insert", "into", "is", "join", "key",
    "left", "like", "merge", "next", "nocount", "not", "of", "offset", "on",
    "only", "or", "order", "outer", "output", "over", "partition",
    "preceding", "primary", "print", "proc", "procedure", "range",
    "references", "return", "right", "rollback", "row", "rows", "select",
    "set", "table", "then", "throw", "top", "tran", "transaction", "try",
    "unbounded", "union", "unique", "update", "use", "values", "view",
    "when", "where", "while", "with",
}

SQL_TYPES = {
    "bigint", "bit", "char", "date", "datetime", "datetime2", "decimal",
    "float", "int", "money", "nchar", "numeric", "nvarchar", "real",
    "smallint", "text", "time", "tinyint", "varchar",
}

SQL_FUNCTIONS = {
    "abs", "avg", "cast", "ceiling", "charindex", "coalesce", "concat",
    "convert", "count", "dateadd", "datediff", "datepart", "day",
    "dense_rank", "first_value", "floor", "format", "getdate", "iif",
    "isnull", "lag", "last_value", "lead", "left", "len", "lower", "ltrim",
    "max", "min", "month", "ntile", "nullif", "power", "rank", "replace",
    "right", "round", "row_number", "rtrim", "sqrt", "string_agg",
    "substring", "sum", "trim", "upper", "year",
}

SQL_CONSTANTS = {"null"}

# Sıra önemli: metin ve yorumlar önce yakalanmalı ki içlerindeki anahtar
# kelimeler boyanmasın.
TOKEN_PATTERN = re.compile(
    r"""
    (?P<comment>\#[^\n]*)
  | (?P<string>'''(?:.|\n)*?'''|\"\"\"(?:.|\n)*?\"\"\"|'(?:\\.|[^'\\\n])*'|"(?:\\.|[^"\\\n])*")
  | (?P<number>\b\d+\.?\d*(?:[eE][+-]?\d+)?\b)
  | (?P<name>\b[A-Za-z_]\w*\b)
    """,
    re.VERBOSE,
)

SQL_TOKEN_PATTERN = re.compile(
    r"""
    (?P<comment>--[^\n]*|/\*[\s\S]*?(?:\*/|$))
  | (?P<string>(?:\bN)?'(?:[^']|'')*')
  | (?P<variable>@@?\w+)
  | (?P<number>\b\d+\.?\d*\b)
  | (?P<name>\b[A-Za-z_]\w*\b)
    """,
    re.VERBOSE | re.IGNORECASE,
)


def _is_assignment_target(source: str, position: int) -> bool:
    """Bu adın hemen ardından değer ataması geliyor mu?

    `isim = "Alican"` içindeki `isim` evet; `a == b` içindeki `a` hayır.
    `+=`, `-=` gibi birleşik atamalar da sayılıyor.
    """
    rest = source[position:]
    stripped = rest.lstrip(" \t")

    if not stripped.startswith("="):
        # +=, -=, *= gibi birleşik atamalar
        if len(stripped) >= 2 and stripped[0] in "+-*/%" and stripped[1] == "=":
            return True
        return False

    # Tek '=' atama, '==' karşılaştırma.
    return not stripped.startswith("==")


def _followed_by_paren(source: str, position: int) -> bool:
    return source[position:].lstrip(" \t").startswith("(")


def _python_tokens(source: str) -> Iterator[tuple[str | None, str]]:
    """Python kodunu (tür, metin) parçalarına ayırır; tür `None` ise düz metin."""
    position = 0
    for match in TOKEN_PATTERN.finditer(source):
        yield None, source[position:match.start()]
        text = match.group()
        kind = match.lastgroup
        if kind == "name":
            if text in KEYWORDS:
                kind = "keyword"
            elif text in CONSTANTS:
                kind = "constant"
            elif text in BUILTINS and source[match.end():match.end() + 1] == "(":
                kind = "builtin"
            elif _is_assignment_target(source, match.end()):
                # Değer atanan değişken adı ayrı renkte. Gözün "burada ne
                # tanımlanıyor" sorusunu tek bakışta cevaplaması için.
                kind = "variable"
            else:
                kind = None
        yield kind, text
        position = match.end()
    yield None, source[position:]


def _sql_tokens(source: str) -> Iterator[tuple[str | None, str]]:
    """SQL kodunu (tür, metin) parçalarına ayırır.

    Aynı kelime hem anahtar kelime hem fonksiyon olabiliyor (`LEFT JOIN` /
    `LEFT(ad, 1)`): parantezden önce geliyorsa fonksiyon sayılıyor.
    """
    position = 0
    for match in SQL_TOKEN_PATTERN.finditer(source):
        yield None, source[position:match.start()]
        text = match.group()
        kind = match.lastgroup
        if kind == "name":
            word = text.lower()
            if word in SQL_FUNCTIONS and _followed_by_paren(source, match.end()):
                kind = "builtin"
            elif word in SQL_KEYWORDS:
                kind = "keyword"
            elif word in SQL_TYPES:
                kind = "definition"
            elif word in SQL_CONSTANTS:
                kind = "constant"
            else:
                kind = None
        yield kind, text
        position = match.end()
    yield None, source[position:]


TOKENIZERS = {LANGUAGE_PYTHON: _python_tokens, LANGUAGE_SQL: _sql_tokens}

# Satır içi stilde kalın ya da eğik yazılan türler.
BOLD_KINDS = {"keyword", "constant"}
ITALIC_KINDS = {"comment"}


def language_for_tag(tag: str) -> str | None:
    """Kod bloğu etiketinden dil; tanınmayan etiket için `None` (boyanmaz)."""
    return LANGUAGE_TAGS.get(tag.strip().lower())


def highlight_code(source: str, language: str | None, mode: str = "light") -> str:
    """Kodu **satır içi renklerle** boyanmış HTML'e çevirir.

    Qt'nin zengin metni sınıf tabanlı stil tanımadığı için sınav ekranı
    bunu kullanıyor.
    """
    tokenizer = TOKENIZERS.get(language or "")
    if tokenizer is None:
        return html.escape(source)
    colors = SYNTAX.get(mode, SYNTAX["light"])
    parts: list[str] = []
    for kind, text in tokenizer(source):
        if not text:
            continue
        if kind is None:
            parts.append(html.escape(text))
            continue
        style = f"color:{colors[kind]};"
        if kind in BOLD_KINDS:
            style += "font-weight:600;"
        if kind in ITALIC_KINDS:
            style += "font-style:italic;"
        parts.append(f'<span style="{style}">{html.escape(text)}</span>')
    return "".join(parts)


# Belge alanlarında kullanılan sınıf adları. Renk değil **sınıf** yazmanın
# sebebi: tema değişince belgeyi baştan yüklemek gerekmiyor, yalnızca stil
# bloğu değiştiriliyor. Satır içi renk yazılsaydı her tema değişiminde bütün
# belge yeniden yüklenirdi ve renk gecikmeli değişirdi (ölçüldü: ~190 ms).
CLASS_PREFIX = "hl-"


def highlight_code_classes(source: str, language: str | None) -> str:
    """Kodu **CSS sınıflarıyla** işaretlenmiş HTML'e çevirir.

    Renk taşımıyor; renkleri belge stil bloğu veriyor.
    """
    tokenizer = TOKENIZERS.get(language or "")
    if tokenizer is None:
        return html.escape(source)
    parts: list[str] = []
    for kind, text in tokenizer(source):
        if not text:
            continue
        if kind is None:
            parts.append(html.escape(text))
        else:
            parts.append(f'<span class="{CLASS_PREFIX}{kind}">{html.escape(text)}</span>')
    return "".join(parts)


FENCE_PATTERN = re.compile(r"<pre><code(?: class=\"([^\"]*)\")?>(.*?)</code></pre>", re.DOTALL)


def highlight_code_blocks(rendered_html: str, mode: str = "light") -> str:
    """Markdown'dan çıkan HTML içindeki kod bloklarını renklendirir.

    `markdown` kütüphanesi kod bloklarını ``<pre><code>`` olarak üretiyor;
    içerik zaten HTML kaçışlı geldiği için önce çözüp sonra boyuyoruz.

    `mode` artık kullanılmıyor: renkler sınıflarla veriliyor ve stil
    bloğundan geliyor. Parametre, çağrı yerlerini bozmamak için duruyor.
    """

    def replace(match: re.Match) -> str:
        tag = (match.group(1) or "").replace("language-", "")
        body = html.unescape(match.group(2))
        return f"<pre><code>{highlight_code_classes(body, language_for_tag(tag))}</code></pre>"

    return FENCE_PATTERN.sub(replace, rendered_html)
