"""İçeriği denetler ve çeviri kapsamını raporlar.

İki iş yapıyor:

1. **Şema denetimi** — bölüm ve alıştırma dosyaları beklenen alanlara sahip
   mi, sınav cevap indeksleri geçerli mi, dosya yolları var mı.
2. **Çeviri kapsamı** — her parçanın hangi dillerde bulunduğu. İçerik Türkçe
   yazılıyor; İngilizcesi eksik kalan yerler burada görünür olsun ki 23 modül
   birikince nerede ne eksik olduğu kaybolmasın.

Kullanım:
    .venv\\Scripts\\python tools/validate_content.py
    .venv\\Scripts\\python tools/validate_content.py --kapsam    # yalnız rapor
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.core.catalog import Catalog, ContentError  # noqa: E402
from app.paths import content_dir  # noqa: E402

LANGUAGES = ("tr", "en")
REFERENCE = "tr"


@dataclass
class Coverage:
    """Tek bir çeviri biriminin durumu."""

    section: str
    kind: str
    name: str
    present: set[str] = field(default_factory=set)

    @property
    def missing(self) -> list[str]:
        return [lang for lang in LANGUAGES if lang not in self.present]


def check_localized_dict(values: dict | None) -> set[str]:
    """`{"tr": ..., "en": ...}` alanında hangi diller dolu?"""
    if not isinstance(values, dict):
        return set()
    return {lang for lang in LANGUAGES if str(values.get(lang, "")).strip()}


def check_localized_file(directory: Path, template: str) -> set[str]:
    """`lesson.{lang}.md` gibi bir şablonun hangi dilleri var?"""
    if "{lang}" not in template:
        return set(LANGUAGES) if (directory / template).exists() else set()
    return {
        lang
        for lang in LANGUAGES
        if (directory / template.replace("{lang}", lang)).exists()
    }


def collect(catalog: Catalog) -> tuple[list[Coverage], list[str]]:
    """Bütün içeriği gezip kapsam ve şema sorunlarını toplar."""
    coverage: list[Coverage] = []
    problems: list[str] = []

    for chapter in catalog.chapters:
        label = chapter.id
        coverage.append(
            Coverage(label, "modül başlığı", chapter.id, check_localized_dict(chapter.title))
        )

        for section in chapter.sections:
            where = f"{chapter.id}/{section.id}"
            coverage.append(
                Coverage(where, "bölüm başlığı", section.id, check_localized_dict(section.title))
            )

            for block in section.blocks:
                if block.type == "lesson":
                    template = block.raw.get("file", "")
                    coverage.append(
                        Coverage(where, "konu anlatımı", template,
                                 check_localized_file(section.directory, template))
                    )

                elif block.type == "notes":
                    for document in block.documents:
                        coverage.append(
                            Coverage(where, "ders notu",
                                     document.get("id", "?"),
                                     check_localized_file(
                                         section.directory, document.get("file", "")))
                        )
                        coverage.append(
                            Coverage(where, "not başlığı", document.get("id", "?"),
                                     check_localized_dict(document.get("title")))
                        )

                elif block.type == "quiz":
                    resolved = block.file_for(REFERENCE)
                    if resolved is None or not resolved.exists:
                        problems.append(f"{where}: sınav dosyası bulunamadı")
                        continue
                    problems.extend(_check_quiz(where, resolved.path, coverage))

            for exercise in section.exercises:
                prompts = exercise.raw.get("prompt", {})
                coverage.append(
                    Coverage(where, "alıştırma yönergesi", exercise.id,
                             {lang for lang in LANGUAGES
                              if prompts.get(lang)
                              and (exercise.directory / prompts[lang]).exists()})
                )
                coverage.append(
                    Coverage(where, "alıştırma başlığı", exercise.id,
                             check_localized_dict(exercise.title))
                )

                for index, hint in enumerate(exercise.hints, start=1):
                    coverage.append(
                        Coverage(where, "ipucu", f"{exercise.id}/{index}",
                                 check_localized_dict(hint))
                    )

                problems.extend(_check_exercise(where, exercise))

    return coverage, problems


def _check_quiz(where: str, path: Path, coverage: list[Coverage]) -> list[str]:
    problems: list[str] = []
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)

    for question in data.get("questions", []):
        qid = question.get("id", "?")
        coverage.append(
            Coverage(where, "soru metni", qid, check_localized_dict(question.get("text")))
        )

        options = question.get("options", {})
        present = {
            lang for lang in LANGUAGES
            if isinstance(options.get(lang), list) and options[lang]
        }
        coverage.append(Coverage(where, "soru şıkları", qid, present))
        coverage.append(
            Coverage(where, "soru açıklaması", qid,
                     check_localized_dict(question.get("explanation")))
        )

        answer = question.get("answer")
        reference_options = options.get(REFERENCE, [])
        if not isinstance(answer, int) or not (0 <= answer < len(reference_options)):
            problems.append(f"{where}/{qid}: cevap indeksi geçersiz ({answer})")

        # Şıkların sayısı diller arasında tutmalı, yoksa cevap kayar.
        counts = {lang: len(options.get(lang, [])) for lang in present}
        if len(set(counts.values())) > 1:
            problems.append(f"{where}/{qid}: dillere göre şık sayısı farklı {counts}")

    return problems


def _check_ascii(where: str, exercise) -> list[str]:
    """Kullanıcının yazmak zorunda kaldığı her şey ASCII olmalı.

    İngilizce klavyede `ş ğ ı İ ç ö ü` yok. `takim = "Beşiktaş"` isteyen bir
    alıştırmayı İngilizce kullanan biri çözemez. Ders metni bu kurala girmez;
    orası okunur, yazılmaz.
    """
    problems: list[str] = []

    def denetle(etiket: str, value) -> None:
        # Beklenen değerler liste, sözlük ya da `{"__tuple__": [...]}` olabiliyor;
        # ASCII denetimi bunların içine de girmeli, yoksa demet içindeki bir
        # Türkçe karakter fark edilmeden geçer.
        if isinstance(value, dict):
            for item in value.values():
                denetle(etiket, item)
            return
        if isinstance(value, (list, tuple)):
            for item in value:
                denetle(etiket, item)
            return
        if not isinstance(value, str):
            return
        if not value.isascii():
            disi = sorted({ch for ch in value if not ch.isascii()})
            problems.append(
                f"{where}/{exercise.id}: {etiket} ASCII değil "
                f"({''.join(disi)}) -> {value!r}"
            )

    for check in exercise.checks:
        kind = check.get("type")
        if kind == "variable":
            denetle("değişken adı", check.get("name"))
            denetle("beklenen değer", check.get("equals"))
        elif kind == "function":
            denetle("fonksiyon adı", check.get("name"))
            for case in check.get("cases", []):
                for argument in case.get("args", []):
                    denetle("örnek argüman", argument)
                denetle("beklenen dönüş", case.get("returns"))
        elif kind == "stdout":
            denetle("beklenen çıktı", check.get("expected"))
        elif kind == "method":
            denetle("sınıf adı", check.get("class"))
            for argument in check.get("args", []):
                denetle("kurucu argümanı", argument)
            for case in check.get("cases", []):
                denetle("metot adı", case.get("method"))
                denetle("özellik adı", case.get("attribute"))
                for argument in case.get("args", []):
                    denetle("örnek argüman", argument)
                denetle("beklenen dönüş", case.get("returns"))
                denetle("beklenen değer", case.get("equals"))
        elif kind == "annotation":
            denetle("fonksiyon adı", check.get("name"))
            denetle("değişken adı", check.get("variable"))
            denetle("beklenen belirtim", check.get("is"))
            denetle("dönüş belirtimi", check.get("returns"))
            for param, tip in (check.get("params") or {}).items():
                denetle("parametre adı", param)
                denetle("parametre belirtimi", tip)
        elif kind == "ast_forbid":
            denetle("yasaklı çağrı", check.get("call"))

    return problems


def _check_exercise(where: str, exercise) -> list[str]:
    problems: list[str] = []

    if not exercise.checks:
        problems.append(f"{where}/{exercise.id}: hiç kontrol tanımlanmamış")

    problems.extend(_check_ascii(where, exercise))

    for name in ("starter", "solution"):
        value = exercise.raw.get(name)
        if not value:
            continue
        if "{lang}" in value:
            for lang in LANGUAGES:
                if not (exercise.directory / value.replace("{lang}", lang)).exists():
                    problems.append(
                        f"{where}/{exercise.id}: {name} dosyası yok "
                        f"({value.replace('{lang}', lang)})"
                    )
        elif not (exercise.directory / value).exists():
            problems.append(f"{where}/{exercise.id}: {name} dosyası yok ({value})")

    if exercise.raw.get("solution"):
        # Çözüm dosyası başlangıç koduyla aynıysa öğrenciye bir şey vermiyor.
        if exercise.solution_code.strip() == exercise.starter_code.strip():
            problems.append(f"{where}/{exercise.id}: çözüm başlangıç koduyla aynı")

    return problems


def report(coverage: list[Coverage]) -> int:
    """Çeviri kapsamını özetler, eksik birim sayısını döndürür."""
    by_kind: dict[str, list[Coverage]] = {}
    for item in coverage:
        by_kind.setdefault(item.kind, []).append(item)

    print("ÇEVİRİ KAPSAMI")
    print("-" * 66)
    total_missing = 0

    for kind in sorted(by_kind):
        items = by_kind[kind]
        complete = sum(1 for item in items if not item.missing)
        missing = len(items) - complete
        total_missing += missing
        oran = round(complete * 100 / len(items)) if items else 100
        durum = "tam" if missing == 0 else f"{missing} eksik"
        print(f"  {kind:<22} {complete:>3}/{len(items):<3}  %{oran:<4} {durum}")

    if total_missing:
        print()
        print("EKSİKLER")
        print("-" * 66)
        for item in coverage:
            if item.missing:
                print(f"  {item.section:<34} {item.kind:<20} {item.name}"
                      f"   -> eksik: {', '.join(item.missing)}")

    print("-" * 66)
    toplam = len(coverage)
    print(f"  Toplam {toplam} birim, {toplam - total_missing} tanesi iki dilde "
          f"(%{round((toplam - total_missing) * 100 / toplam) if toplam else 100})")
    return total_missing


def main() -> int:
    yalniz_kapsam = "--kapsam" in sys.argv

    try:
        catalog = Catalog.load(content_dir())
    except ContentError as exc:
        print(f"İçerik okunamadı: {exc}")
        return 2

    coverage, problems = collect(catalog)

    if not yalniz_kapsam:
        print("ŞEMA DENETİMİ")
        print("-" * 66)
        if problems:
            for problem in problems:
                print(f"  - {problem}")
        else:
            print("  Sorun yok.")
        print()

    missing = report(coverage)

    # Eksik çeviri hata değil, bilinen durum: içerik önce Türkçe yazılıyor.
    # Şema sorunu ise hatadır.
    return 1 if problems and not yalniz_kapsam else 0


if __name__ == "__main__":
    raise SystemExit(main())
