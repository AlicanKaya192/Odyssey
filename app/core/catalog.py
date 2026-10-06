"""Müfredat ağacını okur.

`content/` altındaki JSON dosyalarını okuyup bölüm ve alt bölüm nesnelerine
çevirir. Dosya adlarındaki ``{lang}`` yer tutucusu seçili dile göre çözülür;
istenen dilde dosya yoksa Türkçesine düşülür ve bu durum
``LocalizedFile.is_fallback`` ile bildirilir, böylece arayüz "bu bölüm henüz
çevrilmedi" şeridini gösterebilir.

Buradaki id'ler kullanıcının ilerlemesiyle eşleşiyor. Bu yüzden bir id bir kez
verildikten sonra **değiştirilmez**; başlık ve dosya adı değişebilir ama id
sabit kalır.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .workspace_files import file_language

FALLBACK_LANGUAGE = "tr"

# Tek dosyalı alıştırmada kişinin dosyasının adı (terminaldeki komut da
# bunu yazıyor: `python cozum.py`, `sqlcmd -i sorgu.sql`).
SINGLE_FILE_NAMES = {"python": "cozum.py", "tsql": "sorgu.sql"}


class ContentError(Exception):
    """İçerik dosyalarında yapısal bir sorun olduğunda atılır."""


def _read_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise ContentError(f"Dosya bulunamadı: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ContentError(f"JSON okunamadı ({path}): {exc}") from exc


@dataclass(frozen=True)
class LocalizedFile:
    """Dile göre çözülmüş bir dosya yolu."""

    path: Path
    language: str
    is_fallback: bool

    @property
    def exists(self) -> bool:
        return self.path.exists()


def resolve_localized(directory: Path, template: str, language: str) -> LocalizedFile | None:
    """``lesson.{lang}.md`` gibi bir şablonu seçili dile göre çözer.

    İstenen dilde dosya yoksa Türkçesine düşer. İkisi de yoksa None döner.
    """
    if "{lang}" not in template:
        path = directory / template
        return LocalizedFile(path, language, False) if path.exists() else None

    wanted = directory / template.replace("{lang}", language)
    if wanted.exists():
        return LocalizedFile(wanted, language, False)

    fallback = directory / template.replace("{lang}", FALLBACK_LANGUAGE)
    if fallback.exists():
        return LocalizedFile(fallback, FALLBACK_LANGUAGE, language != FALLBACK_LANGUAGE)

    return None


@dataclass
class Block:
    """Bir alt bölümün içindeki tek bir parça (ders, PDF, sınav, alıştırma)."""

    type: str
    raw: dict
    directory: Path

    @property
    def title(self) -> dict[str, str]:
        return self.raw.get("title", {})

    @property
    def pass_score(self) -> int:
        return int(self.raw.get("pass_score", 70))

    @property
    def time_limit_sec(self) -> int:
        """Sınav süresi. `0` süre yok demek.

        Bölümün kendi `section.json` dosyasında yazıyor: konu zorlaştıkça
        sorular uzuyor ve kod okumak zaman istiyor, o yüzden süre soru
        sayısından türetilmiyor, elle veriliyor.
        """
        return int(self.raw.get("time_limit_sec", 0))

    def file_for(self, language: str) -> LocalizedFile | None:
        template = self.raw.get("file")
        if not template:
            return None
        return resolve_localized(self.directory, template, language)

    @property
    def exercise_dir(self) -> Path | None:
        relative = self.raw.get("dir")
        return self.directory / relative if relative else None

    @property
    def documents(self) -> list[dict]:
        """`notes` bloğundaki ders notlarının listesi.

        Her not: ``{"id", "title": {"tr", "en"}, "file": "notlar/01.{lang}.md"}``
        Notlar PDF değil metin olarak tutuluyor; uygulama içinde aranabilsin,
        kopyalanabilsin ve temayla uyumlu görünsün diye.
        """
        return list(self.raw.get("documents", []))


def read_template(directory: Path, name: str, language: str) -> str:
    """`starter.{lang}.py` gibi bir kod dosyasını dile göre okur.

    Dosya adında `{lang}` varsa kullanıcının diline göre çözülür; yorum
    satırları böylece okunabilir kalıyor. İstenen dil yoksa Türkçesine
    düşülür. Dosya yoksa boş metin.
    """
    if not name:
        return ""
    if "{lang}" in name:
        wanted = directory / name.replace("{lang}", language)
        if wanted.exists():
            return wanted.read_text(encoding="utf-8")
        name = name.replace("{lang}", FALLBACK_LANGUAGE)
    path = directory / name
    return path.read_text(encoding="utf-8") if path.exists() else ""


@dataclass
class ExerciseFile:
    """Alıştırmanın bir dosyası (`exercise.json` → `files`).

    ``{"name": "models.py", "starter": "starter-models.{lang}.py",
    "solution": "solution-models.py"}`` düzenlenebilir bir dosya;
    ``{"name": "settings.json", "readonly": true}`` alıştırma klasöründeki
    dosyanın kendisi, editörde gösteriliyor ama değiştirilemiyor
    (`source` başka bir ad verebilir). Başlangıcı olmayan düzenlenebilir
    dosya boş açılıyor (kişi yazıyor).
    """

    name: str
    directory: Path
    raw: dict

    @property
    def readonly(self) -> bool:
        return bool(self.raw.get("readonly", False))

    @property
    def language(self) -> str:
        return str(self.raw.get("language") or file_language(self.name))

    def starter_for(self, language: str) -> str:
        if self.readonly:
            return read_template(self.directory, str(self.raw.get("source") or self.name), language)
        return read_template(self.directory, str(self.raw.get("starter", "")), language)

    def solution_for(self, language: str) -> str:
        """Çözümdeki hâli; çözümü yazılmamış dosya başlangıçtaki gibi kalıyor."""
        if self.readonly or not self.raw.get("solution"):
            return self.starter_for(language)
        return read_template(self.directory, str(self.raw["solution"]), language)

    def starter_variants(self) -> list[str]:
        """Bütün dillerdeki başlangıç hâlleri (dil listesi dosya adlarından)."""
        name = "" if self.readonly else str(self.raw.get("starter", ""))
        if not name:
            return [self.starter_for(FALLBACK_LANGUAGE)]
        if "{lang}" not in name:
            path = self.directory / name
            return [path.read_text(encoding="utf-8")] if path.exists() else []
        found = sorted(self.directory.glob(name.replace("{lang}", "*")))
        return [path.read_text(encoding="utf-8") for path in found]

    def is_untouched(self, code: str) -> bool:
        """Metin hâlâ (herhangi bir dildeki) başlangıç hâli mi."""
        current = code.strip()
        return any(current == variant.strip() for variant in self.starter_variants())


@dataclass
class Exercise:
    """Tek bir alıştırma: kod yazılan ya da cevabı hesaplanan (problem).

    YZ Matematiği patikasında alıştırmalar kod değil **matematik
    problemi** (`"kind": "problem"`): kullanıcı cevabı yazıyor, cevap
    `core/problem_check.py` ile karşılaştırılıyor. Yönerge ve kademeli
    ipuçları iki türde de aynı; son ipucu problemde çözümün adım adım
    hâli.
    """

    id: str
    directory: Path
    raw: dict

    @property
    def kind(self) -> str:
        """`code` (varsayılan) ya da `problem`."""
        return str(self.raw.get("kind", "code"))

    @property
    def is_problem(self) -> bool:
        return self.kind == "problem"

    @property
    def answers(self) -> list[dict]:
        """Problemin cevap alanları; kod alıştırmasında boş."""
        return list(self.raw.get("answers", []))

    @property
    def symbols(self) -> list[str]:
        """Problemin çalışma kâğıdında öne çıkan özel semboller (`log₂` gibi)."""
        return [str(item) for item in self.raw.get("symbols", [])]

    @property
    def solutions(self) -> list[dict]:
        """Problemin çözüm yolları: ``{"title": {...}, "file": "cozum-1.{lang}.md"}``.

        Birden fazla yol olabiliyor (önce bölmek ya da doğrudan logaritma
        almak gibi); kişi kendi yolunu hepsiyle karşılaştırabiliyor.
        """
        return list(self.raw.get("solutions", []))

    def solution_text(self, index: int, language: str) -> str:
        """Bir çözüm yolunun metni; istenen dil yoksa Türkçesi."""
        solutions = self.solutions
        if not 0 <= index < len(solutions):
            return ""
        template = solutions[index].get("file", "")
        for code in (language, FALLBACK_LANGUAGE):
            path = self.directory / template.replace("{lang}", code)
            if path.exists():
                return path.read_text(encoding="utf-8")
        return ""

    @property
    def title(self) -> dict[str, str]:
        return self.raw.get("title", {})

    @property
    def difficulty(self) -> int:
        return int(self.raw.get("difficulty", 1))

    @property
    def timeout_sec(self) -> int:
        return int(self.raw.get("timeout_sec", 10))

    @property
    def language(self) -> str:
        """Alıştırmanın dili: `python` (varsayılan) ya da `tsql`.

        Dosya adları da buna göre değişiyor (`solution.sql`), ama okuma
        `_code_for` üzerinden yapıldığı için burada yalnızca çalıştırıcının
        hangi yolu seçeceği belirleniyor.
        """
        return str(self.raw.get("language", "python"))

    @property
    def checks(self) -> list[dict]:
        return list(self.raw.get("checks", []))

    @property
    def hints(self) -> list[dict]:
        """Kademeli ipuçları.

        Her kademe ``{"tr": ..., "en": ...}`` biçiminde bir metin. Sıra
        yönlendiren ipucundan çözüme doğru gider; kullanıcı hangi kademeye
        kadar bakacağına kendisi karar verir.
        """
        return list(self.raw.get("hints", []))

    def prompt_for(self, language: str) -> LocalizedFile | None:
        prompts = self.raw.get("prompt", {})
        template = prompts.get(language) or prompts.get(FALLBACK_LANGUAGE)
        if not template:
            return None
        resolved = self.directory / template
        if not resolved.exists():
            return None
        used = language if prompts.get(language) else FALLBACK_LANGUAGE
        return LocalizedFile(resolved, used, used != language)

    def _code_for(self, key: str, language: str) -> str:
        """`starter` / `solution` dosyasını dile göre okur.

        Çok dosyalı alıştırmada giriş dosyasının hâli: tek metin bekleyen
        yerler (ipucu, "takıldın mı?") onunla çalışmaya devam ediyor.
        """
        if self.is_multi_file:
            entry = self.file(self.entry)
            if entry is None:
                return ""
            return entry.starter_for(language) if key == "starter" else entry.solution_for(language)
        return read_template(self.directory, str(self.raw.get(key) or ""), language)

    # --- çok dosyalı alıştırma ---------------------------------------------

    @property
    def is_multi_file(self) -> bool:
        """Alıştırma birden çok dosyadan mı oluşuyor (`files` alanı)."""
        return bool(self.raw.get("files"))

    @property
    def files(self) -> list[ExerciseFile]:
        """Editörde sekme olarak açılan dosyalar, sırasıyla.

        Tek dosyalı alıştırmada da bir dosya var (`cozum.py` / `sorgu.sql`);
        arayüz iki türü aynı yoldan kuruyor, sekme şeridini yalnızca birden
        çok dosya varken gösteriyor.
        """
        if not self.is_multi_file:
            raw = {"starter": self.raw.get("starter", ""), "solution": self.raw.get("solution", ""),
                   "language": self.language}
            return [ExerciseFile(SINGLE_FILE_NAMES.get(self.language, "cozum.py"), self.directory, raw)]
        return [
            ExerciseFile(str(item.get("name", "")), self.directory, dict(item))
            for item in self.raw.get("files", [])
            if isinstance(item, dict)
        ]

    def file(self, name: str) -> ExerciseFile | None:
        return next((item for item in self.files if item.name == name), None)

    @property
    def entry(self) -> str:
        """Çalıştırılan dosya: `entry` alanı, yoksa ilk dosya."""
        files = self.files
        return str(self.raw.get("entry") or (files[0].name if files else ""))

    def starter_files(self, language: str) -> dict[str, str]:
        return {item.name: item.starter_for(language) for item in self.files}

    def solution_files(self, language: str) -> dict[str, str]:
        return {item.name: item.solution_for(language) for item in self.files}

    def starter_code_for(self, language: str) -> str:
        return self._code_for("starter", language)

    def starter_variants(self) -> list[str]:
        """Bütün dillerdeki başlangıç kodları.

        Dil listesi dosya adlarından çıkarılıyor: `starter.{lang}.py`
        şablonu diskte hangi dillerde varsa o kadar. Böylece yeni bir dil
        eklendiğinde burası değişmeden çalışıyor.
        """
        name = self.raw.get("starter")
        if not name:
            return []
        if "{lang}" not in name:
            path = self.directory / name
            return [path.read_text(encoding="utf-8")] if path.exists() else []
        found = sorted(self.directory.glob(name.replace("{lang}", "*")))
        return [path.read_text(encoding="utf-8") for path in found]

    def is_untouched(self, code: str) -> bool:
        """Kod hâlâ başlangıç kodu mu — herhangi bir dilde.

        Kullanıcı bir alıştırmayı açıp hiçbir şey yazmadan çalıştırdığında
        başlangıç kodu "yazdığı kod" olarak kaydediliyor. Dil değişince o
        kaydın yorum satırları eski dilde kalıyordu; hangi dilin başlangıç
        kodu olursa olsun tanımak bunu çözüyor.
        """
        current = code.strip()
        if not current:
            return False
        return any(current == variant.strip() for variant in self.starter_variants())

    def solution_code_for(self, language: str) -> str:
        return self._code_for("solution", language)

    @property
    def starter_code(self) -> str:
        return self._code_for("starter", FALLBACK_LANGUAGE)

    @property
    def solution_code(self) -> str:
        return self._code_for("solution", FALLBACK_LANGUAGE)

    @classmethod
    def load(cls, directory: Path) -> "Exercise":
        raw = _read_json(directory / "exercise.json")
        exercise_id = raw.get("id") or directory.name
        return cls(id=exercise_id, directory=directory, raw=raw)


@dataclass
class Section:
    """Bir alt bölüm: ders, PDF, sınav ve alıştırmalardan oluşur."""

    id: str
    chapter_id: str
    directory: Path
    raw: dict
    blocks: list[Block] = field(default_factory=list)
    # `exercises` ilk erişimde bir kez okunuyor; bkz. oradaki not.
    _exercises: list | None = field(default=None, init=False, repr=False, compare=False)

    @property
    def title(self) -> dict[str, str]:
        return self.raw.get("title", {})

    @property
    def estimated_minutes(self) -> int:
        return int(self.raw.get("estimated_minutes", 0))

    @property
    def level(self) -> str:
        """Bölümün seviyesi: `basic` / `intermediate` / `advanced`.

        Boş bırakılabiliyor. Uzun bir patikada (SQL sıfırdan ileri seviyeye
        gidiyor) yol ekranı bölümleri bu alana göre başlıklar altında
        topluyor; alan yoksa liste eskisi gibi düz akıyor.
        """
        return str(self.raw.get("level", ""))

    @property
    def requires_quiz(self) -> bool:
        return bool(self.raw.get("completion", {}).get("require_quiz", False))

    @property
    def requires_exercises(self) -> bool:
        return bool(self.raw.get("completion", {}).get("require_exercises", False))

    def blocks_of(self, block_type: str) -> list[Block]:
        return [block for block in self.blocks if block.type == block_type]

    @property
    def exercises(self) -> list[Exercise]:
        """Bölümün alıştırmaları; dosyalardan **bir kez** okunuyor.

        Önceden her erişimde bütün `exercise.json` dosyaları baştan
        okunuyordu. Yol, rozet, rota ve ilerleme hesapları bunu bölüm
        başına tekrar tekrar çağırdığı için tek bir dil değişimi 1.103 dosya
        açıyordu; değişimin 352 ms'sinin 209 ms'si buydu (ölçüldü). İçerik
        uygulama çalışırken değişmiyor. Çağırana kopya veriliyor ki listeyi
        değiştiren biri önbelleği bozmasın.
        """
        if self._exercises is None:
            found = []
            for block in self.blocks_of("exercise"):
                directory = block.exercise_dir
                if directory and directory.exists():
                    found.append(Exercise.load(directory))
            self._exercises = found
        return list(self._exercises)

    @classmethod
    def load(cls, directory: Path, chapter_id: str) -> "Section":
        raw = _read_json(directory / "section.json")
        section_id = raw.get("id") or directory.name

        blocks = []
        for entry in raw.get("blocks", []):
            block_type = entry.get("type")
            if not block_type:
                raise ContentError(f"Türü olmayan blok: {directory / 'section.json'}")
            blocks.append(Block(type=block_type, raw=entry, directory=directory))

        return cls(
            id=section_id,
            chapter_id=chapter_id,
            directory=directory,
            raw=raw,
            blocks=blocks,
        )


@dataclass
class Chapter:
    """Bir modül: sırayla ilerlenen alt bölümlerden oluşur."""

    id: str
    directory: Path
    raw: dict
    sections: list[Section] = field(default_factory=list)

    @property
    def title(self) -> dict[str, str]:
        return self.raw.get("title", {})

    @property
    def description(self) -> dict[str, str]:
        return self.raw.get("description", {})

    @property
    def color(self) -> str:
        return self.raw.get("color", "#4F46E5")

    @property
    def icon(self) -> str:
        return self.raw.get("icon", "book")

    @property
    def short(self) -> dict[str, str]:
        """Sekmedeki kısa adı ("MAT 1"); yoksa tam başlık."""
        return self.raw.get("short") or self.title

    @property
    def planned(self) -> list[dict]:
        """Henüz yazılmamış ama yol üzerinde gösterilecek bölümler.

        Yalnızca başlık taşıyorlar; klasörleri yok, içerik doğrulayıcısı
        onlara bakmıyor ve ilerleme kaydı tutulmuyor. Amaç, modülün nereye
        gittiğini baştan göstermek.
        """
        return list(self.raw.get("planned", []))

    @property
    def outline(self) -> list:
        """Yol sırası: yazılmış bölümler (`Section`) ve planlananlar (sözlük).

        `chapter.json` içinde `outline` varsa ikisi o sırayla karışık
        diziliyor. Böylece bir modülün ortasındaki bir bölüm önceden
        yazılabiliyor (MAT 1'in logaritması gibi) ve yol yine doğru sırada
        görünüyor. `outline` yoksa eski davranış: önce yazılmışlar, sonra
        planlananlar.
        """
        order = self.raw.get("outline")
        if not order:
            return [*self.sections, *self.planned]
        written = {section.id: section for section in self.sections}
        planned = {entry.get("id"): entry for entry in self.planned}
        return [written.get(i) or planned[i] for i in order if i in written or i in planned]

    @classmethod
    def load(cls, directory: Path) -> "Chapter":
        raw = _read_json(directory / "chapter.json")
        chapter_id = raw.get("id") or directory.name

        # Sıra chapter.json'da açıkça yazılıdır; klasör sıralamasına güvenmiyoruz.
        # `outline` varsa yazılmış bölümler oradan, klasörü olanlar alınarak.
        section_ids = raw.get("sections")
        if section_ids is None and raw.get("outline"):
            section_ids = [
                i for i in raw["outline"] if (directory / i / "section.json").exists()
            ]
        if section_ids is None:
            section_ids = sorted(
                p.name for p in directory.iterdir()
                if p.is_dir() and (p / "section.json").exists()
            )

        sections = []
        for section_id in section_ids:
            section_dir = directory / section_id
            if not (section_dir / "section.json").exists():
                raise ContentError(
                    f"'{chapter_id}' bölümünde tanımlı ama bulunamayan alt bölüm: {section_id}"
                )
            sections.append(Section.load(section_dir, chapter_id))

        return cls(id=chapter_id, directory=directory, raw=raw, sections=sections)


@dataclass
class Track:
    """Bir öğrenme patikası: Python, Veri Bilimi, Makine Öğrenmesi, SQL.

    Modüllerin üstünde duran katman. Bir patikanın henüz modülü yoksa ana
    ekranda kilitli görünüyor — hangi konuların geleceğini baştan göstermek,
    "uygulamada bu kadarı var" izlenimini önlüyor.
    """

    id: str
    raw: dict
    chapters: list[Chapter] = field(default_factory=list)

    @property
    def title(self) -> dict[str, str]:
        return self.raw.get("title", {})

    @property
    def description(self) -> dict[str, str]:
        return self.raw.get("description", {})

    @property
    def color(self) -> str:
        return self.raw.get("color", "#4F46E5")

    @property
    def icon(self) -> str:
        return self.raw.get("icon", "book")

    @property
    def prerequisite(self) -> str:
        """Önce bitirilmesi önerilen patikanın kimliği; yoksa boş."""
        return self.raw.get("prerequisite", "")

    @property
    def locked(self) -> bool:
        """İçeriği henüz yazılmamış patika kilitli sayılıyor."""
        return not self.chapters

    @property
    def chapter_tabs(self) -> bool:
        """Modüller liste yerine sağ üstte sekme olarak mı gösteriliyor?

        Matematik patikasında MAT 1 ve MAT 2 birbirinin devamı; araya bir
        modül listesi koymak yerine patikaya girince MAT 1'in yolu açılıyor,
        MAT 2'ye başlıktaki seçiciden geçiliyor (Alican istedi).
        """
        return bool(self.raw.get("chapter_tabs"))


@dataclass
class Catalog:
    """Bütün müfredat."""

    chapters: list[Chapter] = field(default_factory=list)
    tracks: list[Track] = field(default_factory=list)

    @classmethod
    def load(cls, content_dir: Path) -> "Catalog":
        if not content_dir.exists():
            raise ContentError(f"İçerik klasörü bulunamadı: {content_dir}")

        directories = sorted(
            p for p in content_dir.iterdir()
            if p.is_dir() and (p / "chapter.json").exists()
        )
        chapters = [Chapter.load(p) for p in directories]
        return cls(chapters=chapters, tracks=cls._load_tracks(content_dir, chapters))

    @staticmethod
    def _load_tracks(content_dir: Path, chapters: list[Chapter]) -> list[Track]:
        """`tracks.json` varsa patikaları kurar.

        Dosya yoksa tek bir patika üretiliyor: eski davranış korunuyor ve
        ekran boş kalmıyor.
        """
        path = content_dir / "tracks.json"
        if not path.exists():
            return []

        by_id = {chapter.id: chapter for chapter in chapters}
        tracks: list[Track] = []
        for raw in _read_json(path).get("tracks", []):
            track_id = raw.get("id", "")
            secili = [
                by_id[cid] for cid in raw.get("chapters", []) if cid in by_id
            ]
            tracks.append(Track(id=track_id, raw=raw, chapters=secili))
        return tracks

    def track(self, track_id: str) -> Track | None:
        return next((t for t in self.tracks if t.id == track_id), None)

    def chapter(self, chapter_id: str) -> Chapter | None:
        return next((c for c in self.chapters if c.id == chapter_id), None)

    def section(self, chapter_id: str, section_id: str) -> Section | None:
        chapter = self.chapter(chapter_id)
        if chapter is None:
            return None
        return next((s for s in chapter.sections if s.id == section_id), None)

    @property
    def all_sections(self) -> list[Section]:
        """Bütün alt bölümler, müfredat sırasında."""
        return [section for chapter in self.chapters for section in chapter.sections]

    def neighbours(self, chapter_id: str, section_id: str) -> tuple[Section | None, Section | None]:
        """Verilen alt bölümün önceki ve sonraki komşusunu döndürür."""
        sections = self.all_sections
        for index, section in enumerate(sections):
            if section.chapter_id == chapter_id and section.id == section_id:
                previous = sections[index - 1] if index > 0 else None
                following = sections[index + 1] if index + 1 < len(sections) else None
                return previous, following
        return None, None
