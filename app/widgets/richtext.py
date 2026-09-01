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

    ```python ... ```   -> kod bloğu (ders anlatımıyla aynı renklendirici)
    `kod`               -> satır içi kod
    **kalın**           -> kalın yazı
"""

from __future__ import annotations

import html
import re

from ..core.highlight import highlight_python
from ..resources.theme.tokens import FONTS, PALETTES

FENCE_PATTERN = re.compile(r"```[A-Za-z]*\n(.*?)```", re.DOTALL)
INLINE_PATTERN = re.compile(r"`([^`\n]+)`")

# `**kalın**`. Ters tırnak dışarıda bırakılıyor: satır içi kodun içindeki
# yıldızlar kalın yazıya dönüşmemeli.
BOLD_PATTERN = re.compile(r"\*\*([^*`\n]+)\*\*")

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

    # Kalın yazı satır içi koddan **önce** işleniyor; sonra işlenseydi
    # kod parçasının HTML'i içindeki yıldızlar da yakalanabilirdi.
    # İşlenmediğinde ekranda `**hem de**` diye ham görünüyordu.
    escaped = BOLD_PATTERN.sub(lambda m: f"<b>{m.group(1)}</b>", escaped)

    escaped = INLINE_PATTERN.sub(
        lambda m: _inline_html(m.group(1), palette), escaped
    )
    escaped = escaped.replace("\n", "<br>")

    for index, block in enumerate(blocks):
        escaped = escaped.replace(
            PLACEHOLDER.format(index), _block_html(block, palette, mode)
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


def _block_html(code: str, palette: dict, mode: str) -> str:
    """Kod bloğu.

    Kod, ders anlatımındaki bloklarla **aynı renklendiriciden** geçiyor
    (`highlight_python`). Önceden tek renk düz metin olarak basılıyordu;
    yeni başlayan biri için `if`, sayı, metin ve fonksiyon adı aynı renkte
    olunca kod bir harf yığınına dönüşüyordu. Sınavda gösterilen kod, aynı
    kodu bir editörde açtığında ne görecekse ona benzemeli.

    Renklendirici satır içi `style` üretiyor; Qt'nin zengin metni CSS'in
    yalnızca bu kadarını tanıyor, sınıf tabanlı bir stil çalışmazdı.
    """
    return (
        '<table cellpadding="8" cellspacing="0" width="100%" '
        f'style="background-color:{palette["code_bg"]};"><tr><td>'
        f'<pre style="font-family:{MONO}; color:{palette["text"]}; margin:0;">'
        f"{highlight_python(code, mode)}"
        "</pre></td></tr></table>"
    )
