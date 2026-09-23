"""Seri hatırlatmaları: ne zaman, hangi bildirim gidecek.

Program kapalıyken de çalışıyor. Windows Görev Zamanlayıcı günde bir iki kez
`Odyssey --reminder-check` çağırıyor (`reminder_task.py`); o çağrı buradaki
`run_check`'i çalıştırıp gerekirse bir Windows bildirimi gösteriyor ve
kapanıyor. Arka planda sürekli açık kalan bir süreç yok, ağa hiçbir şey
gitmiyor.

Kurallar:

- Seçilen saatten (`reminder_time`, varsayılan 19:00) önce hiçbir şey
  gönderilmiyor.
- Bugün çalışıldıysa hiçbir şey gönderilmiyor.
- **Seri canlıysa** (en son dün çalışılmış): seçilen saatte "seri tehlikede",
  21:30'da hâlâ çalışılmadıysa "son çağrı".
- **Seri bittiyse** ne kadar uzun süredir yoksa o kadar seyrek: 2–7 gün her
  gün, 8–30 gün üç günde bir, 31–59 gün haftada bir. 60. günde bir kez
  "artık rahatsız etmeyeceğim" deyip susuyor (Duolingo'nun yaptığı gibi);
  kişi dönüp yeniden kaybolursa döngü baştan başlıyor.
- **Hiç çalışmamış** biri için iki günde bir, en fazla üç kez.
- Günde en fazla bir bildirim (son çağrı hariç).

Metinler `app/resources/reminders.json` içinde, her türün birkaç çeşidi var;
art arda aynısı çıkmasın diye son gösterilen saklanıyor.
"""

from __future__ import annotations

import json
import random
from datetime import date, datetime, time

from ..paths import install_root

# Ayar anahtarları.
ENABLED_KEY = "reminders"          # "1" açık, "0" kapalı, "" henüz sorulmadı
TIME_KEY = "reminder_time"         # "SS:DD"
LAST_DAY_KEY = "reminder_last_day"
LAST_KIND_KEY = "reminder_last_kind"
LAST_VARIANT_KEY = "reminder_last_variant"
NEVER_COUNT_KEY = "reminder_never_count"
GOODBYE_KEY = "reminder_goodbye"   # vedanın hangi yokluk için yapıldığı

DEFAULT_TIME = "19:00"
LAST_CALL = time(21, 30)
NEVER_LIMIT = 3

# (en çok gün, tür, kaç günde bir)
AWAY_STEPS = (
    (3, "away_short", 1),
    (7, "away_week", 1),
    (30, "away_long", 3),
    (59, "away_very_long", 7),
)
GOODBYE_AFTER = 60


def asked(store) -> bool:
    """Kullanıcıya hatırlatma isteyip istemediği soruldu mu?"""
    return store.setting(ENABLED_KEY, "") in ("0", "1")


def enabled(store) -> bool:
    return store.setting(ENABLED_KEY, "") == "1"


def reminder_time(store) -> time:
    try:
        saat, dakika = store.setting(TIME_KEY, DEFAULT_TIME).split(":")
        return time(int(saat), int(dakika))
    except (ValueError, TypeError):
        return time(19, 0)


def decide(store, now: datetime) -> str | None:
    """Şu an gönderilecek bildirimin türü; gönderilecek bir şey yoksa None."""
    if not enabled(store):
        return None
    secilen = reminder_time(store)
    if now.time() < secilen:
        return None

    today = now.date()
    son_calisma = store.last_study_day()
    if son_calisma == today:
        return None

    son_gonderim = store.setting(LAST_DAY_KEY, "")
    bugun_gitti = son_gonderim == today.isoformat()
    son_tur = store.setting(LAST_KIND_KEY, "")

    # Seri canlı: en son dün çalışılmış.
    if store.streak() > 0:
        gec = now.time() >= LAST_CALL and secilen < LAST_CALL
        if not bugun_gitti:
            return "streak_last_call" if gec else "streak_risk"
        if gec and son_tur == "streak_risk":
            return "streak_last_call"
        return None

    if bugun_gitti:
        return None

    gecen = _days_since(son_gonderim, today)

    if son_calisma is None:
        if int(store.setting(NEVER_COUNT_KEY, "0") or 0) >= NEVER_LIMIT:
            return None
        return "never" if gecen >= 2 else None

    yok = (today - son_calisma).days
    if yok >= GOODBYE_AFTER:
        # Veda bu yokluk için bir kez; kişi dönüp yeniden kaybolursa
        # (son çalışma günü değişir) hatırlatmalar yeniden başlıyor.
        if store.setting(GOODBYE_KEY, "") == son_calisma.isoformat():
            return None
        return "goodbye"
    for en_cok, tur, aralik in AWAY_STEPS:
        if yok <= en_cok:
            return tur if gecen >= aralik else None
    return None


