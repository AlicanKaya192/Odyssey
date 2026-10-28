"""Haftalık hedef: her gün çalışamayan için serinin yanında (Alican, 27 Ekim).

Hafta Pazartesi başlıyor (yerel saat). Kişi türünü kendisi seçiyor: biten
bölüm, odak dakikası (çalışma zamanlayıcısı) ya da çalışma günü (serinin
saydığı gün). İlerleme rozetler ve XP gibi **hesaplanıyor, saklanmıyor**;
ayarlarda yalnızca tür, hedef ve hedefin hangi hafta kutlandığı duruyor
(kutlama kartı haftada bir kez çıksın). Varsayılan kapalı.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

KIND_KEY = "weekly_goal_kind"  # "" = kapalı
TARGET_KEY = "weekly_goal_target"
CELEBRATED_KEY = "weekly_goal_celebrated"  # kutlanan hafta, "2026-W44"

KINDS = ("sections", "focus", "days")
# Ayarlardaki seçenekler; odak dakika cinsinden.
TARGETS = {
    "sections": (1, 2, 3, 4, 5, 6, 8, 10),
    "focus": (30, 60, 90, 120, 180, 240, 300, 420, 600),
    "days": (1, 2, 3, 4, 5, 6, 7),
}
DEFAULT_TARGET = {"sections": 3, "focus": 120, "days": 4}
# Geçmiş bu kadar haftaya bakıyor (seri ve en uzun); profilde son `RECENT_WEEKS`.
HISTORY_WEEKS = 104
RECENT_WEEKS = 12


@dataclass(frozen=True)
class Goal:
    kind: str
    target: int
    done: int

    @property
    def reached(self) -> bool:
        return self.done >= self.target


def week_start(today: date) -> date:
    return today - timedelta(days=today.weekday())


def week_key(today: date) -> str:
    yil, hafta, _ = today.isocalendar()
    return f"{yil}-W{hafta:02d}"


def _setting(store) -> tuple[str, int] | None:
    kind = store.setting(KIND_KEY, "")
    if kind not in KINDS:
        return None
    try:
        target = int(store.setting(TARGET_KEY, ""))
    except ValueError:
        target = DEFAULT_TARGET[kind]
    if target not in TARGETS[kind]:
        target = DEFAULT_TARGET[kind]
    return kind, target


def current(store, today: date | None = None) -> Goal | None:
    """Bu haftanın durumu; hedef kapalıysa `None`."""
    ayar = _setting(store)
    if ayar is None:
        return None
    today = today or date.today()
    kind, target = ayar
    return Goal(kind, target, store.week_totals(week_start(today))[kind])


def set_goal(store, kind: str, target: int, today: date | None = None) -> None:
    """Hedefi kaydeder (`kind` boşsa kapatır).

    Hedef konduğu anda zaten tutmuşsa bu hafta kutlanmış sayılıyor: ayarı
    değiştiren kişinin önüne hemen kart düşmesin.
    """
    store.set_setting(KIND_KEY, kind if kind in KINDS else "")
    if kind not in KINDS:
        return
    store.set_setting(TARGET_KEY, str(target))
    today = today or date.today()
    goal = current(store, today)
    if goal is not None and goal.reached:
        store.set_setting(CELEBRATED_KEY, week_key(today))


@dataclass(frozen=True)
class History:
    """Hedefin geçmişi: üst üste tutan hafta (seri gibi), en uzunu ve son
    haftalar (eskiden yeniye, sonuncusu bu hafta)."""

    streak: int
    best: int
    recent: tuple[bool, ...]


def history(store, today: date | None = None, weeks: int = HISTORY_WEEKS) -> History | None:
    """Bugünkü hedefle geçmiş haftalar; hedef kapalıysa `None`.

    Geçmiş de bugünkü tür ve sayıyla ölçülüyor (hedef saklanmıyor,
    hesaplanıyor). Süren hafta tutmadıysa seriyi bozmuyor: hafta henüz
    bitmedi, seri geçen haftadan sayılıyor.
    """
    ayar = _setting(store)
    if ayar is None:
        return None
    kind, target = ayar
    bu_hafta = week_start(today or date.today())
    tuttu = []  # yeniden eskiye
    for geri in range(weeks):
        bas = bu_hafta - timedelta(weeks=geri)
        tuttu.append(store.week_totals(bas, bas + timedelta(weeks=1))[kind] >= target)
    seri = 0
    for hafta in (tuttu if tuttu[0] else tuttu[1:]):
        if not hafta:
            break
        seri += 1
    en_uzun = sure = 0
    for hafta in tuttu:
        sure = sure + 1 if hafta else 0
        en_uzun = max(en_uzun, sure)
    return History(seri, en_uzun, tuple(reversed(tuttu[:RECENT_WEEKS])))


def celebrate(store, today: date | None = None) -> Goal | None:
    """Hedef bu hafta ilk kez tuttuysa onu döndürür ve kutlandı diye yazar."""
    today = today or date.today()
    goal = current(store, today)
    if goal is None or not goal.reached or store.setting(CELEBRATED_KEY, "") == week_key(today):
        return None
    store.set_setting(CELEBRATED_KEY, week_key(today))
    return goal
