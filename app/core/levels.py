"""Seviye, deneyim puanı (XP) ve unvanlar.

XP iki yerden geliyor: tamamlanan her bölüm ve kazanılan her rozet. Rozet
bölümden fazla veriyor ve her rozetin puanı farklı (`content/badges.json`
→ `xp`): zor ve uzun süren rozet daha çok.

XP **hesaplanıyor, saklanmıyor** (rozetler gibi): biten bölüm sayısı ile
kayıtlı rozetlerden her seferinde yeniden toplanıyor. Böylece seviye sistemi
gelmeden önce çalışmış olan da hak ettiği seviyeden başlıyor, geriye dönük
bir göç gerekmiyor.

Seviye atlamak için gereken XP her seviyede artıyor. Unvanlar belirli
seviyelerde, bir patikanın tamamı bitince ve birkaç zor koşulda açılıyor.
Adları ve "nasıl kazanılır" metinleri `content/tags.json` içinde, koşulları
burada (rozetlerdeki ayrımın aynısı). Kazanılmış unvan geri alınmıyor:
kimlikleri `tags_earned` ayarında duruyor (seri bozulsa da unvan kalıyor).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from . import badges

# Tamamlanan her bölümün verdiği puan.
SECTION_XP = 60
# Rozetin `xp` alanı yoksa kademesine göre.
TIER_XP = {"bronze": 100, "silver": 200, "gold": 400, "legendary": 1000}

MAX_LEVEL = 50
# Bir sonraki seviye için gereken XP: 1 → 2 için 100, her seviyede 40 artıyor.
FIRST_STEP = 100
STEP_GROWTH = 40

SEEN_LEVEL_KEY = "level_seen"
EARNED_TAGS_KEY = "tags_earned"
SELECTED_TAG_KEY = "profile_tag"

# Unvan kimliği → gereken seviye.
LEVEL_TAGS = {
    "student": 5,
    "thinker": 10,
    "philosopher": 15,
    "sage": 20,
    "mentor": 25,
    "athena": 30,
    "prometheus": 40,
    "olympian": 50,
}
# Unvan kimliği → gereken rozet (patikanın tamamı).
BADGE_TAGS = {
    "snake-charmer": "python-complete",
    "data-hunter": "data-explorer",
    "oracle": "ml-complete",
    "query-master": "sql-complete",
    "time-bender": "ts-complete",
    "bridge-builder": "api-complete",
    "gatekeeper": "api2-complete",
    "harbor-master": "docker-complete",
    "record-keeper": "git-complete",
    "deep-diver": "bigdata-complete",
}
MATH_CHAPTERS = ("04-temel-matematik", "05-ileri-matematik")
TIRELESS_EXERCISES = 200
DEVOTED_STREAK = 30


def xp_for_next(level: int) -> int:
    """`level`'den bir sonrakine geçmek için gereken XP; son seviyede 0."""
    if level >= MAX_LEVEL:
        return 0
    return FIRST_STEP + STEP_GROWTH * (level - 1)


def total_for_level(level: int) -> int:
    """`level`'e ulaşmak için baştan beri gereken toplam XP."""
    return sum(xp_for_next(k) for k in range(1, min(level, MAX_LEVEL)))


@dataclass(frozen=True)
class LevelState:
    xp: int       # toplam
    level: int
    into: int     # bu seviyenin içinde kazanılan
    need: int     # bu seviyeyi bitirmek için gereken (son seviyede 0)

    @property
    def ratio(self) -> float:
        return 1.0 if not self.need else min(1.0, self.into / self.need)


def level_state(xp: int) -> LevelState:
    level, kalan = 1, max(0, int(xp))
    while level < MAX_LEVEL and kalan >= xp_for_next(level):
        kalan -= xp_for_next(level)
        level += 1
    return LevelState(xp=max(0, int(xp)), level=level, into=kalan, need=xp_for_next(level))


def badge_xp(tanim: dict) -> int:
    """Bir rozetin verdiği XP."""
    deger = tanim.get("xp")
    if isinstance(deger, int) and deger > 0:
        return deger
    kademe = (tanim.get("medal") or ["circle", "bronze"])[-1]
    return TIER_XP.get(kademe, TIER_XP["bronze"])


