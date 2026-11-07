"""İçerikteki tanım dosyalarını (`badges.json`, `tags.json`) bir kez okur.

Açılışta rozet ve unvan tanımları farklı yerlerden 6 ve 4 kez okunuyordu
(7 Kasım ölçüldü); soğuk açılışta her okuma diske gidiyor. İçerik program
çalışırken değişmiyor; anahtarda dosyanın değişme zamanı da var, test
betiklerinin yazdığı geçici dosya yine okunsun diye. Çağırana kopya veriliyor
ki listeyi ya da bir tanımı değiştiren biri önbelleği bozmasın.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

_okunan: dict[tuple[str, int, str], list] = {}


def read_list(path: Path, key: str) -> list[dict]:
    """`path` JSON'undaki `key` listesi; dosya yoksa boş liste."""
    try:
        degisme = path.stat().st_mtime_ns
    except FileNotFoundError:
        return []
    anahtar = (str(path), degisme, key)
    if anahtar not in _okunan:
        with path.open(encoding="utf-8") as handle:
            _okunan[anahtar] = json.load(handle).get(key, [])
    return copy.deepcopy(_okunan[anahtar])
