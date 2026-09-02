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

FALLBACK_LANGUAGE = "tr"


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


@dataclass
class Exercise:
    """Tek bir kod alıştırması."""

    id: str
    directory: Path
    raw: dict

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

        Dosya adında `{lang}` varsa kullanıcının diline göre çözülür; yorum
        satırları böylece okunabilir kalıyor. İstenen dil yoksa Türkçesine
        düşülür.
        """
        name = self.raw.get(key)
        if not name:
            return ""

        if "{lang}" in name:
            wanted = self.directory / name.replace("{lang}", language)
            if wanted.exists():
                return wanted.read_text(encoding="utf-8")
            name = name.replace("{lang}", FALLBACK_LANGUAGE)

        path = self.directory / name
        return path.read_text(encoding="utf-8") if path.exists() else ""

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

    @property
    def title(self) -> dict[str, str]:
        return self.raw.get("title", {})

    @property
    def estimated_minutes(self) -> int:
        return int(self.raw.get("estimated_minutes", 0))

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
        found = []
        for block in self.blocks_of("exercise"):
            directory = block.exercise_dir
            if directory and directory.exists():
                found.append(Exercise.load(directory))
        return found

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
    def planned(self) -> list[dict]:
        """Henüz yazılmamış ama yol üzerinde gösterilecek bölümler.

        Yalnızca başlık taşıyorlar; klasörleri yok, içerik doğrulayıcısı
        onlara bakmıyor ve ilerleme kaydı tutulmuyor. Amaç, modülün nereye
        gittiğini baştan göstermek.
        """
        return list(self.raw.get("planned", []))

    @classmethod
    def load(cls, directory: Path) -> "Chapter":
        raw = _read_json(directory / "chapter.json")
        chapter_id = raw.get("id") or directory.name

        # Sıra chapter.json'da açıkça yazılıdır; klasör sıralamasına güvenmiyoruz.
        section_ids = raw.get("sections")
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
