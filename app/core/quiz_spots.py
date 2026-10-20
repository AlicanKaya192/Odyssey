"""Sınavdan sonra zayıf konu: yanlış sorunun dayandığı ders başlığı ya da not.

Soruların konu etiketi yok (11 000'i aşkın soruya elle etiket yazılmıyor).
Başlık "Takıldın mı?" kartının yoluyla **bulunuyor** (`stuck.chunk_scores`):
sorunun metni, doğru şık ve açıklamadaki kelimeler dersin `## `
parçalarında aranıyor; ters tırnaklı kod adları daha belirleyici.

Alıştırmadan farklı olarak burada **eşik var**: en iyi başlık ikinciden
en az `MIN_MARGIN` kat güçlü değilse soruya bağlantı konmuyor (yanlış
başlığa götürmektense hiç götürmemek). 20 Ekim ölçümü (genel tekrar
dışındaki 10 786 soru): başlık bulunan %98,8, eşiği geçen %85,7 (TR),
%83,8 (EN).

**Ders notları da aranıyor** (Alican 20 Ekim): konu ders metninde değil
notta anlatılıyorsa (Döngüler'de `break`) en yakın ders başlığına gitmesin.
Not, dersin en iyisinden `NOTE_MARGIN` kat güçlüyse kazanıyor. Ölçüm:
bağlantılı soru TR %86,0 → %90,1, EN %84,0 → %88,1; dersten nota geçen
%9,8 (örneklemde 20/20 kabul edilebilir), yeni bağlanan %4,6 (20'de 17–18).

Genel tekrar bölümlerinde kullanılmıyor: soruların cevabı başka
bölümlerin dersinde.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

from .search import lesson_chunks
from .stuck import chunk_scores, code_words, lesson_spots, prose_words, unit_scores

MIN_MARGIN = 1.2
# Ders notu ancak dersin en iyi başlığından bu kat güçlüyse seçiliyor.
NOTE_MARGIN = 1.5
# Sonuç kartında en fazla bu kadar başlık.
WEAK_LIMIT = 3

_FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.S)
_CODE = re.compile(r"`([^`]+)`")
# Soru kalıplarında geçen, yer göstermeyen kelimeler.
_QUESTION_STOP = {
    "hangi", "hangisi", "hangisidir", "nedir", "neden", "nasıl", "olur", "olarak", "için",
    "gibi", "kadar", "doğru", "yanlış", "aşağıdakilerden", "değildir", "kaçtır",
    "which", "what", "does", "when", "following", "about", "there", "their", "these",
    "those", "would", "could", "true", "false",
}


def question_words(question: dict, language: str) -> dict[str, float]:
    """Sorunun aranacak kelimeleri ve ağırlıkları."""

    def metin(alan) -> str:
        if isinstance(alan, dict):
            return str(alan.get(language) or alan.get("tr") or "")
        return str(alan or "")

    secenekler = question.get("options") or []
    if isinstance(secenekler, dict):
        secenekler = secenekler.get(language) or secenekler.get("tr") or []
    dogru = int(question.get("answer", -1))
    dogru_sik = secenekler[dogru] if 0 <= dogru < len(secenekler) else ""

    aranan: dict[str, float] = {}
    for kaynak, agirlik in ((metin(question.get("text")), 1.5), (dogru_sik, 1.0),
                            (metin(question.get("explanation")), 1.0)):
        # Önce kod blokları: içlerindeki ters tırnaklar satır içi kodu kaydırıyordu.
        bloklar = _FENCE.findall(kaynak)
        kaynak = _FENCE.sub(" ", kaynak)
        kelimeler = {w: agirlik for w in prose_words(_CODE.sub(" ", kaynak))}
        for parca in bloklar + _CODE.findall(kaynak):
            kelimeler.update({w: 2 * agirlik for w in code_words(parca)})  # kod adları daha belirleyici
        for kelime, deger in kelimeler.items():
            if kelime not in _QUESTION_STOP:
                aranan[kelime] = max(aranan.get(kelime, 0.0), deger)
    return aranan


@dataclass(frozen=True)
class QuizSpot:
    """Sorunun gösterdiği yer: dersin başlığı ya da bir ders notu (ve başlığı)."""

    title: str
    anchor: str  # notta "" = notun başı
    note: int = -1  # -1 = ders; yoksa bölümün kaçıncı notu

    @property
    def in_notes(self) -> bool:
        return self.note >= 0


class QuizSpots:
    """Bir bölümün dersi ve ders notları; soru soru, gerekince ve bir kez.

    `notes`: bölümün notları sırasıyla, (adı, ekranda çizilen metni
    `# ad` + gövde). Not, dersin en iyi başlığından en az `NOTE_MARGIN` kat
    güçlüyse seçiliyor; yoksa sonuç yalnızca derse bakılmış gibi (notsuz
    hesapla birebir aynı).
    """

    def __init__(self, lesson_source: str, language: str,
                 notes: list[tuple[str, str]] | tuple = ()) -> None:
        self._source = lesson_source if lesson_source.strip() else ""
        self._language = language
        self._spots = [QuizSpot(y.title, y.anchor) for y in lesson_spots(self._source)] if self._source else []
        # Ders parçaları (giriş hariç) + notların bütün parçaları (girişi dahil).
        self._units: list[tuple[str, str]] = list(lesson_chunks(self._source)) if self._source else []
        self._skip = {0} if len(self._units) > 1 else set()
        self._lesson_count = len(self._units)
        self._note_spots: list[QuizSpot] = []
        for sira, (ad, metin) in enumerate(notes):
            yerler = lesson_spots(metin)
            for (baslik, govde), yer in zip(lesson_chunks(metin), yerler):
                self._units.append((baslik or ad, govde))
                self._note_spots.append(QuizSpot(f"{ad} › {baslik}" if baslik else ad, yer.anchor, sira))
        self._cache: dict[int, QuizSpot | None] = {}

    def spot(self, index: int, question: dict) -> QuizSpot | None:
        """Sorunun yeri; ders yoksa ya da eşleşme belirgin değilse None."""
        if index not in self._cache:
            self._cache[index] = self._find(question)
        return self._cache[index]

    def _find(self, question: dict) -> QuizSpot | None:
        aranan = question_words(question, self._language)
        if self._note_spots:
            puanlar = unit_scores(self._units, aranan, self._skip)
            ders = max(puanlar[:self._lesson_count], default=0.0)
            if max(puanlar[self._lesson_count:]) > NOTE_MARGIN * ders:
                secilen = _pick(puanlar)
                if secilen is None:
                    return self._same_note(puanlar)
                if secilen < self._lesson_count:
                    return None
                return self._note_spots[secilen - self._lesson_count]
        if not self._source:
            return None
        secilen = _pick(chunk_scores(self._source, aranan))
        if secilen is None:
            return None
        yer = self._spots[secilen]
        return yer if yer.anchor else None

    def _same_note(self, puanlar: list[float]) -> QuizSpot | None:
        """En güçlü iki parça aynı notun iki başlığıysa (Döngüler'de `break`
        ile `continue`) başlık belirsiz ama not belli: notun başı."""
        sira = sorted(range(len(puanlar)), key=puanlar.__getitem__, reverse=True)[:2]
        if len(sira) < 2 or min(sira) < self._lesson_count:
            return None
        ilk, ikinci = (self._note_spots[i - self._lesson_count] for i in sira)
        if ilk.note != ikinci.note:
            return None
        return next(y for y in self._note_spots if y.note == ilk.note)

    def weak(self, questions: list[tuple[int, dict]]) -> list[tuple[QuizSpot, int]]:
        """Yanlış soruların en çok gösterdiği yerler: (yer, soru sayısı).

        Çoktan aza; eşitlikte önce ders, sonra notlar, kendi sıralarıyla.
        En fazla `WEAK_LIMIT`.
        """
        sayac: Counter[QuizSpot] = Counter()
        for indeks, soru in questions:
            yer = self.spot(indeks, soru)
            if yer is not None:
                sayac[yer] += 1
        sira = {yer: i for i, yer in enumerate(self._spots + self._note_spots)}
        return sorted(sayac.items(), key=lambda kv: (-kv[1], sira.get(kv[0], 0)))[:WEAK_LIMIT]


def _pick(puanlar: list[float]) -> int | None:
    """En iyi parça; hiç eşleşme yoksa ya da ikinciden belirgin güçlü değilse None."""
    sirali = sorted(puanlar, reverse=True)
    if not sirali or sirali[0] <= 0:
        return None
    ikinci = sirali[1] if len(sirali) > 1 else 0.0
    if ikinci and sirali[0] < MIN_MARGIN * ikinci:
        return None
    return puanlar.index(sirali[0])
