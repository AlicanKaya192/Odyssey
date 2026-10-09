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
    # Madalyanın şekli ve kademesi (badges.json → medal), ör. ("hex", "gold").
    medal: tuple = ("circle", "bronze")


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
TS_CHAPTER = "06-zaman-serileri"
API_CHAPTER = "07-api-kullanmak"
API2_CHAPTER = "08-api-yazmak"
DOCKER_CHAPTER = "09-docker"
GIT_CHAPTER = "10-git"
BIGDATA_CHAPTER = "11-buyuk-veri"
ALG1_CHAPTER = "12-temel-algoritmalar"
ALG2_CHAPTER = "13-algoritma-teknikleri"
ALG3_CHAPTER = "14-ml-algoritmalari"

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
TS_DECOMPOSE_SECTION = (TS_CHAPTER, "10-bilesenler-ve-ayristirma")
TS_FORECAST_SECTION = (TS_CHAPTER, "14-temel-tahminler")
API_REQUEST_SECTION = (API_CHAPTER, "06-requests-ile-ilk-istek")
API_PIPELINE_SECTION = (API_CHAPTER, "15-apiden-veri-setine")
API2_ENDPOINT_SECTION = (API2_CHAPTER, "00-api-yazmaya-giris")
API2_CRUD_SECTION = (API2_CHAPTER, "07-crud")
API2_MODEL_SECTION = (API2_CHAPTER, "16-model-sunmak")
DOCKER_IMAGE_SECTION = (DOCKER_CHAPTER, "04-ilk-dockerfile")
DOCKER_COMPOSE_SECTION = (DOCKER_CHAPTER, "10-compose")
GIT_COMMIT_SECTION = (GIT_CHAPTER, "02-ilk-commit")
GIT_MERGE_SECTION = (GIT_CHAPTER, "07-birlestirmek")
GIT_PUSH_SECTION = (GIT_CHAPTER, "09-uzak-depolar")
BIGDATA_PARQUET_SECTION = (BIGDATA_CHAPTER, "05-parquet")
BIGDATA_DUCKDB_SECTION = (BIGDATA_CHAPTER, "07-duckdb")
BIGDATA_SPARK_SECTION = (BIGDATA_CHAPTER, "13-spark")
ALG1_BIG_O_SECTION = (ALG1_CHAPTER, "01-karmasiklik")
ALG1_SORT_SECTION = (ALG1_CHAPTER, "06-verimli-siralamalar")
ALG1_TREE_SECTION = (ALG1_CHAPTER, "13-agaclar")
ALG2_DP_SECTION = (ALG2_CHAPTER, "03-dinamik-programlama-1")
ALG2_PATH_SECTION = (ALG2_CHAPTER, "07-en-kisa-yol")
ALG2_SKETCH_SECTION = (ALG2_CHAPTER, "13-olasiliksal-veri-yapilari")
ALG3_DESCENT_SECTION = (ALG3_CHAPTER, "04-gradyan-inisi")
ALG3_KMEANS_SECTION = (ALG3_CHAPTER, "14-k-means")
ALG3_NETWORK_SECTION = (ALG3_CHAPTER, "20-sinir-agi")

# Patikanın tamamına bağlı rozetler için: modüldeki bölüm sayısı.
PY_SECTION_COUNT = 19
DATA_SECTION_COUNT = 10
ML_SECTION_COUNT = 13
SQL_SECTION_COUNT = 16
TS_SECTION_COUNT = 23
API_SECTION_COUNT = 17
API2_SECTION_COUNT = 18
DOCKER_SECTION_COUNT = 17
GIT_SECTION_COUNT = 17
BIGDATA_SECTION_COUNT = 17
ALG1_SECTION_COUNT = 17
ALG2_SECTION_COUNT = 17
ALG3_SECTION_COUNT = 23


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
        "season-reader": TS_DECOMPOSE_SECTION in bitenler,
        "first-forecast": TS_FORECAST_SECTION in bitenler,
        "ts-complete": modul_basina.get(TS_CHAPTER, 0) >= TS_SECTION_COUNT,
        "first-request": API_REQUEST_SECTION in bitenler,
        "data-pipeline": API_PIPELINE_SECTION in bitenler,
        "api-complete": modul_basina.get(API_CHAPTER, 0) >= API_SECTION_COUNT,
        "first-endpoint": API2_ENDPOINT_SECTION in bitenler,
        "full-resource": API2_CRUD_SECTION in bitenler,
        "model-server": API2_MODEL_SECTION in bitenler,
        "api2-complete": modul_basina.get(API2_CHAPTER, 0) >= API2_SECTION_COUNT,
        "first-image": DOCKER_IMAGE_SECTION in bitenler,
        "conductor": DOCKER_COMPOSE_SECTION in bitenler,
        "docker-complete": modul_basina.get(DOCKER_CHAPTER, 0) >= DOCKER_SECTION_COUNT,
        "first-commit": GIT_COMMIT_SECTION in bitenler,
        "branch-weaver": GIT_MERGE_SECTION in bitenler,
        "first-push": GIT_PUSH_SECTION in bitenler,
        "git-complete": modul_basina.get(GIT_CHAPTER, 0) >= GIT_SECTION_COUNT,
        "columnar": BIGDATA_PARQUET_SECTION in bitenler,
        "file-query": BIGDATA_DUCKDB_SECTION in bitenler,
        "first-spark": BIGDATA_SPARK_SECTION in bitenler,
        "bigdata-complete": modul_basina.get(BIGDATA_CHAPTER, 0) >= BIGDATA_SECTION_COUNT,
        "big-o": ALG1_BIG_O_SECTION in bitenler,
        "divide-conquer": ALG1_SORT_SECTION in bitenler,
        "root-to-leaf": ALG1_TREE_SECTION in bitenler,
        "alg1-complete": modul_basina.get(ALG1_CHAPTER, 0) >= ALG1_SECTION_COUNT,
        "memo-table": ALG2_DP_SECTION in bitenler,
        "pathfinder": ALG2_PATH_SECTION in bitenler,
        "small-memory": ALG2_SKETCH_SECTION in bitenler,
        "alg2-complete": modul_basina.get(ALG2_CHAPTER, 0) >= ALG2_SECTION_COUNT,
        "downhill": ALG3_DESCENT_SECTION in bitenler,
        "centroid-finder": ALG3_KMEANS_SECTION in bitenler,
        "first-network": ALG3_NETWORK_SECTION in bitenler,
        "alg3-complete": modul_basina.get(ALG3_CHAPTER, 0) >= ALG3_SECTION_COUNT,
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
                # Kazanılmış rozet geri alınmaz: patikaya bölüm eklenince
                # koşul yeniden sağlanana kadar kaybolurdu.
                earned=kazanildi or rozet_id in kayitlar,
                earned_at=kayitlar.get(rozet_id, ""),
                medal=tuple((tanim.get("medal") or ["circle", "bronze"])[:2]),
            )
        )
    return sonuc
