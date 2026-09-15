"""Notlarım: notun çizimi ve adlandırma kuralları.

Arayüzden bağımsız, düz fonksiyonlar; `ui/notebook_view.py` kullanıyor.

**Not metni güvenilir içerik sayılmıyor.** Ders metinleri bizim yazdığımız
dosyalar ve ders okuyucusu içlerindeki HTML'i olduğu gibi çiziyor (figürler
bu sayede çalışıyor). Not ise kullanıcının yazdığı ya da başka birinden
aldığı bir metin; aynı yoldan çizilseydi içine konan bir `<script>` belge
alanında çalışır, `![](http://...)` bir sunucuya istek atar, `file:`
bağlantısı belge alanında yerel bir dosya açardı. Bu yüzden notlar ayrı,
daha dar bir markdown ile çiziliyor:

- ham HTML **metin olarak** gösteriliyor, çalışmıyor;
- görsel çizilmiyor (uzaktan hiçbir şey yüklenmiyor);
- bağlantılardan yalnızca `http` ve `https` kalıyor; onlar da tıklanınca
  uygulamada değil sistem tarayıcısında açılıyor (`DocumentView`).
"""

from __future__ import annotations

import html
from urllib.parse import urlsplit

import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

# Notun adının en fazla uzunluğu. Ağaçta ve dosya adında taşmasın diye.
TITLE_MAX_LENGTH = 80

SAFE_LINK_SCHEMES = ("http", "https")

NOTE_EXTENSIONS = ["fenced_code", "tables", "sane_lists"]


def unique_title(title: str, taken: set[str]) -> str:
    """`taken` içinde olmayan bir ad: "Ad", sonra "Ad (2)", "Ad (3)"...

    `taken` küçük harfe indirilmiş (`casefold`) adlar; "Döngüler" ile
    "döngüler" aynı sayılıyor, ağaçta ikisi yan yana karışıyor.
    """
    base = " ".join(title.split())[:TITLE_MAX_LENGTH]
    if base.casefold() not in taken:
        return base

    number = 2
    while True:
        suffix = f" ({number})"
        candidate = base[: TITLE_MAX_LENGTH - len(suffix)] + suffix
        if candidate.casefold() not in taken:
            return candidate
        number += 1


class _SafeLinks(Treeprocessor):
    """`http`/`https` dışındaki bağlantıların adresini siler; metni kalır."""

    def run(self, root):
        for element in root.iter("a"):
            href = element.get("href", "")
            if urlsplit(href).scheme.lower() not in SAFE_LINK_SCHEMES:
                element.attrib.pop("href", None)
        return root


class _NoteMarkdown(Extension):
    """Ham HTML'i, görselleri ve güvensiz bağlantıları kapatır."""

    def extendMarkdown(self, md):  # noqa: N802 (kütüphanenin adlandırması)
        # HTML bloğu ve satır içi HTML: kapatılınca metin olarak kaçışlı
        # çıkıyor, çalışmıyor.
        md.preprocessors.deregister("html_block")
        md.inlinePatterns.deregister("html")
        for name in ("image_link", "image_reference", "short_image_ref"):
            if name in md.inlinePatterns:
                md.inlinePatterns.deregister(name)
        md.treeprocessors.register(_SafeLinks(md), "odyssey_safe_links", 0)


def render_body(text: str) -> str:
    """Not gövdesini güvenli HTML'e çevirir."""
    converter = markdown.Markdown(extensions=[*NOTE_EXTENSIONS, _NoteMarkdown()])
    return converter.convert(text)


def render_note(title: str, body: str, meta: list[str]) -> str:
    """Okuma hâlindeki notun içeriği: başlık, bilgi satırı, gövde.

    Başlık markdown'dan geçmiyor, kaçışlanıp doğrudan yazılıyor: adında
    `*` ya da `#` olan bir not başka bir şeye dönüşmesin.
    """
    parts = [f"<h1>{html.escape(title)}</h1>"]
    if meta:
        parts.append(
            '<div class="meta">'
            + "".join(f"<span>{html.escape(item)}</span>" for item in meta)
            + "</div>"
        )
    parts.append(render_body(body))
    return "".join(parts)
