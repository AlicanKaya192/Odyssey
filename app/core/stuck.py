"""\"Takıldın mı?\" yönlendirmesi: alıştırmanın dayandığı ders başlığı.

Aynı alıştırmada üst üste düşen biri çoğu zaman kodda değil konuda
takılmış oluyor. Üç başarısız denemeden sonra yönergenin altında bir kart
çıkıyor: "Bu alıştırma dersteki *X* kısmına dayanıyor → Derse git".

**Başlık elle yazılmıyor, bulunuyor** (yüzlerce alıştırma var): çözüm
kodundaki adlar (fonksiyon, metot, anahtar kelime, SQL sözcükleri) ve
yönergenin kelimeleri dersin `## ` parçalarında aranıyor. Her ad, kaç
parçada geçtiğine göre ağırlıklandırılıyor (her yerde geçen `print` bir şey
söylemiyor, yalnızca bir parçada geçen `enumerate` çok şey söylüyor). En
yüksek puanlı parça seçiliyor; hiçbiri tutmazsa dersin başı.

Bulunan yer yanlışsa alıştırmanın `exercise.json` dosyasına
`"lesson_anchor": "<çapa>"` yazılır; o kazanır.
"""

from __future__ import annotations

import io
import math
import re
import tokenize
from dataclasses import dataclass

from .search import heading_ids, lesson_chunks

# Bu kadar başarısız denemeden sonra kart çıkıyor.
STUCK_AFTER = 3

_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}")
_PROSE = re.compile(r"[^\W\d_]{4,}", re.UNICODE)

# Her derste geçen ve yer göstermeyen sözcükler.
_STOP = {
    "print", "the", "and", "for", "you", "your", "this", "that", "with", "from", "into",
    "def", "return", "true", "false", "none", "self", "result", "value", "values",
}


@dataclass(frozen=True)
class LessonSpot:
    title: str
    anchor: str  # "" = dersin başı


def code_words(code: str) -> set[str]:
    """Koddaki adlar (yorumlar ve metin sabitleri hariç)."""
    kelimeler: set[str] = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(code).readline):
            if tok.type == tokenize.NAME and len(tok.string) >= 3:
                kelimeler.add(tok.string.lower())
    except (tokenize.TokenError, IndentationError, SyntaxError):
        kelimeler = {w.lower() for w in _WORD.findall(code)}
    return kelimeler - _STOP


def prose_words(text: str) -> set[str]:
    return {w.lower() for w in _PROSE.findall(text)} - _STOP


# Uygulama / özet parçaları alıştırmanın asıl konusu olmuyor; puanları yarıya.
_SIDE = re.compile(r"^(makine öğrenmesinde|in machine learning|özet|summary|sık yapılan|common mistake|yapma)", re.I)


def lesson_spots(lesson_source: str) -> list[LessonSpot]:
    """Dersin `## ` parçaları sırasıyla; ilki başlıksız giriş (çapası "")."""
    parcalar = lesson_chunks(lesson_source)
    capalar = heading_ids(lesson_source)
    return [LessonSpot(baslik, capalar[i - 1] if 0 < i <= len(capalar) else "")
            for i, (baslik, _m) in enumerate(parcalar)]


def chunk_scores(lesson_source: str, aranan: dict[str, float]) -> list[float]:
    """Her ders parçasının aranan kelimelere (kelime → ağırlık) göre puanı.

    Giriş parçası (başlıksız) ders tek parçadan ibaret değilse 0 alıyor.
    """
    parcalar = lesson_chunks(lesson_source)
    return unit_scores(parcalar, aranan, skip={0} if len(parcalar) > 1 else set())


def unit_scores(parcalar: list[tuple[str, str]], aranan: dict[str, float],
                skip: set[int] = frozenset()) -> list[float]:
    """(başlık, metin) parçalarının aranan kelimelere (kelime → ağırlık) göre puanı.

    Kelime kaç parçada geçiyorsa o kadar az değerli (bütün parçalar sayılıyor,
    `skip` dahil); başlığın kendisinde geçiyorsa iki kat. `skip` 0 alıyor.
    """
    metinler = [(baslik + "\n" + metin).lower() for baslik, metin in parcalar]
    puanlar = []
    for i, metin in enumerate(metinler):
        if i in skip:
            puanlar.append(0.0)
            continue
        puan = 0.0
        for kelime, agirlik in aranan.items():
            if kelime not in metin:
                continue
            kac = sum(1 for m in metinler if kelime in m)
            deger = agirlik * math.log(1 + len(metinler) / kac)
            # Başlığın kendisinde geçiyorsa iki kat.
            puan += deger * (2 if kelime in parcalar[i][0].lower() else 1)
        if _SIDE.match(parcalar[i][0]):
            puan /= 2
        puanlar.append(puan)
    return puanlar


def find_spot(lesson_source: str, code: str, prompt: str, override: str = "",
              title: str = "") -> LessonSpot | None:
    """Alıştırmanın dayandığı ders parçası; ders yoksa None."""
    if not lesson_source.strip():
        return None
    yerler = lesson_spots(lesson_source)
    if override:
        for yer in yerler:
            if yer.anchor == override:
                return yer

    aranan = {w: 1.0 for w in prose_words(prompt)}
    aranan.update({w: 2.0 for w in code_words(code)})  # kod adları daha belirleyici
    aranan.update({w: 3.0 for w in prose_words(title)})  # alıştırmanın adı en belirleyici

    puanlar = chunk_scores(lesson_source, aranan)
    en_iyi_puan = max(puanlar)
    if en_iyi_puan <= 0:
        return LessonSpot("", "")
    # Eşitlikte önceki parça (önceki döngü yalnızca büyükse değiştiriyordu).
    return yerler[puanlar.index(en_iyi_puan)]


def failures_since_pass(attempts: list[dict]) -> int:
    """En yeniden geriye, son başarılı denemeye kadar kaç başarısız deneme var."""
    sayi = 0
    for deneme in attempts:
        if deneme.get("passed"):
            break
        sayi += 1
    return sayi
