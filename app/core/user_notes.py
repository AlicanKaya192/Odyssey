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
import io
import re
import zipfile
import zlib
from pathlib import Path, PurePosixPath
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


# --- indirme ve yükleme ------------------------------------------------------
#
# Bir not tek başına `.md` dosyası olarak iniyor; başında küçük bir bilgi
# bloğu var:
#
#     ---
#     odyssey-note: 1
#     title: Döngüler özetim
#     chapter: 00-python-temelleri
#     section: 03-kosul-durumlari
#     ---
#
# Dosya her markdown okuyucusunda düzgün görünüyor (blok başlık bilgisi
# sayılıyor) ve Odyssey'e yüklenince kendi klasörüne, dersine yerleşiyor.
# Klasör ya da bütün notlar `.zip` içinde, klasör başına bir dizin.
#
# **Yüklenen dosya başkasından geliyor.** Zip diske açılmıyor, bellekte
# okunuyor (yol hilesi olmuyor); not başına ve toplamda boyut, dosya
# sayısı sınırı var (zip bombası). Kimlikler bir kalıba uymazsa atılıyor,
# not "Diğer" klasörüne düşüyor. Bilgi bloğu olmayan düz bir markdown da
# kabul: adı dosyanın adı.

FRONT_MATTER = "---"
FORMAT_KEY = "odyssey-note"
FORMAT_VERSION = "1"

# Bir notun en fazla boyutu; ders notlarının en uzunu 30 KB civarında.
MAX_NOTE_BYTES = 1_000_000
# Tek yüklemede en fazla not ve toplam boyut.
MAX_IMPORT_NOTES = 500
MAX_IMPORT_BYTES = 20_000_000

ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,99}$")
_UNSAFE_NAME = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_RESERVED_NAMES = {
    "con", "prn", "aux", "nul",
    *(f"com{i}" for i in range(1, 10)),
    *(f"lpt{i}" for i in range(1, 10)),
}

# Zip içindeki tek bir dosyanın okunamamasına yol açabilecek hatalar:
# şifreli dosya, desteklenmeyen sıkıştırma, bozuk veri.
_ENTRY_ERRORS = (RuntimeError, NotImplementedError, zipfile.BadZipFile, OSError, EOFError, zlib.error)


def note_to_markdown(entry: dict) -> str:
    """Notu bilgi bloğuyla birlikte `.md` metnine çevirir."""
    head = [
        FRONT_MATTER,
        f"{FORMAT_KEY}: {FORMAT_VERSION}",
        f"title: {entry['title']}",
        f"chapter: {entry['chapter_id']}",
    ]
    if entry.get("section_id"):
        head.append(f"section: {entry['section_id']}")
    head.append(FRONT_MATTER)
    return "\n".join(head) + "\n\n" + entry.get("body", "").rstrip() + "\n"


def parse_note(text: str, fallback_title: str, default_title: str) -> dict:
    """`.md` metninden not: (chapter_id, section_id, title, body).

    Bilgi bloğu yoksa ya da bizim değilse (başka bir aracın başlık
    bilgisi) klasör ve ders boş kalıyor; ad blokta varsa oradan, yoksa
    dosya adından, o da yoksa `default_title`.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("﻿")
    meta: dict[str, str] = {}
    body = text

    acilis = FRONT_MATTER + "\n"
    kapanis = "\n" + FRONT_MATTER
    if text.startswith(acilis):
        son = text.find(kapanis + "\n", len(FRONT_MATTER))
        if son != -1:
            govde_basi = son + len(kapanis) + 1
        elif text.endswith(kapanis):
            son = len(text) - len(kapanis)
            govde_basi = len(text)
        else:
            son = -1
        if son != -1:
            for line in text[len(acilis):son].split("\n"):
                key, sep, value = line.partition(":")
                if sep:
                    meta[key.strip().lower()] = value.strip()
            body = text[govde_basi:]

    bizim = FORMAT_KEY in meta
    chapter = meta.get("chapter", "") if bizim else ""
    section = meta.get("section", "") if bizim else ""
    if not ID_PATTERN.match(chapter):
        chapter = ""
    if not chapter or not ID_PATTERN.match(section):
        section = ""

    title = ""
    for aday in (meta.get("title", ""), fallback_title, default_title):
        title = " ".join(aday.split())[:TITLE_MAX_LENGTH]
        if title:
            break
    return {"chapter_id": chapter, "section_id": section, "title": title, "body": body.strip("\n")}


def safe_filename(name: str, fallback: str = "not") -> str:
    """Windows'ta da geçerli bir dosya adı: yasak işaretler `_`, sonda nokta yok."""
    cleaned = _UNSAFE_NAME.sub("_", name).strip().rstrip(". ")[:TITLE_MAX_LENGTH]
    cleaned = cleaned or fallback
    if cleaned.split(".")[0].lower() in _RESERVED_NAMES:
        cleaned = "_" + cleaned
    return cleaned


def build_zip(groups: list[tuple[str, list[dict]]]) -> bytes:
    """(klasör adı, notlar) gruplarından zip. Adlar zip içinde tekil."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for folder_name, entries in groups:
            folder = safe_filename(folder_name, "notlar")
            used: set[str] = set()
            for entry in entries:
                base = safe_filename(entry["title"])
                name = base
                number = 2
                while name.casefold() in used:
                    name = f"{base} ({number})"
                    number += 1
                used.add(name.casefold())
                # Zip içinde yol ayracı her zaman düz eğik çizgi.
                archive.writestr(f"{folder}/{name}.md", note_to_markdown(entry))
    return buffer.getvalue()


def read_notes_file(path: Path, default_title: str) -> tuple[list[dict], int]:
    """Yüklenen `.md` ya da `.zip` dosyasındaki notlar ve okunamayan dosya sayısı.

    Dosyanın kendisi açılamıyorsa (bozuk zip, desteklenmeyen uzantı)
    istisna yükseliyor: `OSError`, `zipfile.BadZipFile` ya da `ValueError`.
    """
    suffix = path.suffix.lower()
    if suffix == ".md":
        if path.stat().st_size > MAX_NOTE_BYTES:
            return [], 1
        try:
            text = path.read_bytes().decode("utf-8-sig")
        except UnicodeDecodeError:
            return [], 1
        return [parse_note(text, path.stem, default_title)], 0

    if suffix != ".zip":
        raise ValueError(f"desteklenmeyen dosya: {path.suffix}")

    notes: list[dict] = []
    problems = 0
    total = 0
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            if info.is_dir() or not info.filename.lower().endswith(".md"):
                continue
            if len(notes) >= MAX_IMPORT_NOTES or total > MAX_IMPORT_BYTES:
                problems += 1
                continue
            try:
                # Başlıktaki boyut yalan söyleyebilir: en fazla sınırın bir
                # bayt fazlası okunuyor.
                with archive.open(info) as handle:
                    data = handle.read(MAX_NOTE_BYTES + 1)
            except _ENTRY_ERRORS:
                problems += 1
                continue
            if len(data) > MAX_NOTE_BYTES:
                problems += 1
                continue
            total += len(data)
            try:
                text = data.decode("utf-8-sig")
            except UnicodeDecodeError:
                problems += 1
                continue
            notes.append(parse_note(text, PurePosixPath(info.filename).stem, default_title))
    return notes, problems
