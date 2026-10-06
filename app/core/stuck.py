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


def _code_words(code: str) -> set[str]:
    """Koddaki adlar (yorumlar ve metin sabitleri hariç)."""
    kelimeler: set[str] = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(code).readline):
            if tok.type == tokenize.NAME and len(tok.string) >= 3:
                kelimeler.add(tok.string.lower())
    except (tokenize.TokenError, IndentationError, SyntaxError):
        kelimeler = {w.lower() for w in _WORD.findall(code)}
    return kelimeler - _STOP


def _prose_words(text: str) -> set[str]:
    return {w.lower() for w in _PROSE.findall(text)} - _STOP


# Uygulama / özet parçaları alıştırmanın asıl konusu olmuyor; puanları yarıya.
_SIDE = re.compile(r"^(makine öğrenmesinde|in machine learning|özet|summary|sık yapılan|common mistake|yapma)", re.I)


def find_spot(lesson_source: str, code: str, prompt: str, override: str = "",
              title: str = "") -> LessonSpot | None:
    """Alıştırmanın dayandığı ders parçası; ders yoksa None."""
    if not lesson_source.strip():
        return None
    parcalar = lesson_chunks(lesson_source)
    capalar = heading_ids(lesson_source)
    basliklar = [(baslik, capalar[i - 1] if 0 < i <= len(capalar) else "") for i, (baslik, _m) in enumerate(parcalar)]
    if override:
        for baslik, capa in basliklar:
            if capa == override:
                return LessonSpot(baslik, capa)

    metinler = [(baslik + "\n" + metin).lower() for baslik, metin in parcalar]
    aranan = {w: 1.0 for w in _prose_words(prompt)}
    aranan.update({w: 2.0 for w in _code_words(code)})  # kod adları daha belirleyici
    aranan.update({w: 3.0 for w in _prose_words(title)})  # alıştırmanın adı en belirleyici

    en_iyi, en_iyi_puan = 0, 0.0
    for i, metin in enumerate(metinler):
        if i == 0 and len(metinler) > 1:
            continue  # giriş parçası (başlıksız) ancak tek parçaysa
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
        if puan > en_iyi_puan:
            en_iyi, en_iyi_puan = i, puan
    if en_iyi_puan <= 0:
        return LessonSpot("", "")
    baslik, capa = basliklar[en_iyi]
    return LessonSpot(baslik, capa)


def failures_since_pass(attempts: list[dict]) -> int:
    """En yeniden geriye, son başarılı denemeye kadar kaç başarısız deneme var."""
    sayi = 0
    for deneme in attempts:
        if deneme.get("passed"):
            break
        sayi += 1
    return sayi
