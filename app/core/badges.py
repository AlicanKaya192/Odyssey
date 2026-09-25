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


# Modül kimlikleri (`content/` altındaki klasör adları).
PY_CHAPTER = "00-python-temelleri"
DATA_CHAPTER = "01-veri-bilimi"
ML_CHAPTER = "02-makine-ogrenmesi"
SQL_CHAPTER = "03-sql"

# Tek bir bölüme bağlı rozetler için: (modül kimliği, bölüm kimliği).
#
# Her bölümün rozeti yok. Rozet, o bölümü bitirince **yapabildiğin şeyin
# değiştiği** yerlere konuyor: döngü, fonksiyon, nesne, ilk model, JOIN...
# Bölüm başına rozet verildiğinde duvar elli rozeti geçiyor ve hiçbiri bir
# şey ifade etmiyordu; Alican 16 Eylül'de seyrekleştirmeyi istedi.
PY_LOOP_SECTION = (PY_CHAPTER, "04-donguler")
PY_FUNCTION_SECTION = (PY_CHAPTER, "05-fonksiyonlar")
PY_OOP_SECTION = (PY_CHAPTER, "12-oop")
DATAFRAME_SECTION = (DATA_CHAPTER, "03-dataframe")
CHART_SECTION = (DATA_CHAPTER, "07-gorsellestirme")
FIRST_MODEL_SECTION = (ML_CHAPTER, "01-ilk-model")
VALIDATION_SECTION = (ML_CHAPTER, "05-dogrulama")
PIPELINE_SECTION = (ML_CHAPTER, "11-pipeline-ve-model-kaydetme")
SQL_SELECT_SECTION = (SQL_CHAPTER, "01-select-ve-where")
SQL_JOIN_SECTION = (SQL_CHAPTER, "06-tablolari-birlestirmek")
SQL_WINDOW_SECTION = (SQL_CHAPTER, "11-pencere-fonksiyonlari")

# Patikanın tamamına bağlı rozetler için: modüldeki bölüm sayısı.
PY_SECTION_COUNT = 17
DATA_SECTION_COUNT = 10
ML_SECTION_COUNT = 13
SQL_SECTION_COUNT = 16


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
                chapter.id, section.id, section.exercises
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


def completed_sections(catalog, store) -> set[tuple[str, str]]:
    """Biten bölümlerin `(modül, bölüm)` kimlikleri.

    Ana pencere ilerleme her değiştiğinde bunu bir önceki kümeyle
    karşılaştırıp yeni bitenleri sağ alttaki kartla kutluyor.
    """
    return _completed_sections(catalog, store)[3]


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
        # Notlarım: içinde bir şey yazılı ilk not (boş not sayılmıyor).
        "first-note": store.written_note_count() >= 1,
        # Patikaya bağlı rozetler modül kimliğine bakıyor. Kimlik
        # `content/` altındaki klasör adı; modül yeniden adlandırılırsa
        # burası da değişmeli.
        "python-loops": PY_LOOP_SECTION in bitenler,
        "python-functions": PY_FUNCTION_SECTION in bitenler,
        "python-oop": PY_OOP_SECTION in bitenler,
        "python-complete": modul_basina.get(PY_CHAPTER, 0) >= PY_SECTION_COUNT,
        "two-chapters": len(modul_basina) >= 2,
        "first-table": DATAFRAME_SECTION in bitenler,
        "first-chart": CHART_SECTION in bitenler,
        "data-explorer": modul_basina.get(DATA_CHAPTER, 0) >= DATA_SECTION_COUNT,
        "first-model": FIRST_MODEL_SECTION in bitenler,
        "honest-measure": VALIDATION_SECTION in bitenler,
        "one-object": PIPELINE_SECTION in bitenler,
        "ml-complete": modul_basina.get(ML_CHAPTER, 0) >= ML_SECTION_COUNT,
        "first-filter": SQL_SELECT_SECTION in bitenler,
        "joiner": SQL_JOIN_SECTION in bitenler,
        "window-frame": SQL_WINDOW_SECTION in bitenler,
        "sql-complete": modul_basina.get(SQL_CHAPTER, 0) >= SQL_SECTION_COUNT,
    }


def award_new(catalog, store, path) -> list[dict]:
    """Koşulu sağlanmış ama henüz kaydedilmemiş rozetleri kaydeder.

    Döndürdüğü liste yeni kazanılan rozetlerin tanımları. Kazanım önce
    yalnızca profil ekranı açılınca (`collect`) kaydediliyordu; bildirim de
    bu yüzden ancak profile bakınca düşüyordu — o sırada rozet zaten
    ekrandaydı. Ana pencere bunu ilerleme her değiştiğinde çağırıyor.
    """
    durumlar = evaluate(catalog, store)
    kayitlar = store.earned_badges()
    yeni = []
    for tanim in load_definitions(path):
        rozet_id = tanim.get("id", "")
        if durumlar.get(rozet_id, False) and rozet_id not in kayitlar:
            store.award_badge(rozet_id)
            yeni.append(tanim)
    return yeni


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
