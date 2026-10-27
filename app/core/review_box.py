"""Tekrar kutusu: sınavda yanlış yapılan soruları aralıklı yeniden sormak.

Alican 27 Ekim (1.4.0). Sınavda yanlış ya da boş bırakılan soru kutuya
giriyor ve ertesi gün soruluyor; doğru bilinince bir sonraki aralığa (3, 7,
14 gün) geçiyor, 14 günlükte de doğruysa kutudan çıkıyor. Yanlışsa ertesi
güne, ilk aralığa dönüyor. Unutmayı en çok azaltan bilinen yöntem bu
(aralıklı tekrar, spaced repetition).

Günde en fazla `DAILY_LIMIT` soru gösteriliyor; fazlası sonraki günlere
kalıyor. Bu sürümden önceki sınavların yanlışları ilk açılışta bir kez
ekleniyor: her bölümün son bitmiş denemesi (Alican seçti).

Soru dosyadaki sırasıyla ve metninin parmak iziyle tutuluyor (sınav
kayıtları gibi). Soru sonradan değişirse parmak izi tutmuyor; o kayıt
gösterilmiyor ve kutudan çıkarılıyor. Tekrar XP vermiyor (XP hesaplanıyor),
ama çalışma günü sayılıyor.
"""

from __future__ import annotations

import hashlib
import json
from datetime import date, timedelta

# Doğru bilinince sıradaki aralık (gün). Kutuya giren soru ilk kez ertesi gün.
INTERVALS = (1, 3, 7, 14)
DAILY_LIMIT = 20
BACKFILL_KEY = "review_backfilled"


def question_key(question: dict) -> str:
    """Sorunun kısa parmak izi: soru sonradan değişirse eski cevap ona
    uygulanmasın."""
    metin = json.dumps(question.get("text", {}), ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(metin.encode("utf-8")).hexdigest()[:10]


def wrong_questions(answers: str, abandoned: bool = False) -> list[tuple[int, str]]:
    """Sınav kaydından kutuya girecek sorular: (sıra, parmak izi).

    Bitmiş sınavda yanlış ve boşlar; yarıda bırakılanda yalnızca cevaplanıp
    yanlış olanlar (boşlar sorulmadan kalanlar olabilir).
    """
    try:
        cevaplar = json.loads(answers)
    except (TypeError, ValueError):
        return []
    sonuc = []
    for cevap in cevaplar if isinstance(cevaplar, list) else []:
        if not isinstance(cevap, dict) or cevap.get("ok") or not cevap.get("key"):
            continue
        if abandoned and cevap.get("chosen") is None:
            continue
        index = cevap.get("q", -1)
        if isinstance(index, int) and index >= 0:
            sonuc.append((index, str(cevap["key"])))
    return sonuc


def backfill(store, today: date | None = None) -> None:
    """Bu sürümden önceki sınavların yanlışlarını bir kez, bugüne ekler."""
    if store.setting(BACKFILL_KEY, ""):
        return
    today = today or date.today()
    for chapter_id, section_id, answers in store.last_finished_quiz_answers():
        store.add_review_items(chapter_id, section_id, wrong_questions(answers), today)
    store.set_setting(BACKFILL_KEY, today.isoformat())


def today_items(store, today: date | None = None) -> list[dict]:
    """Bugün sorulacaklar (en fazla `DAILY_LIMIT`)."""
    return store.due_reviews(today or date.today(), DAILY_LIMIT)


def today_count(store, today: date | None = None) -> int:
    return min(store.due_review_count(today or date.today()), DAILY_LIMIT)


def answer(store, item: dict, correct: bool, today: date | None = None) -> None:
    """Cevaba göre sorunun aşamasını ilerletir, başa alır ya da çıkarır."""
    today = today or date.today()
    if correct:
        stage = item["stage"] + 1
        if stage >= len(INTERVALS):
            store.set_review(item["chapter_id"], item["section_id"], item["question_key"], None)
            return
    else:
        stage = 0
    store.set_review(item["chapter_id"], item["section_id"], item["question_key"], stage,
                     today + timedelta(days=INTERVALS[stage]))


def load_questions(section, language: str) -> list[dict]:
    """Bölümün sınav soruları (dosyadaki sırayla); sınavı yoksa boş."""
    for block in section.blocks if section is not None else ():
        if block.type != "quiz":
            continue
        resolved = block.file_for(language)
        if resolved and resolved.exists:
            try:
                with resolved.path.open(encoding="utf-8") as dosya:
                    return json.load(dosya).get("questions", [])
            except (OSError, ValueError):
                return []
    return []


def find_question(questions: list[dict], item: dict) -> dict | None:
    """Kayıttaki soruyu dosyada bulur: önce sırasıyla, sonra parmak iziyle."""
    index = item["question_index"]
    if 0 <= index < len(questions) and question_key(questions[index]) == item["question_key"]:
        return questions[index]
    for soru in questions:
        if question_key(soru) == item["question_key"]:
            return soru
    return None
