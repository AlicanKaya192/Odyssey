"""Bitmiş bölüm bitmiş kalır.

Bölümün tamamlanması her seferinde ilerlemeden hesaplanıyor: sınav geçildi
mi, alıştırmaların hepsi çözüldü mü. Bir bölüme sonradan alıştırma
eklenince (0.9.2: Python'un altı bölümü 7 alıştırmaya çıktı) o bölümü
bitirmiş biri bölümünü "yarım kalmış" görüyor, bölüm başına XP'yi ve belki
bir seviyeyi kaybediyordu.

Artık bir bölüm ilk tamamlandığında `section_progress.completed_at`
yazılıyor ve `SectionState.status` o tarihi görünce bölümü tamamlanmış
sayıyor; yeni alıştırmalar o kişiye ek alıştırma olarak kalıyor.

Tarih alanı bu sürümde geldiği için, alıştırma eklenmeden **önce**
bitirilmiş bölümler eski alıştırma listesine göre bir kez işaretleniyor
(`GRANDFATHERED`). Bir bölüme ileride yine alıştırma eklenirse ona gerek
yok: o bölümü bitirmiş olanların tarihi zaten yazılı.
"""

from __future__ import annotations

PY = "00-python-temelleri"

# Eski listeye göre işaretleme yalnızca bir kez (güncellemeden sonraki ilk
# açılışta) yapılıyor; sonra yeni bir kullanıcı eski alıştırmaları çözüp
# yenilerini atlayarak bölümü bitiremesin.
LEGACY_KEY = "completion_legacy_done"

# 0.9.1'deki (yayınlanmış) alıştırma listeleri; `git show setup-0.9.1`.
GRANDFATHERED: dict[tuple[str, str], tuple[str, ...]] = {
    (PY, "00-baslangic"): ("first-program", "print-calculation", "print-together", "receipt-lines"),
    (PY, "01-degiskenler"): ("e1", "format-a-sentence", "text-to-number", "unit-report"),
    (PY, "02-operatorler"): ("division-kinds", "rectangle", "seconds-to-minutes"),
    (PY, "03-kosullar"): ("even-or-odd", "largest-of-three", "letter-grade"),
    (PY, "04-donguler"): ("count-above-limit", "sum-with-loop", "times-table"),
    (PY, "07-sozlukler"): ("count-votes", "dict-lookup", "dict-update"),
}


def stamp(catalog, store) -> int:
    """Tamamlanmış ama tarihi yazılmamış bölümleri işaretler; kaç tane yazıldı.

    İlk çağrıda (ayar yoksa) `GRANDFATHERED` listeleri de deneniyor.
    """
    legacy = store.setting(LEGACY_KEY, "") != "1"
    yazilan = 0
    for chapter in catalog.chapters:
        for section in chapter.sections:
            state = store.section_state(chapter.id, section.id, section.exercises)
            if state.completed_at or not state.has_activity:
                continue
            tamam = state.status(section.requires_quiz, section.requires_exercises) == "completed"
            eski = GRANDFATHERED.get((chapter.id, section.id))
            if not tamam and legacy and eski is not None:
                onceki = store.section_state(chapter.id, section.id, eski)
                tamam = onceki.status(section.requires_quiz, section.requires_exercises) == "completed"
            if tamam:
                store.mark_section_completed(chapter.id, section.id)
                yazilan += 1
    if legacy:
        store.set_setting(LEGACY_KEY, "1")
    return yazilan
