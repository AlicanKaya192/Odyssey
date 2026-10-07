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
from app.core.problem_check import parse_number  # noqa: E402
from app.core.workspace_files import safe_name  # noqa: E402
from app.paths import content_dir  # noqa: E402

LANGUAGES = ("tr", "en")

# Bölümün seviyesi. Boş bırakılabiliyor; yazılıyorsa yol ekranı bu ada
# göre başlık arıyor (`path.level_<seviye>`), uydurma bir ad ekranda ham
# anahtar olarak görünürdü.
# Matematik MAT 2'de seviye zorluk değil konu grubu: doğrusal cebir,
# kalkülüs, olasılık.
SEVIYELER = ("basic", "intermediate", "advanced", "linear_algebra", "calculus", "probability")
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

        seviyeliler = 0

        for section in chapter.sections:
            where = f"{chapter.id}/{section.id}"
            coverage.append(
                Coverage(where, "bölüm başlığı", section.id, check_localized_dict(section.title))
            )

            if section.level:
                seviyeliler += 1
                if section.level not in SEVIYELER:
                    problems.append(
                        f"{where}: tanınmayan seviye '{section.level}' "
                        f"(beklenen: {', '.join(SEVIYELER)})"
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

        # Modülün bölümleri ya tümü seviyeli ya da hiçbiri. Yarısı seviyeli
        # olursa seviyesiz bölümler sessizce bir önceki başlığın altına
        # düşüyor; ekranda hata görünmüyor ama ders yanlış gruba giriyor.
        if seviyeliler and seviyeliler != len(chapter.sections):
            problems.append(
                f"{chapter.id}: bölümlerin {seviyeliler}/"
                f"{len(chapter.sections)} tanesinde seviye var, "
                "ya hepsinde olmalı ya hiçbirinde"
            )

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
        elif kind == "http":
            # Kişinin yazacağı adres ve gövdeler (`/books`, alan adları).
            denetle("uygulama adı", check.get("app"))
            for step in check.get("steps", []):
                denetle("istek adresi", step.get("path"))
                denetle("istek gövdesi", step.get("json"))
                denetle("beklenen yanıt", (step.get("expect") or {}).get("json"))
                denetle("beklenen alanlar", (step.get("expect") or {}).get("json_has"))
        elif kind in ("rows", "columns"):
            # SQL sonuç kümesi: sütun adları ve beklenen hücreler de
            # öğrencinin yazacağı şeyler arasında.
            denetle("beklenen sonuç", check.get("expected"))
        elif kind in ("sql_require", "sql_forbid"):
            denetle("SQL kalıbı", check.get("pattern"))

    return problems


# Tanınan alıştırma dilleri ve her birinin kabul ettiği kontrol tipleri.
# Yanlış eşleşme sessizce geçmesin: bir Python alıştırmasına `rows`
# yazıldığında kontrol hiç çalışmıyor ama alıştırma "geçti" görünüyor.
DILLER = ("python", "tsql", "docker")
ORTAK_KONTROLLER = {"stdout", "artifact"}
DILE_OZEL_KONTROLLER = {
    "python": {
        "variable", "function", "ast_require", "ast_forbid",
        "annotation", "method", "requests",
        # API 2: FastAPI uygulaması sunucusuz çağrılıyor, kişinin testleri koşuyor.
        "http", "pytest",
    },
    "tsql": {
        "rows", "columns", "affected_rows", "sql_require", "sql_forbid",
        "schema_unchanged",
    },
    # Docker'da ortak kontroller (stdout, artifact) yok: kişinin kodu
    # çalışmıyor, dosyaları denetleniyor ve imaj kuruluyor.
    "docker": {"dockerfile", "compose", "command", "container", "compose_up"},
}
ORTAKSIZ_DILLER = {"docker"}


def _check_problem(where: str, exercise) -> list[str]:
    """Matematik problemi: kod yok, cevap alanları ve adım adım çözüm var."""
    problems: list[str] = []
    yer = f"{where}/{exercise.id}"

    if not exercise.answers:
        problems.append(f"{yer}: problemde cevap alanı yok")
    for index, spec in enumerate(exercise.answers, start=1):
        if "value" not in spec and not spec.get("accept"):
            problems.append(f"{yer}: {index}. cevabın ne değeri ne kabul listesi var")
        if "value" in spec and parse_number(str(spec["value"])) is None:
            problems.append(f"{yer}: {index}. cevabın değeri sayı değil ({spec['value']!r})")
        if len(exercise.answers) > 1 and not all(spec.get("label", {}).get(l) for l in LANGUAGES):
            problems.append(f"{yer}: birden fazla cevap var ama {index}. alanın iki dilde etiketi yok")

    symbols = exercise.raw.get("symbols", [])
    if not isinstance(symbols, list) or not all(isinstance(s, str) and s for s in symbols):
        problems.append(f"{yer}: symbols boş olmayan metinlerden oluşan bir liste olmalı")

    # Problemde çözüm ipucunda değil, çözüm yollarında; ipuçları yalnızca
    # yönlendirme.
    if not exercise.hints:
        problems.append(f"{yer}: problemde ipucu yok")
    if not exercise.solutions:
        problems.append(f"{yer}: problemde çözüm yolu yok")
    for index, solution in enumerate(exercise.solutions, start=1):
        template = solution.get("file", "")
        for lang in LANGUAGES:
            if not (exercise.directory / template.replace("{lang}", lang)).exists():
                problems.append(f"{yer}: {index}. çözüm yolunun {lang} dosyası yok ({template})")
        if len(exercise.solutions) > 1 and not all(solution.get("title", {}).get(l) for l in LANGUAGES):
            problems.append(f"{yer}: {index}. çözüm yolunun iki dilde başlığı yok")
    if exercise.raw.get("checks") or exercise.raw.get("starter") or exercise.raw.get("solution"):
        problems.append(f"{yer}: problemde kod alanları (checks/starter/solution) olmaz")
    return problems


# Zorluk ölçeği arayüzdeki gibi üç kademe (●○○ / ●●○ / ●●●). Makine
# Öğrenmesi patikası dört kademeyle yazılmıştı ve 4'ler arayüzde boş bir
# "Zorluk:" etiketi olarak görünüyordu; bu denetim yokken fark edilmedi.
ZORLUKLAR = (1, 2, 3)


# Çok dosyalı alıştırmanın başlangıç / çözüm şablonları bu öneklerle
# başlamalı: çalıştırıcı alıştırma klasörünü kopyalarken onları atlıyor
# (`runner.SKIPPED_PREFIXES`); başka adla kişinin çalışma klasörüne düşerlerdi.
SABLON_ONEKLERI = ("starter", "solution")


def _check_files(where: str, exercise) -> list[str]:
    """Çok dosyalı alıştırma (`files`): adlar, şablonlar, giriş dosyası."""
    yer = f"{where}/{exercise.id}"
    problems: list[str] = []
    if exercise.language not in ("python", "docker"):
        problems.append(f"{yer}: çok dosyalı alıştırma yalnızca python ve docker")
    if exercise.raw.get("starter") or exercise.raw.get("solution"):
        problems.append(f"{yer}: files varken starter/solution dosyanın içinde yazılır")

    adlar = []
    for item in exercise.raw.get("files", []):
        if not isinstance(item, dict) or not item.get("name"):
            problems.append(f"{yer}: files öğesinde name yok")
            continue
        ad = str(item["name"])
        adlar.append(ad)
        if not safe_name(ad):
            problems.append(f"{yer}: dosya adı güvenli değil ({ad!r})")
        if item.get("readonly"):
            if item.get("starter") or item.get("solution"):
                problems.append(f"{yer}: salt okunur {ad} starter/solution almaz")
            kaynak = str(item.get("source") or ad)
            if not (exercise.directory / kaynak).exists():
                problems.append(f"{yer}: salt okunur dosya yok ({kaynak})")
            continue
        for alan in ("starter", "solution"):
            sablon = item.get(alan)
            if not sablon:
                continue
            if not str(sablon).startswith(SABLON_ONEKLERI):
                problems.append(f"{yer}: {ad} {alan} şablonu {SABLON_ONEKLERI} ile başlamalı ({sablon})")
            diller = LANGUAGES if "{lang}" in sablon else ("",)
            for lang in diller:
                dosya = sablon.replace("{lang}", lang)
                if not (exercise.directory / dosya).exists():
                    problems.append(f"{yer}: {ad} {alan} dosyası yok ({dosya})")

    if len(set(adlar)) != len(adlar):
        problems.append(f"{yer}: aynı adlı iki dosya var")
    giris = exercise.file(exercise.entry)
    if giris is None:
        problems.append(f"{yer}: giriş dosyası ({exercise.entry}) files içinde yok")
    elif exercise.language == "python" and not giris.name.endswith(".py"):
        problems.append(f"{yer}: giriş dosyası .py olmalı ({giris.name})")

    duzenlenebilir = [item for item in exercise.files if not item.readonly]
    if not duzenlenebilir:
        problems.append(f"{yer}: düzenlenebilir dosya yok")
    elif all(item.solution_for("tr").strip() == item.starter_for("tr").strip() for item in duzenlenebilir):
        problems.append(f"{yer}: çözüm başlangıçla aynı")

    for check in exercise.checks:
        if check.get("file") and check["file"] not in adlar:
            problems.append(f"{yer}: kontrolün dosyası files içinde yok ({check['file']})")
    return problems


def _check_difficulty(where: str, exercise) -> list[str]:
    deger = exercise.raw.get("difficulty")
    if deger not in ZORLUKLAR:
        return [f"{where}/{exercise.id}: zorluk {deger!r}; 1, 2 ya da 3 olmalı"]
    return []


# Git terminal alıştırmasının `git_state` alanları (`app/core/git_checks.py`).
GIT_STATE_KEYS = {
    "type", "repo", "label", "hint", "show_message", "exists", "branch", "branches", "no_branches",
    "no_remote_branches",
    "commits", "min_commits", "clean", "staged", "unstaged", "untracked", "tracked", "not_tracked",
    "files", "missing_files", "head_files", "last_message", "messages", "merged", "merge_commit",
    "linear", "no_conflicts", "in_progress", "tags", "annotated", "stash", "config", "remotes",
    "upstream", "pushed", "remote_commits", "ignored", "detached", "same_as", "blob_of", "tips", "tag_at", "remote_tags", "last_body", "show_body",
}


def _check_terminal(where: str, exercise) -> list[str]:
    """Git terminal alıştırması: kod dosyası yok; kurulum, çözüm komutları,
    kontroller ve hedef etiketleri. Çözümün gerçekten geçtiğine
    `check_exercises.py` bakıyor."""
    problems: list[str] = []
    yer = f"{where}/{exercise.id}"
    if exercise.language != "git":
        problems.append(f"{yer}: terminal alıştırmasının dili 'git' olmalı ({exercise.language!r})")
    for alan in ("starter", "files", "entry"):
        if alan in exercise.raw:
            problems.append(f"{yer}: terminal alıştırmasında {alan!r} olmaz")
    if not exercise.checks:
        problems.append(f"{yer}: hiç kontrol tanımlanmamış")
    etiketli = 0
    for check in exercise.checks:
        tur = check.get("type", "")
        if tur == "git_state":
            for key in check:
                if key not in GIT_STATE_KEYS:
                    problems.append(f"{yer}: bilinmeyen git_state alanı {key!r}")
        elif tur == "shell_state":
            for key in check:
                if key not in {"type", "label", "hint", "dirs", "files", "missing", "cwd"}:
                    problems.append(f"{yer}: bilinmeyen shell_state alanı {key!r}")
        elif tur == "git_config":
            for key in check:
                if key not in {"type", "label", "hint", "repo", "global", "local"}:
                    problems.append(f"{yer}: bilinmeyen git_config alanı {key!r}")
        elif tur == "git_command":
            if not check.get("pattern"):
                problems.append(f"{yer}: git_command kontrolünde pattern yok")
        else:
            problems.append(f"{yer}: terminal alıştırmasında geçersiz kontrol tipi {tur!r}")
        label = check.get("label")
        if label:
            etiketli += 1
            for lang in LANGUAGES:
                if not label.get(lang):
                    problems.append(f"{yer}: hedef etiketi {lang} dilinde yok")
    if exercise.checks and not etiketli:
        problems.append(f"{yer}: hiçbir kontrolün hedef etiketi (label) yok")
    komutlar = exercise.solution_commands
    if not komutlar or not isinstance(exercise.raw.get("solution"), list):
        problems.append(f"{yer}: solution komut listesi olmalı")
    for komut in komutlar:
        if not komut.isascii():
            disi = sorted({ch for ch in komut if not ch.isascii()})
            problems.append(f"{yer}: çözüm komutu ASCII değil ({''.join(disi)}) -> {komut!r}")
    for adim in exercise.setup:
        if not isinstance(adim, (str, dict)) or (isinstance(adim, dict) and not adim.get("remote")):
            problems.append(f"{yer}: kurulum adımı komut ya da {{'remote': ...}} olmalı: {adim!r}")
    return problems


def _check_exercise(where: str, exercise) -> list[str]:
    if exercise.is_problem:
        return _check_difficulty(where, exercise) + _check_problem(where, exercise)
    if exercise.is_terminal:
        return _check_difficulty(where, exercise) + _check_terminal(where, exercise)

    problems: list[str] = _check_difficulty(where, exercise)

    if not exercise.checks:
        problems.append(f"{where}/{exercise.id}: hiç kontrol tanımlanmamış")

    dil = exercise.language
    if dil not in DILLER:
        problems.append(
            f"{where}/{exercise.id}: bilinmeyen dil {dil!r} "
            f"(beklenen: {', '.join(DILLER)})"
        )
    else:
        izinli = DILE_OZEL_KONTROLLER[dil] | (set() if dil in ORTAKSIZ_DILLER else ORTAK_KONTROLLER)
        for check in exercise.checks:
            tur = check.get("type", "")
            if tur not in izinli:
                problems.append(
                    f"{where}/{exercise.id}: {dil} alıştırmasında "
                    f"geçersiz kontrol tipi {tur!r}"
                )

    if dil == "tsql":
        # Tohum olmadan alıştırmanın sorgulayacağı bir tablo yok.
        if not (exercise.directory / "seed.sql").exists():
            problems.append(f"{where}/{exercise.id}: seed.sql yok")

    problems.extend(_check_ascii(where, exercise))

    if exercise.is_multi_file:
        return problems + _check_files(where, exercise)

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
