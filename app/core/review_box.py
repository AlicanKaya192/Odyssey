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
import re
from datetime import date, timedelta

# Doğru bilinince sıradaki aralık (gün). Kutuya giren soru ilk kez ertesi gün.
INTERVALS = (1, 3, 7, 14)
DAILY_LIMIT = 20
BACKFILL_KEY = "review_backfilled"
# Sözlük terimlerinin kayıtlarında modül yerine bu (bkz. `add_term`).
GLOSSARY = "glossary"


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


# --- sözlük terimleri ------------------------------------------------------
#
# Alican 28 Ekim: sözlükte işaretlenen terim de kutuya giriyor ve aynı
# aralıklarla soruluyor. Kayıt sınav sorularıyla aynı tabloda, "modül"
# yerine `GLOSSARY`, bölüm ve parmak izi yerine terimin kimliği. Soru dört
# şıklı: terimin tanımı ve aynı gruptan (yetmezse başka gruptan) üç tanım.


def add_term(store, term_id: str, today: date | None = None) -> None:
    """Terimi kutuya koyar; ilk kez ertesi gün soruluyor."""
    yarin = (today or date.today()) + timedelta(days=INTERVALS[0])
    store.add_review_items(GLOSSARY, term_id, [(0, term_id)], yarin)


def remove_term(store, term_id: str) -> None:
    store.set_review(GLOSSARY, term_id, term_id, None)


def term_ids(store) -> set[str]:
    """Kutudaki terimler."""
    return store.review_sections(GLOSSARY)


# Dersteki terim kartı (`LessonView`) her yerde kuruluyor (ders, not, yönerge);
# kaydı ana pencere bir kez veriyor. Verilmemişse (testler) kartta bağlantı yok.
live_store = None
live_changed = None


def connect_live(store, changed=None) -> None:
    """Terim kartındaki bağlantının kullanacağı kayıt ve kutu değişince
    çağrılacak işlev (karşılama kartındaki sayı)."""
    global live_store, live_changed
    live_store, live_changed = store, changed


def toggle_term(store, term_id: str, today: date | None = None) -> bool:
    """Terim kutudaysa çıkarır, değilse koyar; yeni durum (kutuda mı).
    Sözlük sayfası ve dersteki terim kartı bunu kullanıyor."""
    if term_id in term_ids(store):
        remove_term(store, term_id)
        return False
    add_term(store, term_id, today)
    return True


def term_question(term: dict, terms: tuple[dict, ...] | list[dict], language: str,
                  prompt: str, rng) -> dict | None:
    """Terimin dört şıklı sorusu (`QuestionCard` biçiminde, tek dil).

    Tanımda terimin adı geçiyorsa `___` ile örtülüyor: cevabı ele vermesin.
    Tanımı olmayan terim için `None`.
    """
    def tanim(t: dict) -> str:
        metin = (t.get("text") or {}).get(language) or (t.get("text") or {}).get("tr") or ""
        ad = (t.get("title") or {}).get(language) or ""
        # Kelime başında (Türkçe ek serbest: "listeler" → "___ler").
        return re.sub(r"(?<!\w)" + re.escape(ad), "___", metin, flags=re.IGNORECASE) if ad else metin

    dogru = tanim(term)
    if not dogru:
        return None
    ayni = [t for t in terms if t["id"] != term["id"] and t.get("group") == term.get("group")]
    baska = [t for t in terms if t["id"] != term["id"] and t.get("group") != term.get("group")]
    rng.shuffle(ayni)
    rng.shuffle(baska)
    celdiriciler: list[str] = []
    for aday in ayni + baska:
        metin = tanim(aday)
        if metin and metin != dogru and metin not in celdiriciler:
            celdiriciler.append(metin)
        if len(celdiriciler) == 3:
            break
    if not celdiriciler:
        return None
    baslik = (term.get("title") or {}).get(language) or (term.get("title") or {}).get("tr") or term["id"]
    return {
        "text": {language: prompt.format(term=baslik)},
        "options": {language: [dogru, *celdiriciler]},
        "answer": 0,
    }


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
