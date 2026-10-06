"""Geçmiş denemeler: alıştırmada "Denemelerim" sekmesi, sınavda yanlışlar.

Alican istedi (30 Eylül): kişi geçmişte yaptığı yanlışları görebilmeli.
Alıştırmada yanlış yazdığı kodlar ve en son yazdığı doğru kod; sınavda
hangi soruya ne cevap verdiği, doğrusunun ne olduğu ve açıklaması.

Buradaki fonksiyonlar yalnızca metin üretiyor (markdown + küçük HTML);
belge `LessonView` ile çiziliyor. Kayıtlar `ProgressStore`'da
(`exercise_attempts`, `quiz_attempts`).

**Geri bildirim iki dilde saklanıyor.** Denemenin "neden düştü" satırları
çalıştırma anında üretiliyor; tek dilde saklansaydı dil değiştirince eski
dilde kalırdı. Kayıt anında iki dilin metni birden yazılıyor (`detail`).
"""

from __future__ import annotations

import difflib
import hashlib
import html
import json
from datetime import datetime

from ..core import workspace_files
from ..core.grader import describe
from ..core.language import AVAILABLE_LANGUAGES, LanguageManager

_MANAGERS: dict[str, LanguageManager] = {}


def _manager(language: str) -> LanguageManager:
    if language not in _MANAGERS:
        _MANAGERS[language] = LanguageManager(language)
    return _MANAGERS[language]


def run_detail(result) -> str:
    """Bir çalıştırmanın düşen kontrolleri, iki dilde (JSON)."""
    detay = {}
    for dil in AVAILABLE_LANGUAGES:
        detay[dil] = [f.message for f in describe(result, _manager(dil)) if not f.passed][:4]
    return json.dumps(detay, ensure_ascii=False)


