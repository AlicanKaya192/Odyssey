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

    def file_for(self, language: str) -> LocalizedFile | None:
        template = self.raw.get("file")
        if not template:
            return None
        return resolve_localized(self.directory, template, language)

    @property
    def exercise_dir(self) -> Path | None:
        relative = self.raw.get("dir")
        return self.directory / relative if relative else None


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

    @property
    def starter_code(self) -> str:
        name = self.raw.get("starter")
        if not name:
            return ""
        path = self.directory / name
        return path.read_text(encoding="utf-8") if path.exists() else ""

    @property
    def solution_code(self) -> str:
        name = self.raw.get("solution")
        if not name:
            return ""
        path = self.directory / name
        return path.read_text(encoding="utf-8") if path.exists() else ""

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
class Catalog:
    """Bütün müfredat."""

    chapters: list[Chapter] = field(default_factory=list)

    @classmethod
    def load(cls, content_dir: Path) -> "Catalog":
        if not content_dir.exists():
            raise ContentError(f"İçerik klasörü bulunamadı: {content_dir}")

        directories = sorted(
            p for p in content_dir.iterdir()
            if p.is_dir() and (p / "chapter.json").exists()
        )
        return cls(chapters=[Chapter.load(p) for p in directories])

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
