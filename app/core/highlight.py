"""Kod bloklarını HTML olarak renklendirir.

Ders metinlerindeki ``` ile açılan kod blokları, maketteki renklerle
boyanmış HTML'e çevriliyor. Pygments gibi bir bağımlılık eklemedim; kurallar
editördekiyle aynı olsun diye tek yerden yönetiliyor.

Renkler `tokens.SYNTAX` sözlüğünden geliyor, yani tema değişince kod da
değişiyor.
"""

from __future__ import annotations

import html
import re

from ..resources.theme.tokens import SYNTAX

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


def highlight_python(source: str, mode: str = "light") -> str:
    """Python kodunu renklendirilmiş HTML'e çevirir."""
    colors = SYNTAX.get(mode, SYNTAX["light"])
    parts: list[str] = []
    position = 0

    def span(color_key: str, text: str, bold: bool = False) -> str:
        weight = "font-weight:600;" if bold else ""
        return f'<span style="color:{colors[color_key]};{weight}">{html.escape(text)}</span>'

    for match in TOKEN_PATTERN.finditer(source):
        parts.append(html.escape(source[position:match.start()]))
        text = match.group()

        if match.lastgroup == "comment":
            parts.append(
                f'<span style="color:{colors["comment"]};font-style:italic;">'
                f"{html.escape(text)}</span>"
            )
        elif match.lastgroup == "string":
            parts.append(span("string", text))
        elif match.lastgroup == "number":
            parts.append(span("number", text))
        elif text in KEYWORDS:
            parts.append(span("keyword", text, bold=True))
        elif text in CONSTANTS:
            parts.append(span("constant", text, bold=True))
        elif text in BUILTINS and source[match.end():match.end() + 1] == "(":
            parts.append(span("builtin", text))
        else:
            parts.append(html.escape(text))

        position = match.end()

    parts.append(html.escape(source[position:]))
    return "".join(parts)


FENCE_PATTERN = re.compile(r"<pre><code(?: class=\"([^\"]*)\")?>(.*?)</code></pre>", re.DOTALL)


def highlight_code_blocks(rendered_html: str, mode: str = "light") -> str:
    """Markdown'dan çıkan HTML içindeki kod bloklarını renklendirir.

    `markdown` kütüphanesi kod bloklarını ``<pre><code>`` olarak üretiyor;
    içerik zaten HTML kaçışlı geldiği için önce çözüp sonra boyuyoruz.
    """

    def replace(match: re.Match) -> str:
        language = (match.group(1) or "").replace("language-", "").strip()
        body = html.unescape(match.group(2))

        # Yalnızca Python boyanıyor; başka dil belirtilmişse dokunulmuyor.
        if language and language not in ("python", "py"):
            return f"<pre><code>{html.escape(body)}</code></pre>"

        return f"<pre><code>{highlight_python(body, mode)}</code></pre>"

    return FENCE_PATTERN.sub(replace, rendered_html)
