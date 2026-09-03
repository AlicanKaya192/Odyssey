"""Bütün alıştırmaları gerçekten çalıştırarak denetler.

`validate_content.py` şemaya bakıyor: dosya var mı, çeviri tam mı, kod ASCII
mi. Bu araç ise kodu **çalıştırıyor** ve iki soruyu cevaplıyor:

1. `solution.py` alıştırmanın kontrollerinden geçiyor mu?
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

Kullanım:

    python tools/check_exercises.py            # hepsi
    python tools/check_exercises.py 02-makine-ogrenmesi
    python tools/check_exercises.py 02-makine-ogrenmesi 05-dogrulama
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.catalog import Exercise
from app.core.runner import run_code
from app.paths import content_dir

KOD_BLOGU = re.compile(r"```python\n(.*?)```", re.S)


def hint_kodu(exercise: Exercise, language: str) -> str | None:
    """Son ipucundaki kod bloğu."""
    if not exercise.hints:
        return None
    match = KOD_BLOGU.search(exercise.hints[-1].get(language, ""))
    return match.group(1) if match else None


def starter_kodu(exercise: Exercise, language: str) -> str:
    """Başlangıç kodunun yorum olmayan satırları.

    Kullanıcı bunları silmiyor; ipucu bunların üstüne yazılıyor.
    """
    lines = exercise.starter_code_for(language).splitlines()
    return "\n".join(l for l in lines if l.strip() and not l.strip().startswith("#"))


def denetle(directories: list[Path]) -> list[str]:
    problems: list[str] = []
    count = 0

    for path in directories:
        exercise = Exercise.load(path)
        where = f"{path.parts[-4]}/{path.parts[-3]}/{exercise.id}"
        count += 1

        result = run_code(
            exercise.solution_code, exercise.checks, exercise.timeout_sec, path
        )
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
            alone = run_code(code, exercise.checks, exercise.timeout_sec, path)
            if alone.passed:
                continue
            merged = starter_kodu(exercise, language) + "\n" + code
            hint_result = run_code(
                merged, exercise.checks, exercise.timeout_sec, path
            )
            if not hint_result.passed:
                problems.append(
                    f"{where}: son ipucu ({language}) alıştırmayı çözmüyor "
                    f"(tek başına {alone.status}, birleşik {hint_result.status})"
                )

    print(f"{count} alıştırma çalıştırıldı.")
    return problems


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

    started = time.time()
    problems = denetle(directories)
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
