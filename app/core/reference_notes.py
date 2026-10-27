"""Bölümün başvuru notu: hızlı başvuru kartı boşken gösterilen bağlantı.

Bölümlerin çoğunda zaten bir başvuru notu var ("Hızlı Başvuru", "…
Başvurusu", "… Kartı", "Komut Kartı"...); hangisi olduğu not başlığından
anlaşılıyor (`REFERENCE_TITLE`). 20 Ekim ölçümü: notu olan 455 bölümün
362'sinde böyle bir not var.

Notun kendisi çekmecede açılmıyor (27 Ekim, Alican): çekmece kişinin kendi
kartı; bağlantı notu bölümün Ders Notu sekmesinde açıyor.
"""

from __future__ import annotations

import re

from .catalog import Section

# Başvuru türü notun Türkçe başlığında geçen sözcükler (İngilizce başlıklar
# aynı notun çevirisi, ayrıca bakılmıyor).
REFERENCE_TITLE = re.compile(
    r"(başvuru|kartı|rehberi|sözlüğü|kontrol listesi|komutları|kalıpları|tablosu)", re.I)


def reference_note(section: Section) -> tuple[int, dict] | None:
    """Bölümün ilk başvuru notu: (Ders Notu sekmesindeki sırası, not kaydı).

    Sekme son not bloğunu gösteriyor (`TopicView._quiz_notes`); sıra oradan.
    """
    bloklar = [blok for blok in section.blocks_of("notes") if blok.documents]
    if not bloklar:
        return None
    for sira, belge in enumerate(bloklar[-1].documents):
        baslik = belge.get("title")
        tr = str(baslik.get("tr", "")) if isinstance(baslik, dict) else str(baslik or "")
        if REFERENCE_TITLE.search(tr):
            return sira, belge
    return None
