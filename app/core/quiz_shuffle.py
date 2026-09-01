"""Sınav sorularını ve şıklarını karıştırır.

Her denemede sıra değişiyor. Sebebi ezber: aynı sırayla üç kez giren biri
soruyu okumadan "ikinci şık" diye işaretlemeye başlıyor ve sınav ölçmeyi
bırakıyor.

Şıklar da karışıyor. Şık karışınca doğru cevabın sırası da değişiyor;
`answer` alanı yeni sıraya göre yeniden hesaplanıyor.

**Üst üste ikiden fazla aynı sırada doğru cevap olmuyor.** Rastgelelik kendi
başına bırakılınca bu düzenli olarak oluyor ve insan farkında olmadan
"bir süredir hep B geldi, bu da B'dir" diye düşünüyor. Karıştırma bittikten
sonra bu duruma bakılıp yalnızca sorunlu sorunun şıkları yeniden diziliyor.
"""

from __future__ import annotations

import random

# Aynı sırada arka arkaya en fazla kaç doğru cevap olabilir.
MAX_STREAK = 2

# Şık dizilimini düzeltmeye kaç kez çalışılacağı. Şık sayısı kadar farklı
# yer var; birkaç deneme her zaman yetiyor, ama sonsuz döngü olmasın.
MAX_ATTEMPTS = 20


def _shuffle_options(question: dict, rng: random.Random) -> dict:
    """Bir sorunun şıklarını karıştırıp `answer` alanını düzeltir.

    Şıklar her dil için ayrı listede duruyor ama **aynı sırayı** paylaşıyor:
    Türkçe üçüncü şık ile İngilizce üçüncü şık aynı cevap. Bu yüzden tek bir
    sıralama üretilip iki listeye de uygulanıyor.
    """
    options = question.get("options", {})
    diller = [dil for dil, liste in options.items() if isinstance(liste, list)]
    if not diller:
        return question

    uzunluk = len(options[diller[0]])
    if uzunluk < 2:
        return question

    sira = list(range(uzunluk))
    rng.shuffle(sira)

    yeni = dict(question)
    yeni["options"] = {
        dil: [options[dil][i] for i in sira] for dil in diller
    }
    yeni["answer"] = sira.index(question.get("answer", 0))
    return yeni


def _fix_streaks(questions: list[dict], rng: random.Random) -> list[dict]:
    """Aynı sırada üst üste gelen doğru cevapları dağıtır."""
    for index in range(MAX_STREAK, len(questions)):
        pencere = questions[index - MAX_STREAK:index + 1]
        if len({q["answer"] for q in pencere}) > 1:
            continue

        # Bu soru zinciri uzatıyor; şıklarını yeniden diz.
        for _ in range(MAX_ATTEMPTS):
            aday = _shuffle_options(questions[index], rng)
            if aday["answer"] != questions[index]["answer"]:
                questions[index] = aday
                break

    return questions


def prepare(questions: list[dict], rng: random.Random | None = None) -> list[dict]:
    """Soruları ve şıkları karıştırılmış yeni bir liste döndürür.

    Özgün liste değiştirilmiyor: aynı sınav dosyası her denemede baştan
    karıştırılıyor.
    """
    rng = rng or random.Random()

    karisik = list(questions)
    rng.shuffle(karisik)
    karisik = [_shuffle_options(q, rng) for q in karisik]
    return _fix_streaks(karisik, rng)
