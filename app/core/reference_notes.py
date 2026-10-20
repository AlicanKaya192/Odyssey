"""Hızlı başvuru çekmecesinin içeriği: bölümlerin ders notları.

Yeni içerik yazılmıyor. Bölümlerin çoğunda zaten bir başvuru notu var
("Hızlı Başvuru", "… Başvurusu", "… Kartı", "Komut Kartı"...); hangisi
olduğu not başlığından anlaşılıyor (`REFERENCE_TITLE`). 20 Ekim ölçümü:
notu olan 455 bölümün 362'sinde böyle bir not var; olmayanlarda bölümün
bütün notları sırasıyla gösteriliyor, böylece hiçbir bölüm boş kalmıyor.

Çekmecede başvuru notu öne, bölümün öteki notları arkasından geliyor.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .catalog import Catalog
from .search import fold

_WORDS = re.compile(r"\w+")

# Başvuru türü notun Türkçe başlığında geçen sözcükler (İngilizce başlıklar
# aynı notun çevirisi, ayrıca bakılmıyor).
REFERENCE_TITLE = re.compile(
    r"(başvuru|kartı|rehberi|sözlüğü|kontrol listesi|komutları|kalıpları|tablosu)", re.I)


@dataclass(frozen=True)
class ReferenceEntry:
    """Bir bölümün çekmecedeki kaydı."""

    chapter_id: str
    section_id: str
    chapter_title: dict
    section_title: dict
    directory: Path
    documents: tuple  # not kayıtları (section.json), başvuru notları önde
    has_reference: bool

    @property
    def key(self) -> tuple[str, str]:
        return (self.chapter_id, self.section_id)

    def path_for(self, index: int, language: str) -> Path | None:
        """Notun dosyası; seçili dilde yoksa Türkçesi."""
        if not (0 <= index < len(self.documents)):
            return None
        sablon = self.documents[index].get("file", "")
        if not sablon:
            return None
        istenen = self.directory / sablon.replace("{lang}", language)
        return istenen if istenen.exists() else self.directory / sablon.replace("{lang}", "tr")


def _pick(text: dict, language: str) -> str:
    return str(text.get(language) or text.get("tr") or "") if isinstance(text, dict) else str(text or "")


def build_entries(catalog: Catalog) -> list[ReferenceEntry]:
    """Notu olan her bölüm, katalog sırasıyla."""
    kayitlar = []
    for chapter in catalog.chapters:
        for section in chapter.sections:
            for block in section.blocks_of("notes"):
                notlar = list(block.documents)
                if not notlar:
                    continue
                basvuru = [n for n in notlar if REFERENCE_TITLE.search(_pick(n.get("title"), "tr"))]
                digerleri = [n for n in notlar if n not in basvuru]
                kayitlar.append(ReferenceEntry(
                    chapter.id, section.id, chapter.title, section.title, block.directory,
                    tuple(basvuru + digerleri), bool(basvuru)))
                break
    return kayitlar


def search(entries: list[ReferenceEntry], query: str, language: str,
           limit: int = 40) -> list[ReferenceEntry]:
    """Bölüm adı, not adları ve modül adında arama (Türkçe harfler katlanmış).

    Aranan her kelime bir kelimenin **başında** geçmeli ("git" Git'i bulur,
    "Eğitilmiş"i bulmaz). Önce adında geçen bölümler, sonra notunun adında
    geçenler, en son yalnızca modül adında geçenler.
    """
    kelimeler = _WORDS.findall(fold(query))
    if not kelimeler:
        return []

    def var(metin: list[str]) -> bool:
        return all(any(w.startswith(k) for w in metin) for k in kelimeler)

    puanli = []
    for sira, kayit in enumerate(entries):
        bolum = _WORDS.findall(fold(_pick(kayit.section_title, language)))
        notlar = _WORDS.findall(fold(" ".join(_pick(n.get("title"), language) for n in kayit.documents)))
        modul = _WORDS.findall(fold(_pick(kayit.chapter_title, language)))
        if not var(bolum + notlar + modul):
            continue
        if var(bolum):
            derece = 0
        elif var(bolum + notlar):
            derece = 1
        else:
            derece = 2
        puanli.append((derece, sira, kayit))
    puanli.sort(key=lambda t: (t[0], t[1]))
    return [kayit for _d, _s, kayit in puanli[:limit]]