def _days_since(iso_day: str, today: date) -> int:
    try:
        return (today - date.fromisoformat(iso_day)).days
    except ValueError:
        return 10_000


def _messages() -> dict:
    path = install_root() / "app" / "resources" / "reminders.json"
    return json.loads(path.read_text(encoding="utf-8"))


def compose(
    store,
    kind: str,
    now: datetime,
    section_title: str = "",
    rng: random.Random | None = None,
) -> tuple[str, str, int]:
    """Bildirimin başlığı, metni ve seçilen çeşidin sırası.

    Aynı tür art arda geldiğinde bir önceki çeşit seçilmiyor.
    """
    rng = rng or random.Random()
    dil = store.setting("language", "tr")
    dil = dil if dil in ("tr", "en") else "tr"
    cesitler = _messages()[kind][dil]

    onceki = -1
    if store.setting(LAST_KIND_KEY, "") == kind:
        try:
            onceki = int(store.setting(LAST_VARIANT_KEY, "-1"))
        except ValueError:
            onceki = -1
    adaylar = [i for i in range(len(cesitler)) if i != onceki] or [0]
    secim = rng.choice(adaylar)

    ad = (store.profile().get("first_name") or "").strip()
    son = store.last_study_day()
    degerler = {
        "name": ad or ("dostum" if dil == "tr" else "friend"),
        "streak": store.streak(),
        "days": (now.date() - son).days if son else 0,
        "section": section_title or ("ilk bölüm" if dil == "tr" else "the first section"),
    }
    baslik, metin = cesitler[secim]
    return baslik.format(**degerler), metin.format(**degerler), secim


def record_sent(store, kind: str, variant: int, now: datetime) -> None:
    store.set_setting(LAST_DAY_KEY, now.date().isoformat())
    store.set_setting(LAST_KIND_KEY, kind)
    store.set_setting(LAST_VARIANT_KEY, str(variant))
    if kind == "never":
        sayi = int(store.setting(NEVER_COUNT_KEY, "0") or 0)
        store.set_setting(NEVER_COUNT_KEY, str(sayi + 1))
    if kind == "goodbye":
        son = store.last_study_day()
        store.set_setting(GOODBYE_KEY, son.isoformat() if son else "")


def last_section_title(store, catalog) -> str:
    """{section} yerine yazılacak ad: kaldığı bölüm, yoksa ilk bölüm."""
    dil = store.setting("language", "tr")
    son = store.last_visited()
    bolum = catalog.section(*son) if son else None
    if bolum is None and catalog.all_sections:
        bolum = catalog.all_sections[0]
    if bolum is None:
        return ""
    return bolum.title.get(dil) or bolum.title.get("tr", "")


def run_check(store, now: datetime, show, catalog=None) -> str | None:
    """Karar ver, gerekiyorsa `show(title, body)` ile göster ve kaydet.

    `show` gösterimin başarılı olup olmadığını döndürüyor; başarısızsa
    kayıt yapılmıyor ki bir sonraki çalışmada yeniden denensin.
    """
    kind = decide(store, now)
    if kind is None:
        return None
    baslik_bolum = last_section_title(store, catalog) if catalog is not None else ""
    title, body, variant = compose(store, kind, now, baslik_bolum)
    if not show(title, body):
        return None
    record_sent(store, kind, variant, now)
    return kind
