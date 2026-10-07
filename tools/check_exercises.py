"""Bütün alıştırmaları gerçekten çalıştırarak denetler.

`validate_content.py` şemaya bakıyor: dosya var mı, çeviri tam mı, kod ASCII
mi. Bu araç ise kodu **çalıştırıyor** ve iki soruyu cevaplıyor:

1. `solution` alıştırmanın kontrollerinden geçiyor mu?
2. **Son ipucu** alıştırmayı gerçekten çözüyor mu?

İkincisi gözden kaçmaya çok müsait. Arayüz son kademeyi "Çözümün tamamı"
diye etiketliyor; oraya kadar gelen kişi tıkanmış demektir ve elinde
çalışan bir kod görmesi gerekiyor. Bir alıştırma yazarken ipucuna sonradan
eklenen bir satır ya da başlangıç kodunda değişen bir şey bu sözü sessizce
bozabiliyor.

Ölçüt şu: ipucundaki kod **tek başına** ya da **başlangıç kodunun üstüne
eklendiğinde** alıştırmayı geçirmeli. İki yol da kabul, çünkü iki farklı
alıştırma biçimi var: başlangıçta hazır veri duruyorsa ipucu onu
tekrarlamıyor (birleştirme geçer), başlangıçtaki kod değiştirilecekse ipucu
tam çözümü veriyor (tek başına geçer).

Python ve T-SQL alıştırmalarının ikisi de aynı yoldan geçiyor; fark
`exercise.json` içindeki `language` alanında ve çalıştırıcı onu kendisi
seçiyor.

Çok dosyalı alıştırmada (`files`) son ipucu her dosyayı kendi adıyla
veriyor: kod bloğunun hemen üstünde kalın yazılmış dosya adı
(`**models.py**`). İpucundaki dosyalar başlangıç dosyalarının yerine
konuyor; ipucunda olmayan dosya başlangıçtaki hâliyle kalıyor.

Kullanım:

    python tools/check_exercises.py            # hepsi
    python tools/check_exercises.py 02-makine-ogrenmesi
    python tools/check_exercises.py 02-makine-ogrenmesi 05-dogrulama

SQL alıştırmaları çalışırken her biri sunucuda kendi veritabanını açıyor
(yaklaşık 16 MB). Denetim bitince **kendi açtıklarını siliyor**: başlamadan
önce listeyi alıyor, sonunda farkı düşürüyor. Uygulamayı kullanırken
açılmış veritabanlarına dokunmuyor — aynı adla zaten varsa denetim onu
kullanıyor ama silmiyor.
"""

from __future__ import annotations

import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.catalog import Exercise  # noqa: E402
from app.core import docker_admin  # noqa: E402
from app.core.git_checks import build_world, evaluate, hint_commands  # noqa: E402
from app.core.runner import run_code, sql_admin  # noqa: E402
from app.paths import content_dir  # noqa: E402

LANGUAGES = ("tr", "en")

# İpucundaki kod bloğu. Dil etiketi alıştırmanın diline göre değişiyor
# (`python` / `sql`); ikisi de kabul ediliyor.
KOD_BLOGU = re.compile(r"```(?:python|sql|tsql|dockerfile)\n(.*?)```", re.S)
# Çok dosyalı ipucu: `**models.py**` (ya da **`models.py`**) ve altındaki blok.
DOSYA_BLOGU = re.compile(r"\*\*`?([\w./-]+)`?\*\*[ \t]*\n+```[\w-]*\n(.*?)```", re.S)

# Kaç alıştırma aynı anda çalışsın. Her biri bir alt süreç açıp beklerken
# GIL'i bırakıyor, yani iş parçacığı yeterli — süreç havuzuna gerek yok.
# Altıda tutuluyor: daha fazlası hem belleği hem MSSQL bağlantılarını
# zorluyor, kazanç ise düzleşiyor.
ISCI_SAYISI = 6

# Başlangıç kodunda yorum satırının nasıl başladığı.
YORUM_ONEKI = {"python": "#", "tsql": "--", "docker": "#"}


def hint_kodu(exercise: Exercise, language: str) -> str | None:
    """Son ipucundaki kod bloğu."""
    if not exercise.hints:
        return None
    match = KOD_BLOGU.search(exercise.hints[-1].get(language, ""))
    return match.group(1) if match else None


def hint_dosyalari(exercise: Exercise, language: str) -> dict[str, str] | None:
    """Çok dosyalı alıştırmanın son ipucu: başlangıç dosyaları + ipucundakiler."""
    if not exercise.hints:
        return None
    bloklar = DOSYA_BLOGU.findall(exercise.hints[-1].get(language, ""))
    if not bloklar:
        return None
    dosyalar = exercise.starter_files(language)
    for ad, kod in bloklar:
        dosyalar[ad] = kod
    return dosyalar


