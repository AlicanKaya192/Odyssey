r"""Ders metnindeki formüller.

Formüller markdown içinde LaTeX olarak yazılıyor: satır içinde `$x^2$`,
kendi satırında `$$ ... $$`. Sayfada KaTeX çiziyor
(`app/resources/katex`, pakete gömülü; ağ yok).

**Markdown'dan önce ayıklanıyor.** Markdown formülün içini bozuyor:
`x_i` ile `y_j` arasını italik yapıyor, `\\` ve `\{` kaçışlarını yiyor.
Formüller önce yer tutucuya çevriliyor, markdown çalışıyor, sonra
`<span class="math">` olarak geri konuyor.

Kod bloklarının ve satır içi kodun içine dokunulmuyor: `$` orada kod.
Metinde düz dolar işareti gerekiyorsa `\$` yazılır.

**Sınav soruları bu yoldan geçmiyor.** Sorular Qt etiketiyle (`QLabel`)
çiziliyor, orada KaTeX yok; sorudaki formül Unicode ile yazılır (`x²`,
`Σ`, `√`).
"""

from __future__ import annotations

import html
import re

# Kod: çitli blok ya da satır içi kod. Bunların içi olduğu gibi kalıyor.
_CODE = re.compile(r"(^```.*?^```[ \t]*$|`[^`\n]+`)", re.MULTILINE | re.DOTALL)

_DISPLAY = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
# Satır içi: açılışın ardından ve kapanışın önünden boşluk gelmiyor, kapanışın
# ardından rakam gelmiyor. Böylece "5$ ile 10$" gibi bir metin formül sayılmıyor.
# Formül tek bir satır sonunu aşabiliyor (paragraf seksen sütunda bölünüyor),
# boş satırı aşamıyor: orası yeni paragraf.
_INLINE = re.compile(r"(?<![\\$])\$(?=\S)((?:[^$\n]|\n(?![ \t]*\n))+?)(?<=\S)\$(?!\d)")

_ESCAPED_DOLLAR = "\\$"

# Harf ve rakamdan oluşuyor: markdown'ın dokunacağı hiçbir karakter yok.
_TOKEN = "KATEXMATH{}END"
_TOKEN_RE = re.compile(r"(<p>)?KATEXMATH(\d+)END(</p>)?")
_DOLLAR_TOKEN = "KATEXDOLLAREND"


def protect(text: str) -> tuple[str, list[tuple[str, bool]]]:
    """Formülleri yer tutucuya çevirir.

    Dönen liste `(tex, kendi satırında mı)` çiftleri; `restore` sırayla
    geri koyuyor.
    """
    formulas: list[tuple[str, bool]] = []

    def display(match: re.Match) -> str:
        formulas.append((match.group(1).strip(), True))
        return _TOKEN.format(len(formulas) - 1)

    def inline(match: re.Match) -> str:
        formulas.append((match.group(1), False))
        return _TOKEN.format(len(formulas) - 1)

    parts = _CODE.split(text)
    for index in range(0, len(parts), 2):
        part = parts[index].replace(_ESCAPED_DOLLAR, _DOLLAR_TOKEN)
        part = _DISPLAY.sub(display, part)
        parts[index] = _INLINE.sub(inline, part)
    return "".join(parts), formulas


def restore(body: str, formulas: list[tuple[str, bool]]) -> str:
    """Yer tutucuları KaTeX'in çizeceği öğelere çevirir."""
    if not formulas:
        return body.replace(_DOLLAR_TOKEN, "$")

    def put(match: re.Match) -> str:
        opened, index, closed = match.group(1), int(match.group(2)), match.group(3)
        tex, is_display = formulas[index]
        escaped = html.escape(tex)
        if is_display:
            # Kendi paragrafındaysa `<p>` kalkıyor; blok öğe paragrafın
            # içinde duramıyor.
            element = f'<div class="math display">{escaped}</div>'
            if opened and closed:
                return element
            return f"{opened or ''}{element}{closed or ''}"
        return f'{opened or ""}<span class="math">{escaped}</span>{closed or ""}'

    return _TOKEN_RE.sub(put, body).replace(_DOLLAR_TOKEN, "$")


def plain(text: str, formulas: list[tuple[str, bool]]) -> str:
    """Yer tutucuları formülün kendi metniyle değiştirir (başlık listesi)."""
    return _TOKEN_RE.sub(lambda m: formulas[int(m.group(2))][0], text).replace(_DOLLAR_TOKEN, "$")


def has_math(body: str) -> bool:
    """Sayfaya KaTeX yüklenmeli mi?"""
    return 'class="math' in body
