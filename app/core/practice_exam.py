"""Tekrar sınavı: bir modülde bitirilen bölümlerden karışık sorular.

Alican 27 Ekim (1.4.0). Modülde en az `MIN_DONE` bölüm bitince yolun
başında çıkıyor; bitirilen bölümlerin sınavlarından toplam `TOTAL` soru,
bölümlere olabildiğince eşit dağıtılarak (20'den çok bölüm bittiyse 20
farklı bölümden birer soru). Süresiz; cevaptan sonra doğrusu gösteriliyor.
Yanlışlar tekrar kutusuna giriyor (`review_box`); kilit, XP ve rozet
değişmiyor. Son sonuç `practice:<modül>` ayarında.
"""

from __future__ import annotations

import json
import random
from datetime import date

from . import review_box
from .completion import is_completed
from .placement import sections_for

TOTAL = 20
MIN_DONE = 3


def setting_key(chapter_id: str) -> str:
    return f"practice:{chapter_id}"


def done_sections(chapter, store, language: str) -> list:
    """Sınavı olan (genel tekrar hariç) ve bitirilmiş bölümler, sırayla."""
    if chapter is None:
        return []
    active = store.active_sections()
    return [s for s in sections_for(chapter, language) if is_completed(store, s, active)]


def available(chapter, store, language: str) -> bool:
    return len(done_sections(chapter, store, language)) >= MIN_DONE


def _shares(count: int, rng: random.Random) -> list[int]:
    """`TOTAL` soruyu `count` bölüme dağıtır (artan sorular rastgele bölümlere)."""
    if count >= TOTAL:
        secilen = set(rng.sample(range(count), TOTAL))
        return [int(i in secilen) for i in range(count)]
    taban, artan = divmod(TOTAL, count)
    fazla = set(rng.sample(range(count), artan))
    return [taban + (i in fazla) for i in range(count)]


def build(sections: list, language: str, rng: random.Random | None = None) -> list[dict]:
    """Sorular, karışık sırada: `{"section", "index", "question"}`.

    `index` sorunun dosyadaki sırası (yanlışlar tekrar kutusuna onunla girer).
    """
    rng = rng or random.Random()
    sorular = []
    for section, pay in zip(sections, _shares(len(sections), rng)):
        if not pay:
            continue
        hepsi = review_box.load_questions(section, language)
        for index in rng.sample(range(len(hepsi)), min(pay, len(hepsi))):
            sorular.append({"section": section, "index": index, "question": hepsi[index]})
    rng.shuffle(sorular)
    return sorular


def save(store, chapter_id: str, correct: int, total: int, today: date | None = None) -> None:
    store.set_setting(setting_key(chapter_id), json.dumps({
        "correct": correct, "total": total, "date": (today or date.today()).isoformat(),
    }))


def load(store, chapter_id: str) -> dict:
    try:
        veri = json.loads(store.setting(setting_key(chapter_id), "") or "{}")
    except (ValueError, TypeError):
        return {}
    return veri if isinstance(veri, dict) else {}