def starter_kodu(exercise: Exercise, language: str) -> str:
    """Başlangıç kodunun yorum olmayan satırları.

    Kullanıcı bunları silmiyor; ipucu bunların üstüne yazılıyor. Yorum
    işareti dile göre değişiyor: Python'da `#`, T-SQL'de `--`.
    """
    onek = YORUM_ONEKI.get(exercise.language, "#")
    lines = exercise.starter_code_for(language).splitlines()
    return "\n".join(
        l for l in lines if l.strip() and not l.strip().startswith(onek)
    )


def _terminal(exercise: Exercise, where: str) -> list[str]:
    """Git terminal alıştırması: benzeticide başlangıç geçmemeli, çözüm
    komutları ve son ipucunun komutları iki dilde de geçmeli."""
    problems: list[str] = []
    for language in LANGUAGES:
        world = build_world(exercise, language)
        if all(r["passed"] for r in evaluate(world, exercise.checks)):
            problems.append(f"{where}: başlangıç durumu ({language}) zaten geçiyor")
        # `allow_fail`: çözümün bilerek hata gösteren adımları (sıra numarası).
        izinli = set(exercise.raw.get("allow_fail", []))
        for i, line in enumerate(exercise.solution_commands):
            _, code = world.run(line)
            if code not in (0, 1) and i not in izinli:
                problems.append(f"{where}: çözüm komutu ({language}) {code} ile bitti: {line}")
        dusen = [r for r in evaluate(world, exercise.checks) if not r["passed"]]
        if dusen:
            problems.append(f"{where}: çözüm ({language}) geçmiyor: {dusen[0]['detail']}")
        komutlar = hint_commands(exercise.hints[-1].get(language, "")) if exercise.hints else []
        if not komutlar:
            problems.append(f"{where}: son ipucunda ({language}) bash bloğu yok")
            continue
        world = build_world(exercise, language)
        for line in komutlar:
            world.run(line)
        dusen = [r for r in evaluate(world, exercise.checks) if not r["passed"]]
        if dusen:
            problems.append(f"{where}: son ipucu ({language}) alıştırmayı çözmüyor: {dusen[0]['detail']}")
    return problems


def bir_alistirma(path: Path) -> list[str]:
    """Tek bir alıştırmayı denetler; bulduğu sorunları döndürür."""
    problems: list[str] = []
    exercise = Exercise.load(path)
    where = f"{path.parts[-4]}/{path.parts[-3]}/{exercise.id}"
    if exercise.is_terminal:
        return _terminal(exercise, where)

    def calistir(kod: str | dict):
        return run_code(
            kod,
            exercise.checks,
            exercise.timeout_sec,
            path,
            language=exercise.language,
            exercise_key=where,
            entry=exercise.entry,
        )

    if exercise.is_multi_file:
        return problems + _cok_dosya(exercise, where, calistir)

    result = calistir(exercise.solution_code)
    if not result.passed:
        problems.append(f"{where}: çözüm geçmiyor ({result.status})")

    for language in ("tr", "en"):
        code = hint_kodu(exercise, language)
        if code is None:
            problems.append(f"{where}: son ipucunda ({language}) kod bloğu yok")
            continue
        if language != "tr":
            # Kod iki dilde aynı olmak zorunda değil ama ikisi de
            # çalışmalı; TR'yi zaten çalıştırdık, EN farklıysa onu da.
            if code == hint_kodu(exercise, "tr"):
                continue
        # İki yol da kabul: ipucu tek başına yeterli olabilir ya da
        # başlangıçtaki hazır kodun üstüne eklenerek çalışabilir.
        alone = calistir(code)
        if alone.passed:
            continue
        merged = starter_kodu(exercise, language) + "\n" + code
        hint_result = calistir(merged)
        if not hint_result.passed:
            problems.append(
                f"{where}: son ipucu ({language}) alıştırmayı çözmüyor "
                f"(tek başına {alone.status}, birleşik {hint_result.status})"
            )

    return problems


