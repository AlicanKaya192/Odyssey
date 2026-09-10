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
from app.core.runner import run_code, sql_admin  # noqa: E402
from app.paths import content_dir  # noqa: E402

# İpucundaki kod bloğu. Dil etiketi alıştırmanın diline göre değişiyor
# (`python` / `sql`); ikisi de kabul ediliyor.
KOD_BLOGU = re.compile(r"```(?:python|sql|tsql)\n(.*?)```", re.S)

# Kaç alıştırma aynı anda çalışsın. Her biri bir alt süreç açıp beklerken
# GIL'i bırakıyor, yani iş parçacığı yeterli — süreç havuzuna gerek yok.
# Altıda tutuluyor: daha fazlası hem belleği hem MSSQL bağlantılarını
# zorluyor, kazanç ise düzleşiyor.
ISCI_SAYISI = 6

# Başlangıç kodunda yorum satırının nasıl başladığı.
YORUM_ONEKI = {"python": "#", "tsql": "--"}


def hint_kodu(exercise: Exercise, language: str) -> str | None:
    """Son ipucundaki kod bloğu."""
    if not exercise.hints:
        return None
    match = KOD_BLOGU.search(exercise.hints[-1].get(language, ""))
    return match.group(1) if match else None


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


def bir_alistirma(path: Path) -> list[str]:
    """Tek bir alıştırmayı denetler; bulduğu sorunları döndürür."""
    problems: list[str] = []
    exercise = Exercise.load(path)
    where = f"{path.parts[-4]}/{path.parts[-3]}/{exercise.id}"

    def calistir(kod: str):
        return run_code(
            kod,
            exercise.checks,
            exercise.timeout_sec,
            path,
            language=exercise.language,
            exercise_key=where,
        )

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


def denetle(directories: list[Path]) -> list[str]:
    """Alıştırmaları paralel çalıştırır; sorunları kaynak sırasında verir."""
    isci = min(ISCI_SAYISI, max(1, len(directories)))
    with ThreadPoolExecutor(max_workers=isci) as havuz:
        # `map` sırayı koruyor: rapor her çalıştırmada aynı sırada çıkıyor.
        sonuclar = list(havuz.map(bir_alistirma, directories))

    print(f"{len(directories)} alıştırma çalıştırıldı ({isci} paralel).")
    return [sorun for grup in sonuclar for sorun in grup]


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
    if not directories:
        print(f"Eşleşen alıştırma yok: {pattern}")
        return 1

    # Denetimden önceki liste: sonunda yalnızca bu çalıştırmanın açtıkları
    # siliniyor. SQL alıştırması yoksa sunucuya hiç gidilmiyor.
    sql_var = any(Exercise.load(d).language == "tsql" for d in directories)
    onceki = _veritabanlari() if sql_var else None

    started = time.time()
    try:
        problems = denetle(directories)
    finally:
        if onceki is not None:
            _test_veritabanlarini_sil(onceki)
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
