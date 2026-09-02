"""Rozetler.

Tanımlar `content/badges.json` içinde (ad ve açıklama iki dilde), koşullar
burada. Ayrım bilinçli: bir rozetin adını değiştirmek içerik işi, ne zaman
kazanıldığını değiştirmek kod işi.

Kazanım **hesaplanıyor, saklanmıyor** — bir rozetin koşulu sağlanıyorsa
kazanılmış sayılıyor. Kazanıldığı tarih ise `badges` tablosunda saklanıyor:
koşul sonradan tekrar sağlansa bile "ilk ne zaman aldın" bilgisi korunuyor.

Böylece rozet listesi büyüdüğünde eski kullanıcılar hak ettikleri rozetleri
kendiliğinden alıyor; geriye dönük bir göç yazmak gerekmiyor.
"""

from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Badge:
    """Bir rozetin tanımı ve kullanıcının durumu."""

    id: str
    icon: str
    title: dict
    description: dict
    earned: bool = False
    earned_at: str = ""


def load_definitions(path) -> list[dict]:
    """`content/badges.json` dosyasını okur."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return json.load(handle).get("badges", [])


# Veri Bilimi modülünün kimliği (`content/` altındaki klasör adı).
DATA_CHAPTER = "01-veri-bilimi"

# Tek bir bölüme bağlı rozetler için: (modül kimliği, bölüm kimliği).
NUMPY_SECTION = (DATA_CHAPTER, "01-numpy")
DATAFRAME_SECTION = (DATA_CHAPTER, "03-dataframe")
CLEANING_SECTION = (DATA_CHAPTER, "06-veri-temizleme")
CHART_SECTION = (DATA_CHAPTER, "07-gorsellestirme")

# Patikanın tamamına bağlı rozet için: modüldeki bölüm sayısı.
DATA_SECTION_COUNT = 10


def _completed_sections(
    catalog, store
) -> tuple[int, int, dict[str, int], set[tuple[str, str]]]:
    """(bölüm, modül, modül başına bölüm, biten bölümlerin kimlikleri).

    Üçüncü değer modül kimliğinden sayıya: hangi modülde kaç bölüm bitmiş.
    Dördüncüsü `(modül, bölüm)` çiftlerinden bir küme — tek bir bölüme
    bağlı rozetler bunu kullanıyor.
    """
    bolum = 0
    modul = 0
    modul_basina: dict[str, int] = {}
    bitenler: set[tuple[str, str]] = set()
    for chapter in catalog.chapters:
        hepsi = True
        for section in chapter.sections:
            state = store.section_state(
                chapter.id, section.id, len(section.exercises)
            )
            if state.status(section.requires_quiz, section.requires_exercises) == "completed":
                bolum += 1
                modul_basina[chapter.id] = modul_basina.get(chapter.id, 0) + 1
                bitenler.add((chapter.id, section.id))
            else:
                hepsi = False
        if hepsi and chapter.sections:
            modul += 1
    return bolum, modul, modul_basina, bitenler


def evaluate(catalog, store) -> dict[str, bool]:
    """Her rozet için koşulun sağlanıp sağlanmadığını döndürür.

    Sorgular bir kez yapılıp paylaşılıyor: her rozet kendi sorgusunu
    çalıştırsaydı profil ekranı her açılışta onlarca kez veritabanına
    giderdi.
    """
    alistirma = store.solved_exercise_count()
    seri = store.streak()
    bolum, modul, modul_basina, bitenler = _completed_sections(catalog, store)
    turler = store.activity_totals()
    en_yogun = store.busiest_day_count()
    en_iyi = store.best_quiz_score()
    gecilen = store.passed_quiz_count()

    return {
        "first-exercise": alistirma >= 1,
        "ten-exercises": alistirma >= 10,
        "fifty-exercises": alistirma >= 50,
        "first-quiz": gecilen >= 1,
        "perfect-quiz": en_iyi is not None and en_iyi >= 100,
        "first-section": bolum >= 1,
        "five-sections": bolum >= 5,
        "module-complete": modul >= 1,
        "streak-3": seri >= 3,
        "streak-7": seri >= 7,
        "busy-day": en_yogun >= 5,
        "reader": turler.get("lesson", 0) >= 10,
        # Patikaya bağlı rozetler modül kimliğine bakıyor. Kimlik
        # `content/` altındaki klasör adı; modül yeniden adlandırılırsa
        # burası da değişmeli.
        "data-start": modul_basina.get(DATA_CHAPTER, 0) >= 1,
        "two-chapters": len(modul_basina) >= 2,
        "first-library": NUMPY_SECTION in bitenler,
        "first-table": DATAFRAME_SECTION in bitenler,
        "data-clean": CLEANING_SECTION in bitenler,
        "first-chart": CHART_SECTION in bitenler,
        "data-explorer": modul_basina.get(DATA_CHAPTER, 0) >= DATA_SECTION_COUNT,
    }


def collect(catalog, store, path) -> list[Badge]:
    """Tanımları durumla birleştirip listeler.

    Yeni kazanılan rozetlerin tarihi bu çağrıda kaydediliyor; profil ekranı
    her açıldığında kontrol edilmiş oluyor.
    """
    durumlar = evaluate(catalog, store)
    kayitlar = store.earned_badges()

    sonuc = []
    for tanim in load_definitions(path):
        rozet_id = tanim.get("id", "")
        kazanildi = durumlar.get(rozet_id, False)
        if kazanildi and rozet_id not in kayitlar:
            store.award_badge(rozet_id)
            kayitlar = store.earned_badges()
        sonuc.append(
            Badge(
                id=rozet_id,
                icon=tanim.get("icon", "●"),
                title=tanim.get("title", {}),
                description=tanim.get("description", {}),
                earned=kazanildi,
                earned_at=kayitlar.get(rozet_id, ""),
            )
        )
    return sonuc