def load_tags(path) -> list[dict]:
    """`content/tags.json` dosyasını okur."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return json.load(handle).get("tags", [])


def _tag_conditions(catalog, store, level: int, rozetler: set[str],
                    bitenler: set[tuple[str, str]], rozet_sayisi: int) -> set[str]:
    """Koşulu şu anda sağlanan unvanlar."""
    acik = {tag for tag, gereken in LEVEL_TAGS.items() if level >= gereken}
    acik |= {tag for tag, rozet in BADGE_TAGS.items() if rozet in rozetler}

    dolu = [c for c in catalog.chapters if c.sections]

    def tamam(chapter) -> bool:
        return all((chapter.id, s.id) in bitenler for s in chapter.sections)

    matematik = [c for c in dolu if c.id in MATH_CHAPTERS]
    if len(matematik) == len(MATH_CHAPTERS) and all(tamam(c) for c in matematik):
        acik.add("mathematician")
    if dolu and all(tamam(c) for c in dolu):
        acik.add("odysseus")
    if rozet_sayisi and len(rozetler) >= rozet_sayisi:
        acik.add("collector")
    if store.solved_exercise_count() >= TIRELESS_EXERCISES:
        acik.add("tireless")
    if store.streak() >= DEVOTED_STREAK:
        acik.add("devoted")
    return acik


@dataclass(frozen=True)
class Update:
    """`refresh` çağrısının sonucu."""

    state: LevelState
    tags: frozenset = frozenset()          # kazanılmış unvanların kimlikleri
    leveled_up: bool = False               # son bakıştan beri seviye arttı mı
    new_tags: tuple = field(default=())    # bu çağrıda açılan unvanlar (tanımlar)


def refresh(catalog, store, content_dir, done: set | None = None,
            record: bool = True) -> Update:
    """XP'yi, seviyeyi ve unvanları hesaplar; yeni olanları kaydeder.

    Rozetler kaydedildikten **sonra** çağrılmalı (`badges.award_new` ya da
    `badges.collect`): XP kayıtlı rozetlerden toplanıyor.

    İlk çağrıda (ayar yokken) seviye ve unvanlar sessizce kaydediliyor:
    sistem gelmeden önce çalışmış birine açılışta on kutlama kartı birden
    çıkmasın.

    `record=False` hiçbir şey kaydetmiyor (profil ekranı): seviye atlama ve
    yeni unvan, kutlama kartını çıkaran ana pencereye kalıyor.
    """
    if done is None:
        done = badges.completed_sections(catalog, store)
    tanimlar = badges.load_definitions(content_dir / "badges.json")
    rozetler = set(store.earned_badges())
    xp = len(done) * SECTION_XP + sum(
        badge_xp(t) for t in tanimlar if t.get("id") in rozetler
    )
    state = level_state(xp)

    kayit = store.setting(SEEN_LEVEL_KEY, None)
    try:
        gorulen = int(kayit) if kayit is not None else None
    except ValueError:
        gorulen = None
    atladi = gorulen is not None and state.level > gorulen
    if record and (gorulen is None or state.level != gorulen):
        store.set_setting(SEEN_LEVEL_KEY, str(state.level))

    unvanlar = load_tags(content_dir / "tags.json")
    bilinen = {u.get("id", "") for u in unvanlar}
    acik = _tag_conditions(catalog, store, state.level, rozetler, done, len(tanimlar)) & bilinen
    kayit = store.setting(EARNED_TAGS_KEY, None)
    onceki = set(filter(None, kayit.split(","))) if kayit is not None else None
    hepsi = acik | (onceki or set())
    yeni: tuple = ()
    if record and (onceki is None or hepsi != onceki):
        store.set_setting(EARNED_TAGS_KEY, ",".join(sorted(hepsi)))
        if onceki is not None:
            yeni = tuple(u for u in unvanlar if u.get("id") in hepsi - onceki)

    return Update(state=state, tags=frozenset(hepsi & bilinen), leveled_up=atladi, new_tags=yeni)


def selected_tag(store, earned) -> str:
    """Profilde gösterilen unvanın kimliği; seçilmemişse ya da artık
    listede yoksa boş."""
    secili = store.setting(SELECTED_TAG_KEY, "")
    return secili if secili in earned else ""


def select_tag(store, tag_id: str) -> None:
    store.set_setting(SELECTED_TAG_KEY, tag_id)
