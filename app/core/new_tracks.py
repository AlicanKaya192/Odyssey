"""Yeni patika: Öğrenme Yolu'nda hangi patika parlıyor (taslak 1, 17 Kasım).

`tracks.json`'da patikanın isteğe bağlı `since` alanı ("1.8.0") geldiği
sürümü söylüyor. Patika şu dört şart birlikte tutunca "yeni" sayılıyor:

- `since`'in orta sürümü (1.8) çalışan programınkiyle aynı; 1.9'a geçince
  kendiliğinden sönüyor.
- Kişi o patikayı hiç açmamış (ilk açılışta kalıcı olarak sönüyor) ve
  patikada etkinliği yok.
- Kişi patikayı ilk gördüğünden bu yana `GLOW_DAYS` günden az geçmiş. İlk
  görülme tarihi ayara yazılıyor; güncellemeyi iki hafta sonra açan da
  kendi iki haftasını görüyor.
- İlk kurulum değil: ilk kurulumda o an var olan bütün patikalar görülmüş
  sayılıyor (yeni gelen biri için her şey yeni, işaret bir şey söylemez).

Durum yalnızca `setting` / `set_setting` ile tutuluyor.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from datetime import date

SEEN_SETTING = "track_first_seen"    # {"deep-learning": "2026-11-17" | "install"}
OPENED_SETTING = "tracks_opened"     # ["deep-learning", ...]
GLOW_DAYS = 14
# İlk kurulumda var olan patikanın ilk görülme değeri: hiç yeni sayılmaz.
INSTALL = "install"


def minor_of(version: str) -> tuple[int, int] | None:
    """"1.8.2" → (1, 8); okunamazsa `None`."""
    parcalar = (version or "").split(".")
    try:
        return int(parcalar[0]), int(parcalar[1])
    except (IndexError, ValueError):
        return None


def is_new(since: str, app_version: str, first_seen: str | None, opened: bool, today: date) -> bool:
    """Tek bir patika için kural; `first_seen` ayardaki değer (yoksa `None`)."""
    if not since or opened or first_seen in (None, INSTALL):
        return False
    surum = minor_of(since)
    if surum is None or surum != minor_of(app_version):
        return False
    try:
        gorulme = date.fromisoformat(first_seen)
    except ValueError:
        return False
    return (today - gorulme).days < GLOW_DAYS


def _read(store, key: str, default):
    """Ayardaki JSON; yoksa ya da bozuksa `default`."""
    try:
        deger = json.loads(store.setting(key, "") or "null")
    except json.JSONDecodeError:
        return default
    return deger if isinstance(deger, type(default)) else default


def opened(store) -> set[str]:
    return {kimlik for kimlik in _read(store, OPENED_SETTING, []) if isinstance(kimlik, str)}


def mark_opened(store, track_id: str) -> bool:
    """Patikanın açıldığını kalıcı olarak yazar; ilk açılışta `True`."""
    acilan = opened(store)
    if track_id in acilan:
        return False
    store.set_setting(OPENED_SETTING, json.dumps(sorted(acilan | {track_id})))
    return True


def refresh(store, tracks: Iterable[tuple[str, str]], app_version: str, today: date,
            first_install: bool, started: set[str]) -> set[str]:
    """Bugün yeni sayılan patikalar; ilk görülme tarihlerini de yazar.

    `tracks`: (kimlik, since) çiftleri. Tarih yalnızca orta sürüm tuttuğunda
    yazılıyor: 1.7'deki bir kayıt 1.8'in iki haftasını önceden harcamasın.
    """
    gorulen = {k: v for k, v in _read(store, SEEN_SETTING, {}).items() if isinstance(v, str)}
    acilan = opened(store) | set(started)
    surum = minor_of(app_version)
    degisti = False
    yeni: set[str] = set()
    for kimlik, since in tracks:
        if not since:
            continue
        if kimlik not in gorulen:
            if first_install:
                gorulen[kimlik] = INSTALL
                degisti = True
            elif surum is not None and minor_of(since) == surum:
                gorulen[kimlik] = today.isoformat()
                degisti = True
        if is_new(since, app_version, gorulen.get(kimlik), kimlik in acilan, today):
            yeni.add(kimlik)
    if degisti:
        store.set_setting(SEEN_SETTING, json.dumps(gorulen, sort_keys=True))
    return yeni
