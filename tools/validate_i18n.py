"""Dil dosyalarını denetler.

Yeni bir metin eklerken bir dile ekleyip diğerini unutmak çok kolay. Bu script
onu yakalar:

- İki dosyada da aynı anahtarlar var mı?
- Bir metindeki yer tutucular ({name} gibi) diğer dilde de aynı mı?
- Boş bırakılmış çeviri var mı?

Kullanım:
    .venv\\Scripts\\python tools/validate_i18n.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

I18N_DIR = Path(__file__).resolve().parent.parent / "app" / "i18n"
PLACEHOLDER = re.compile(r"\{(\w+)\}")

# Türkçe referans kabul ediliyor: içerik önce Türkçe yazılıyor.
REFERENCE = "tr"


def load(language: str) -> dict[str, str]:
    path = I18N_DIR / f"{language}.json"
    if not path.exists():
        sys.exit(f"Dil dosyası bulunamadı: {path}")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    languages = sorted(p.stem for p in I18N_DIR.glob("*.json"))
    if REFERENCE not in languages:
        sys.exit(f"Referans dil ({REFERENCE}) bulunamadı.")

    catalogs = {language: load(language) for language in languages}
    reference = catalogs[REFERENCE]
    problems: list[str] = []

    for language in languages:
        if language == REFERENCE:
            continue
        catalog = catalogs[language]

        for key in sorted(set(reference) - set(catalog)):
            problems.append(f"[{language}] eksik anahtar: {key}")

        for key in sorted(set(catalog) - set(reference)):
            problems.append(f"[{language}] fazladan anahtar: {key}")

        for key in sorted(set(reference) & set(catalog)):
            expected = set(PLACEHOLDER.findall(reference[key]))
            actual = set(PLACEHOLDER.findall(catalog[key]))
            if expected != actual:
                problems.append(
                    f"[{language}] '{key}' yer tutucuları uyuşmuyor: "
                    f"{sorted(expected)} yerine {sorted(actual)}"
                )

    for language, catalog in catalogs.items():
        for key, value in sorted(catalog.items()):
            if not value.strip():
                problems.append(f"[{language}] boş çeviri: {key}")

    if problems:
        print(f"{len(problems)} sorun bulundu:\n")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    counts = ", ".join(f"{lang}: {len(cat)}" for lang, cat in catalogs.items())
    print(f"Dil dosyaları tutarlı ({counts}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
