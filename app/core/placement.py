"""Seviye tespit sınavı: bildiği bölümleri atlamak isteyen için.

Bir modüle başka bir yerden bir şeyler bilerek gelen kişi (Python'u biraz
bilen, SQL'i iş yerinde kullanmış) ilk bölümlerden tek tek geçmek zorunda
kalıyordu; kilit her bölümü bir öncekine bağlıyor. Yolun başındaki kartla
isteğe bağlı bir sınava giriyor: **her bölümün kendi sınavından 4 soru**,
sırayla. En az 3'ü doğruysa o bölümü biliyor sayılıyor. (İlk sürümde 2 soru
vardı ve ikisi de doğru isteniyordu; Alican yetersiz buldu. Rastgele
tahminle geçme şansı 2/2'de %6, 3/4'te %5'in altında; tek dikkatsizlik de
bölümü düşürmüyor.)

**Ne açılıyor:** baştan itibaren bilinen bölümler ve hemen arkasındaki
bölüm (sıradaki öğrenilecek yer). Arada **bir** bölüm tutmazsa zincir
kopmuyor (birkaç soru şansa da gidebilir); o bölüm sonuçta "tekrar et" diye
işaretli ama açık. **Üst üste iki bölüm tutmazsa sınav orada bitiyor**:
oradan sonrasını sormak boşa vakit.

**Açılan bölüm tamamlanmış sayılmıyor:** XP, rozet, ilerleme yüzdesi
değişmiyor; yalnızca kilit kalkıyor (`unlock.blocking_section`). Kişi o
bölümlere yine girip sınavını, alıştırmalarını yapabiliyor.

Sonuç `placement:<modül>` ayarında JSON: `reach` (açılan son bilinen
bölümün id'si; id saklanıyor, modüle bölüm eklenince sıra kaysa da doğru
kalsın), `results` (bölüm → doğru sayısı), `date`. Yeniden girilebilir;
yeni sonuç öncekinden azsa da yenisi geçerli (ama başlanmış bölüm zaten
kilitlenmiyor).
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from datetime import date

from .quiz_shuffle import prepare

QUESTIONS_PER_SECTION = 4
# Bölüm bilindi sayılmak için gereken doğru sayısı.
PASS_CORRECT = 3
# Bu kadar bölüm üst üste tutmazsa sınav biter.
STOP_AFTER_FAILS = 2
# Bundan az bölümü (sınavı) olan modülde seviye tespiti gösterilmiyor.
MIN_SECTIONS = 3


def setting_key(chapter_id: str) -> str:
    return f"placement:{chapter_id}"


def _is_review(section) -> bool:
    """Genel tekrar bölümü: konusu yok, bütün modülün özeti; sorulmuyor."""
    return "genel-tekrar" in section.id


def _quiz_path(section, language: str):
    for block in section.blocks:
        if block.type == "quiz":
            resolved = block.file_for(language)
            if resolved and resolved.exists:
                return resolved.path
    return None


def sections_for(chapter, language: str) -> list:
    """Sınavda sorulacak bölümler (sırayla): kendi sınavı olanlar, tekrar hariç."""
    return [s for s in chapter.sections if not _is_review(s) and _quiz_path(s, language) is not None]


def available(chapter, language: str) -> bool:
    return chapter is not None and len(sections_for(chapter, language)) >= MIN_SECTIONS


@dataclass
class Item:
    """Sınavın bir bölümü: bölüm ve ondan seçilen sorular."""

    section: object
    questions: list[dict]
    correct: list[bool] = field(default_factory=list)


def build(chapter, language: str, rng: random.Random | None = None) -> list[Item]:
    """Her bölümden `QUESTIONS_PER_SECTION` soru, şıkları karıştırılmış."""
    rng = rng or random.Random()
    items = []
    for section in sections_for(chapter, language):
        with _quiz_path(section, language).open(encoding="utf-8") as dosya:
            sorular = json.load(dosya).get("questions", [])
        if not sorular:
            continue
        secilen = rng.sample(sorular, min(QUESTIONS_PER_SECTION, len(sorular)))
        items.append(Item(section, prepare(secilen, rng)))
    return items


def passed(item: Item) -> bool:
    gereken = min(PASS_CORRECT, len(item.questions))
    return len(item.correct) == len(item.questions) and sum(item.correct) >= gereken


def should_stop(items: list[Item], done: int) -> bool:
    """`done` bölüm cevaplandıktan sonra sınav bitmeli mi (üst üste iki düşüş)."""
    if done < STOP_AFTER_FAILS:
        return False
    return not any(passed(items[i]) for i in range(done - STOP_AFTER_FAILS, done))


def reach(items: list[Item]) -> int:
    """Bilinen son bölümün sırası (-1: hiçbiri).

    Baştan ilerleniyor; tek bir düşüş zinciri koparmıyor, üst üste iki
    düşüş koparıyor. Zincirin sonundaki düşüşler sayılmıyor.
    """
    son = -1
    ust_uste = 0
    for i, item in enumerate(items):
        if passed(item):
            son, ust_uste = i, 0
        else:
            ust_uste += 1
            if ust_uste >= STOP_AFTER_FAILS:
                break
    return son


def save(store, chapter_id: str, items: list[Item], done: int) -> str:
    """Sonucu kaydeder; açılan son bilinen bölümün id'si ("" hiçbiri)."""
    sira = reach(items[:done])
    hedef = items[sira].section.id if sira >= 0 else ""
    store.set_setting(setting_key(chapter_id), json.dumps({
        "reach": hedef,
        "results": {it.section.id: sum(it.correct) for it in items[:done]},
        "date": date.today().isoformat(),
    }))
    return hedef


def load(store, chapter_id: str) -> dict:
    try:
        veri = json.loads(store.setting(setting_key(chapter_id), "") or "{}")
    except (ValueError, TypeError):
        return {}
    return veri if isinstance(veri, dict) else {}


def reach_index(store, chapter) -> int:
    """Kayıtlı sonuca göre bilinen son bölümün modüldeki sırası (-1 yoksa)."""
    if chapter is None:
        return -1
    hedef = load(store, chapter.id).get("reach", "")
    if not hedef:
        return -1
    for i, section in enumerate(chapter.sections):
        if section.id == hedef:
            return i
    return -1
