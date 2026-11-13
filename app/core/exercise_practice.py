"""Alıştırma tekrarı: bir modülde bitirilen bölümlerin alıştırmalarından
karışık birkaç tane, ipuçları kapalı (Alican 7 Kasım, 1.7.0).

Tekrar sınavının (`practice_exam`) alıştırma hâli. Kişinin kayıtlı çözümüne
ve deneme geçmişine dokunulmuyor: pencere alıştırma ekranına gerçek depo
yerine `PracticeStore` veriyor. Yalnızca çalışma günü ve oturum sonucu
(`exercise_practice:<modül>` ayarı) yazılıyor; kilit, XP, rozet ve
tamamlanma değişmiyor.

İlk sürümde yalnızca tek dosyalı Python kod alıştırmaları ve matematik
problemleri (Alican): Docker, Rust, SQL, Git/Komut Satırı ve iş akışı
alıştırmaları dış ortam istiyor ya da aynı anda iki ekranda çakışabiliyor.
"""

from __future__ import annotations

import json
import random
from datetime import date

from .completion import is_completed

TOTAL = 5
MIN_DONE = 3

# Başlangıç koduyla bilerek geçen alıştırmalar: (modül, bölüm, alıştırma id)
# → neden. Tekrarda seçilmiyorlar (hiçbir şey yazmadan "çözülürdü");
# `tools/check_exercises.py` aynı listeyi buradan alıyor. İçerik şemasına
# alan eklenmedi; istisna burada, gerekçesiyle duruyor.
START_PASSES: dict[tuple[str, str, str], str] = {
    ("03-sql", "00-kurulum", "merhaba-sql"):
        "Kurulum denemesi: yönerge 'hiçbir şey değiştirmeden Çalıştır'a bas' diyor.",
}

# Bu kontrolleri taşıyan Python alıştırmaları dışarıda: FastAPI uygulaması
# (sunucu düğmesi) ve kişinin kendi testleri (çok dosyalı kurgu).
_HEAVY_CHECKS = {"http", "pytest"}


def setting_key(chapter_id: str) -> str:
    return f"exercise_practice:{chapter_id}"


def _is_review(section) -> bool:
    return "genel-tekrar" in section.id


def eligible(section, exercise) -> bool:
    """Bu alıştırma tekrarda sorulabilir mi."""
    if _is_review(section):
        return False
    if (section.chapter_id, section.id, exercise.id) in START_PASSES:
        return False
    if exercise.is_problem:
        return True
    if exercise.is_terminal or exercise.is_multi_file or exercise.group == "pset":
        return False
    if exercise.language != "python":
        return False
    return not any(check.get("type") in _HEAVY_CHECKS for check in exercise.checks)


def _eligible_of(section) -> list:
    return [e for e in section.exercises if eligible(section, e)]


def done_sections(chapter, store) -> list:
    """Bitirilmiş ve uygun alıştırması olan bölümler, modüldeki sırayla."""
    if chapter is None:
        return []
    active = store.active_sections()
    sonuc = []
    for section in chapter.sections:
        if _is_review(section) or not section.exercise_ids:
            continue
        if is_completed(store, section, active) and _eligible_of(section):
            sonuc.append(section)
    return sonuc


def available(chapter, store) -> bool:
    return len(done_sections(chapter, store)) >= MIN_DONE


def build(sections: list, rng: random.Random | None = None, total: int = TOTAL) -> list[tuple]:
    """`(bölüm, alıştırma)` çiftleri, karışık sırada.

    Bölüm sayısı `total`'dan çoksa rastgele `total` bölümden birer; azsa her
    bölümden en az bir, kalanlar bölümlere sırayla dağıtılıyor (bölümün
    uygun alıştırması bitince atlanıyor). Aynı alıştırma iki kez gelmiyor.
    """
    rng = rng or random.Random()
    havuz = {s.id: _eligible_of(s) for s in sections}
    sirali = [s for s in sections if havuz[s.id]]
    if len(sirali) > total:
        sirali = rng.sample(sirali, total)
    for liste in havuz.values():
        rng.shuffle(liste)
    secim: list[tuple] = []
    while len(secim) < total and any(havuz[s.id] for s in sirali):
        for section in sirali:
            if len(secim) >= total:
                break
            if havuz[section.id]:
                secim.append((section, havuz[section.id].pop()))
    rng.shuffle(secim)
    return secim


def save(store, chapter_id: str, solved: int, helped: int, total: int,
         today: date | None = None) -> None:
    store.set_setting(setting_key(chapter_id), json.dumps({
        "solved": solved, "helped": helped, "total": total,
        "date": (today or date.today()).isoformat(),
    }))


def load(store, chapter_id: str) -> dict:
    try:
        veri = json.loads(store.setting(setting_key(chapter_id), "") or "{}")
    except (ValueError, TypeError):
        return {}
    return veri if isinstance(veri, dict) else {}


class PracticeStore:
    """Alıştırma ekranına gerçek depo yerine verilen sarmalayıcı.

    Alıştırma ekranının depoya eriştiği yöntemlerin hepsi burada, açıkça:
    kayıtlı kod, denemeler ve çözüldü bilgisi görünmüyor; çalıştırmalar
    yalnızca bu oturumda sayılıyor. Çalışma günü ve ayarlar gerçek depoya
    gidiyor. Burada olmayan her yöntem `AttributeError` veriyor: ekran
    ileride yeni bir kayıt yolu edinirse tekrar sessizce gerçek kayda
    yazmasın, hata versin.
    """

    def __init__(self, store) -> None:
        self._store = store
        self._attempts: dict[tuple[str, str, str], int] = {}
        self._solved: set[tuple[str, str, str]] = set()

    # --- okuma --------------------------------------------------------------
    def exercise_code(self, chapter_id: str, section_id: str, exercise_id: str) -> str:
        return ""

    def exercise_attempts(self, chapter_id: str, section_id: str, exercise_id: str) -> list:
        return []

    def exercise_solved(self, chapter_id: str, section_id: str, exercise_id: str) -> bool:
        return (chapter_id, section_id, exercise_id) in self._solved

    def attempts(self, chapter_id: str, section_id: str, exercise_id: str) -> int:
        return self._attempts.get((chapter_id, section_id, exercise_id), 0)

    def setting(self, key: str, default: str = "") -> str:
        return self._store.setting(key, default)

    # --- yazma --------------------------------------------------------------
    def save_exercise(self, chapter_id: str, section_id: str, exercise_id: str, code: str,
                      solved: bool | None = None, count_attempt: bool = False) -> None:
        anahtar = (chapter_id, section_id, exercise_id)
        if count_attempt:
            self._attempts[anahtar] = self._attempts.get(anahtar, 0) + 1
        if solved:
            self._solved.add(anahtar)

    def add_exercise_attempt(self, *args, **kwargs) -> bool:
        return False

    def mark_study_day(self) -> bool:
        return self._store.mark_study_day()
