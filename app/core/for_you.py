"""Öğrenme Yolu'nun "Senin için" şeridi: en çok üç patika (taslak 1, 17 Kasım).

Sıra: (a) en son çalışılan başlanmış patika, (b) yeni patika, (c) seçili
rotada sıradaki patika. Boş kalan yerler başka başlanmış patikalarla (son
çalışılan önde), o da yoksa rotanın sonraki adımlarıyla doluyor. Aynı patika
iki kez girmiyor; zaten seçilmiş bir patika rotada sıradakiyse kartına o
etiket de ekleniyor. Kilitli patikaları çağıran listelere koymuyor.

Rota adımının durumu (`step_state`) ve "Sıradaki" kuralı (`next_step_index`)
Rotalar ekranınınkiyle aynı: yazılmamış (kilitli), bitmiş ve isteğe bağlı
adımlar atlanıyor.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .completion import is_completed

LIMIT = 3

# Kart etiketleri.
STARTED = "started"
NEW = "new"
ROUTE_NEXT = "route_next"
ROUTE_LATER = "route"


@dataclass
class Pick:
    track_id: str
    tags: list[str] = field(default_factory=list)


def pick(started: list[str], new: list[str], route_next: str | None, route_later: list[str],
         limit: int = LIMIT) -> list[Pick]:
    """Seçim; `started` son çalışılan önde, `route_later` rota sırasıyla."""
    secilen: dict[str, Pick] = {}

    def ekle(track_id: str | None, tag: str) -> None:
        if not track_id:
            return
        if track_id in secilen:
            if tag == ROUTE_NEXT:
                secilen[track_id].tags.append(tag)
            return
        if len(secilen) < limit:
            secilen[track_id] = Pick(track_id, [tag])

    ekle(started[0] if started else None, STARTED)
    ekle(new[0] if new else None, NEW)
    ekle(route_next, ROUTE_NEXT)
    for track_id in started[1:]:
        ekle(track_id, STARTED)
    for track_id in route_later:
        ekle(track_id, ROUTE_LATER)
    return list(secilen.values())


def order_started(track_ids: list[str], last: str | None, latest: dict[str, str | None]) -> list[str]:
    """Başlanmış patikalar yakınlığa göre: son ziyaret edilen bölümün patikası
    önde, sonra en son bölüm bitirilen; eşitlikte gelen sıra korunuyor."""
    sirali = sorted(track_ids, key=lambda kimlik: latest.get(kimlik) or "", reverse=True)
    if last in sirali:
        sirali.remove(last)
        sirali.insert(0, last)
    return sirali


# --- rota ---------------------------------------------------------------------

def route_for(routes: list[dict], route_id: str) -> dict | None:
    """Seçili rota; seçilmemişse ya da artık yoksa Rotalar ekranı gibi ilki."""
    for route in routes:
        if route.get("id") == route_id:
            return route
    return routes[0] if routes else None


def _ref(entry) -> str:
    return entry.get("ref", "") if isinstance(entry, dict) else str(entry)


def step_state(catalog, store, step: dict, active) -> dict:
    """Adımın durumu: yazılmış mı, kaç bölümün kaçı bitti (Rotalar ekranıyla aynı)."""
    track = catalog.track(step.get("track", ""))
    if track is None or track.locked:
        return {"soon": True, "done": False, "completed": 0, "total": 0}
    if step.get("sections"):
        sections = [catalog.section(*_ref(entry).split("/", 1)) for entry in step["sections"]]
        sections = [section for section in sections if section is not None]
    else:
        sections = [s for chapter in track.chapters for s in chapter.sections]
    completed = sum(1 for section in sections if is_completed(store, section, active))
    total = len(sections)
    return {
        "soon": False,
        "done": total > 0 and completed == total,
        "completed": completed,
        "total": total,
        "minutes": sum(section.estimated_minutes for section in sections),
    }


def _waiting(step: dict, state: dict) -> bool:
    """Kimsenin bekletilmemesi gereken adımlar değil: yazılmış, bitmemiş, zorunlu."""
    return not state["soon"] and not state["done"] and not step.get("optional")


def next_step_index(steps: list[dict], states: list[dict]) -> int:
    """"Sıradaki" adım: bitmemiş ilk zorunlu, yazılmış adım; yoksa -1."""
    return next((i for i, (step, state) in enumerate(zip(steps, states)) if _waiting(step, state)), -1)


def route_tracks(catalog, store, route: dict | None) -> tuple[str | None, list[str]]:
    """Rotada sıradaki patika ve ondan sonraki bekleyen adımların patikaları."""
    if not route:
        return None, []
    steps = route.get("steps", [])
    active = store.active_sections()
    states = [step_state(catalog, store, step, active) for step in steps]
    sira = next_step_index(steps, states)
    if sira < 0:
        return None, []
    siradaki = steps[sira].get("track")
    sonraki: list[str] = []
    for step, state in zip(steps[sira + 1:], states[sira + 1:]):
        kimlik = step.get("track")
        if _waiting(step, state) and kimlik != siradaki and kimlik not in sonraki:
            sonraki.append(kimlik)
    return siradaki, sonraki
