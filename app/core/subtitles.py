"""Videonun kendi altyazıları (SRT).

YouTube'un gömülü oynatıcısına dışarıdan altyazı verilemiyor; otomatik
Türkçe çevirisi de gömülü oynatıcıda görünmüyor (22 Ekim, ölçüldü). CS50'nin
İngilizce altyazısı ve bizim Türkçe çevirimiz bölüm klasöründe SRT dosyası
olarak duruyor (`section.json` → video bloğu → `subtitles`); sayfa onları
oynatıcının o anki saniyesine göre videonun üstüne kendisi yazıyor.
"""

from __future__ import annotations

import re
from pathlib import Path

Cue = tuple[float, float, str]

_TIME = re.compile(r"(\d+):(\d\d):(\d\d)[,.](\d{1,3})")
_ARROW = re.compile(rf"^\s*{_TIME.pattern}\s*-->\s*{_TIME.pattern}")


def _seconds(h: str, m: str, s: str, ms: str) -> float:
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms.ljust(3, "0")) / 1000


def parse_srt(text: str) -> list[Cue]:
    """SRT metnini `(başlangıç, bitiş, yazı)` listesine çevirir.

    Boş yazılı ya da bozuk zamanlı satırlar atlanıyor (CS50'nin dosyalarında
    başta ve sonda boş altyazı var); sıra başlangıca göre."""
    cues: list[Cue] = []
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n").replace("\r", "\n").lstrip("﻿")):
        lines = block.strip("\n").split("\n")
        for i, line in enumerate(lines):
            match = _ARROW.match(line)
            if not match:
                continue
            g = match.groups()
            start, end = _seconds(*g[:4]), _seconds(*g[4:])
            body = "\n".join(part.strip() for part in lines[i + 1:] if part.strip())
            if body and end > start:
                cues.append((start, end, body))
            break
    return sorted(cues, key=lambda cue: cue[0])


def load(path: Path) -> list[Cue]:
    """Dosyadan okur; dosya yoksa ya da okunamıyorsa boş liste."""
    try:
        return parse_srt(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return []