def _cok_dosya(exercise: Exercise, where: str, calistir) -> list[str]:
    """Çok dosyalı alıştırma: iki dilde çözüm, iki dilde son ipucu; başlangıç geçmemeli."""
    problems: list[str] = []
    for language in ("tr", "en"):
        result = calistir(exercise.solution_files(language))
        if not result.passed:
            problems.append(f"{where}: çözüm ({language}) geçmiyor ({result.status}) {result.error or ''}")
        dosyalar = hint_dosyalari(exercise, language)
        if dosyalar is None:
            problems.append(f"{where}: son ipucunda ({language}) dosya adlı kod bloğu yok")
            continue
        hint_result = calistir(dosyalar)
        if not hint_result.passed:
            problems.append(f"{where}: son ipucu ({language}) alıştırmayı çözmüyor ({hint_result.status})")
    if calistir(exercise.starter_files("tr")).passed:
        problems.append(f"{where}: başlangıç dosyaları alıştırmayı zaten geçiyor")
    return problems


def denetle(directories: list[Path]) -> list[str]:
    """Alıştırmaları paralel çalıştırır; sorunları kaynak sırasında verir.

    Docker alıştırmaları sırayla: compose dosyaları ana makinede sabit port
    açıyor (`8080:8000`), aynı anda iki tanesi aynı portu isteyince biri
    düşerdi.
    """
    docker = [d for d in directories if Exercise.load(d).language == "docker"]
    diger = [d for d in directories if d not in docker]
    sonuc_haritasi: dict[Path, list[str]] = {}
    isci = min(ISCI_SAYISI, max(1, len(diger)))
    if diger:
        with ThreadPoolExecutor(max_workers=isci) as havuz:
            sonuc_haritasi.update(zip(diger, havuz.map(bir_alistirma, diger)))
    for directory in docker:
        sonuc_haritasi[directory] = bir_alistirma(directory)

    print(f"{len(directories)} alıştırma çalıştırıldı ({isci} paralel"
          + (f", {len(docker)} Docker alıştırması sırayla" if docker else "") + ").")
    # Rapor her çalıştırmada aynı sırada (kaynak sırası).
    return [sorun for directory in directories for sorun in sonuc_haritasi[directory]]


def _veritabanlari() -> set[str] | None:
    """Sunucudaki alıştırma veritabanlarının adları; sunucu yoksa `None`."""
    sonuc = sql_admin("list_databases")
    if sonuc.get("status") != "ok":
        return None
    return {v["name"] for v in sonuc.get("databases", [])}


def _test_veritabanlarini_sil(onceki: set[str]) -> None:
    """Bu çalıştırmanın açtığı veritabanlarını siler.

    Ayarlar penceresinin kullandığı yoldan geçiyor (`sql_admin`), yani
    yalnızca `Odyssey_` önekli adlar silinebiliyor.
    """
    simdiki = _veritabanlari()
    if simdiki is None:
        return
    yeni = sorted(simdiki - onceki)
    if not yeni:
        return
    sonuc = sql_admin("drop_databases", yeni)
    print(f"Denetimin açtığı {len(sonuc.get('dropped', []))} veritabanı silindi.")
    for hata in sonuc.get("errors", []):
        print(f"  silinemedi: {hata.get('name')}: {hata.get('message')}")


def main() -> int:
    root = content_dir()
    if len(sys.argv) > 2:
        pattern = f"{sys.argv[1]}/{sys.argv[2]}/exercises/*/exercise.json"
    elif len(sys.argv) > 1:
        pattern = f"{sys.argv[1]}/*/exercises/*/exercise.json"
    else:
        pattern = "*/*/exercises/*/exercise.json"

    directories = sorted(p.parent for p in root.glob(pattern))
    # Matematik problemlerinde çalıştırılacak kod yok; cevapları
    # `validate_content.py` denetliyor.
    directories = [d for d in directories if not Exercise.load(d).is_problem]
    if not directories:
        print(f"Eşleşen alıştırma yok: {pattern}")
        return 1

    # Denetimden önceki liste: sonunda yalnızca bu çalıştırmanın açtıkları
    # siliniyor. SQL alıştırması yoksa sunucuya hiç gidilmiyor.
    sql_var = any(Exercise.load(d).language == "tsql" for d in directories)
    onceki = _veritabanlari() if sql_var else None

    started = time.time()
    docker_var = any(Exercise.load(d).language == "docker" for d in directories)
    try:
        problems = denetle(directories)
    finally:
        if onceki is not None:
            _test_veritabanlarini_sil(onceki)
        if docker_var:
            # Denetimin kurduğu imajlar (yalnızca `odyssey=1` etiketliler).
            print(f"Denetimin kurduğu {docker_admin.remove_images()} Docker imajı silindi.")
    elapsed = time.time() - started

    print("-" * 66)
    if problems:
        print(f"{len(problems)} sorun bulundu ({elapsed:.0f} sn):")
        for problem in problems:
            print(f"  {problem}")
        return 1

    print(f"Sorun yok ({elapsed:.0f} sn).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