def question_key(question: dict) -> str:
    """Sorunun kısa parmak izi: soru sonradan değişirse eski cevap ona
    uygulanmasın."""
    metin = json.dumps(question.get("text", {}), ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(metin.encode("utf-8")).hexdigest()[:10]


def when(language: LanguageManager, stamp: str) -> str:
    """"30 Eylül 14:05" / "30 September 14:05"."""
    try:
        an = datetime.fromisoformat(stamp)
    except ValueError:
        return stamp
    return f"{an.day} {language.t(f'month_long.{an.month}')} {an:%H:%M}"


def _reasons(language: LanguageManager, detail: str) -> list[str]:
    try:
        veri = json.loads(detail) if detail else {}
    except ValueError:
        return []
    if not isinstance(veri, dict):
        return []
    satirlar = veri.get(language.language) or veri.get("tr") or []
    return [str(s) for s in satirlar]


def _marked_code(code: str, reference: str | None) -> str:
    """Kod, `.cmp` kutusunda; `reference` verilirse onda olmayan satırlar
    işaretli (yanlışın büyük olasılıkla olduğu yer)."""
    satirlar = code.splitlines() or [""]
    isaretli: set[int] = set()
    if reference is not None:
        a = [s.strip() for s in satirlar]
        b = [s.strip() for s in reference.splitlines()]
        eslesme = difflib.SequenceMatcher(None, a, b, autojunk=False)
        for islem, i1, i2, _, _ in eslesme.get_opcodes():
            if islem in ("replace", "delete"):
                isaretli.update(i for i in range(i1, i2) if a[i])
    parcalar = []
    for i, satir in enumerate(satirlar):
        sinif = "ln diff" if i in isaretli else "ln"
        parcalar.append(f'<span class="{sinif}">{html.escape(satir) or " "}</span>')
    return '<div class="cmp code">' + "".join(parcalar) + "</div>"


# Kod bloğu etiketi (editör dili → markdown).
FENCE_TAGS = {"tsql": "sql", "shell": "bash"}


def _fence(code: str, language: str) -> str:
    return f"```{FENCE_TAGS.get(language, language)}\n{code.rstrip()}\n```"


def _file_title(name: str) -> str:
    return f'<div class="out-label">{html.escape(name)}</div>'


def _right_code(code: str, code_language: str) -> list[str]:
    """Son doğru çözüm; çok dosyalı kayıtta dosya dosya."""
    files = workspace_files.decode(code)
    if files is None:
        return [_fence(code, code_language)]
    parcalar = []
    for name, text in files.items():
        parcalar.append(_file_title(name))
        parcalar.append(_fence(text, workspace_files.file_language(name)))
    return parcalar


def _wrong_code(code: str, reference: str | None) -> list[str]:
    """Yanlış deneme; çok dosyalı kayıtta yalnızca son doğrudan farklı dosyalar."""
    files = workspace_files.decode(code)
    if files is None:
        return [_marked_code(code.rstrip("\n"), reference)]
    ref_files = workspace_files.decode(reference) if reference is not None else None
    parcalar = []
    for name, text in files.items():
        ref = None if ref_files is None else ref_files.get(name, "")
        if ref is not None and ref.strip() == text.strip():
            continue
        parcalar.append(_file_title(name))
        parcalar.append(_marked_code(text.rstrip("\n"), ref))
    return parcalar


def _problem_answers(code: str) -> str:
    try:
        cevaplar = json.loads(code)
    except ValueError:
        return code
    if isinstance(cevaplar, dict):
        cevaplar = cevaplar.get("answers", [])
    return " · ".join(f"`{str(c).strip() or '—'}`" for c in cevaplar)


def exercise_markdown(language: LanguageManager, attempts: list[dict], code_language: str,
                      problem: bool = False) -> str:
    """"Denemelerim" sekmesinin metni. `attempts` en yenisi başta."""
    t = language.t
    toplam = len(attempts)
    dogru = [a for a in attempts if a["passed"]]
    yanlis = [a for a in attempts if not a["passed"]]
    parcalar = [f"# {t('history.title')}"]
    if not attempts:
        parcalar.append(t("history.empty"))
        return "\n\n".join(parcalar)
    parcalar.append(t("history.summary", total=toplam, wrong=len(yanlis), right=len(dogru)))

    sira = {a["id"]: toplam - i for i, a in enumerate(attempts)}
    son_dogru = dogru[0] if dogru else None
    if son_dogru is not None:
        parcalar.append(f"## {t('history.last_right')}")
        parcalar.append(f'<div class="out-label">{html.escape(t("history.attempt", n=sira[son_dogru["id"]], when=when(language, son_dogru["created_at"])))} ✓</div>')
        if problem:
            parcalar.append(t("history.answers", answers=_problem_answers(son_dogru["code"])))
        else:
            parcalar.extend(_right_code(son_dogru["code"], code_language))

    if yanlis:
        parcalar.append(f"## {t('history.wrong_title')}")
        if problem:
            parcalar.append(t("history.wrong_intro_problem"))
        elif son_dogru is not None:
            parcalar.append(t("history.wrong_intro_marked"))
        else:
            parcalar.append(t("history.wrong_intro_unmarked"))
        referans = None if problem or son_dogru is None else son_dogru["code"]
        for deneme in yanlis:
            parcalar.append(f"### {t('history.attempt', n=sira[deneme['id']], when=when(language, deneme['created_at']))} ✕")
            nedenler = _reasons(language, deneme.get("detail", ""))
            if nedenler:
                parcalar.append("\n".join(f"- {n}" for n in nedenler))
            if problem:
                parcalar.append(t("history.answers", answers=_problem_answers(deneme["code"])))
            else:
                parcalar.extend(_wrong_code(deneme["code"], referans))
    elif son_dogru is not None:
        parcalar.append(t("history.no_wrong"))
    return "\n\n".join(parcalar)


def quiz_answers(cards) -> str:
    """Bitmiş sınavın cevapları (JSON): sorunun dosyadaki sırası, özgün şık,
    doğru mu, sorunun parmak izi. Kartlar sınavdaki sırada."""
    cevaplar = []
    for kart in cards:
        soru = kart.question
        secilen = kart.selected if kart.is_answered else None
        sira = soru.get("_order")
        ozgun = sira[secilen] if (secilen is not None and sira) else secilen
        cevaplar.append({
            "q": soru.get("_index", -1),
            "chosen": ozgun,
            "ok": bool(kart.is_answered and kart.is_correct),
            "key": question_key(soru),
        })
    return json.dumps(cevaplar, ensure_ascii=False)


def quiz_markdown(language: LanguageManager, questions: list[dict], attempt: dict,
                  only_wrong: bool) -> str:
    """Bir sınav denemesinin soru soru dökümü."""
    t = language.t
    try:
        cevaplar = json.loads(attempt.get("answers") or "[]")
    except ValueError:
        cevaplar = []
    dogru = sum(1 for c in cevaplar if c.get("ok"))
    if attempt.get("abandoned"):
        parcalar = [t("quiz_history.summary_abandoned", correct=dogru, total=len(cevaplar),
                      when=when(language, attempt["created_at"]))]
    else:
        parcalar = [t("quiz_history.summary", correct=dogru, total=len(cevaplar),
                      score=attempt["score"], when=when(language, attempt["created_at"]))]
    gosterilen = 0
    for sira, cevap in enumerate(cevaplar, start=1):
        if only_wrong and cevap.get("ok"):
            continue
        indeks = cevap.get("q", -1)
        if not (0 <= indeks < len(questions)):
            continue
        soru = questions[indeks]
        gosterilen += 1
        isaret = "✓" if cevap.get("ok") else "✕"
        parcalar.append(f"### {t('quiz_history.question', n=sira)} {isaret}")
        if cevap.get("key") and cevap["key"] != question_key(soru):
            parcalar.append(f"*{t('quiz_history.changed')}*")
        parcalar.append(language.pick(soru.get("text"), ""))
        secenekler = language.pick(soru.get("options"), []) or []
        dogru_sik = int(soru.get("answer", -1))
        secilen = cevap.get("chosen")
        satirlar = []
        if secilen is None:
            satirlar.append(f"- {t('quiz_history.blank')}")
        elif not cevap.get("ok") and 0 <= secilen < len(secenekler):
            satirlar.append(f"- ✕ **{t('quiz_history.yours')}** {secenekler[secilen]}")
        if 0 <= dogru_sik < len(secenekler):
            satirlar.append(f"- ✓ **{t('quiz_history.right')}** {secenekler[dogru_sik]}")
        parcalar.append("\n".join(satirlar))
        aciklama = language.pick(soru.get("explanation"), "")
        if aciklama:
            parcalar.append("\n".join(f"> {satir}" for satir in aciklama.splitlines()))
    if not gosterilen:
        parcalar.append(t("quiz_history.all_right"))
    return "\n\n".join(parcalar)
