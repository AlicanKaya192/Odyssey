"""Sınav metinlerinde kod gösterimi.

Konu anlatımı ve ders notları Chromium ile çiziliyor, orada CSS'in tamamı
çalışıyor. Sınav ise normal Qt bileşenleriyle kuruluyor — soru bir `QLabel`,
şıklar birer satır. Qt'nin zengin metni CSS'in yalnızca küçük bir alt kümesini
tanıyor: yuvarlak köşe ve kenarlık yok, ama **yazı tipi, renk ve arka plan**
çalışıyor. Kod parçalarını tek aralıklı yazıp zemin vermeye bu yetiyor.

Kod blokları için tek hücreli bir tablo kullanılıyor. Qt'de bir bloğa dolgulu
zemin vermenin güvenilir yolu bu; `<pre>` üzerine verilen `background-color`
her sürümde aynı sonucu vermiyor.

İşlenen biçimler:

    ```python ... ```   -> kod bloğu
    `kod`               -> satır içi kod
"""

from __future__ import annotations

import html
import re

from ..resources.theme.tokens import FONTS, PALETTES

FENCE_PATTERN = re.compile(r"```[A-Za-z]*\n(.*?)```", re.DOTALL)
INLINE_PATTERN = re.compile(r"`([^`\n]+)`")

# Yazı tipi listesi çift tırnak taşıyor; `style="..."` özniteliğinin içine
# olduğu gibi konursa özniteliği ortasından kapatıyor.
MONO = FONTS["mono"].replace('"', "'")

# Kod bloğu yerine geçici olarak konan işaret. Metnin geri kalanı kaçışa
# uğrarken blokların içine dokunulmaması için gerekiyor.
PLACEHOLDER = "\x00BLOK{}\x00"


def has_code(text: str) -> bool:
    """Metinde işlenecek bir kod parçası var mı?"""
    return "`" in text


def render(text: str, mode: str = "light") -> str:
    """Markdown kod işaretlerini Qt zengin metnine çevirir."""
    palette = PALETTES.get(mode, PALETTES["light"])

    blocks: list[str] = []

    def stash(match: re.Match) -> str:
        blocks.append(match.group(1).rstrip("\n"))
        return PLACEHOLDER.format(len(blocks) - 1)

    staged = FENCE_PATTERN.sub(stash, text)

    escaped = html.escape(staged)
    escaped = INLINE_PATTERN.sub(
        lambda m: _inline_html(m.group(1), palette), escaped
    )
    escaped = escaped.replace("\n", "<br>")

    for index, block in enumerate(blocks):
        escaped = escaped.replace(
            PLACEHOLDER.format(index), _block_html(block, palette)
        )

    return escaped


def _inline_html(code: str, palette: dict) -> str:
    """Satır içi kod.

    `code` buraya **zaten kaçışa uğramış** olarak geliyor; metnin tamamı bir
    üstte `html.escape`'ten geçiyor. Burada ikinci kez kaçırılırsa `a > b`
    ekranda `a &gt; b` diye görünüyor.
    """
    return (
        f'<span style="font-family:{MONO}; '
        f'background-color:{palette["code_bg"]}; color:{palette["accent"]};">'
        f"&nbsp;{code}&nbsp;</span>"
    )


def _block_html(code: str, palette: dict) -> str:
    """Kod bloğu. Bu metin kaçışa uğramadan saklandığı için burada kaçırılıyor."""
    return (
        '<table cellpadding="8" cellspacing="0" width="100%" '
        f'style="background-color:{palette["code_bg"]};"><tr><td>'
        f'<pre style="font-family:{MONO}; color:{palette["text"]}; margin:0;">'
        f"{html.escape(code)}"
        "</pre></td></tr></table>"
    )
