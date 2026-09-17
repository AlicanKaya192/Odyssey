"""Matematik problemlerinin cevap denetimi.

Kod alıştırmasından farkı: kullanıcı kod değil **cevap** yazıyor ve cevap
çalıştırılmıyor, karşılaştırılıyor. Karar yine deterministik: yapay zeka
yok, "yakın sayılır" diye bir yorum yok.

Bir problem bir ya da birkaç cevap alanı taşıyor (`exercise.json` →
`answers`). Her alan:

```json
{ "label": {"tr": "x", "en": "x"}, "value": "19" }
{ "label": {...}, "value": "14.21", "tolerance": 0.01 }
{ "label": {...}, "accept": ["tanımsız", "undefined"] }
```

- **Sayılar kesin karşılaştırılıyor.** `1/2`, `0.5` ve `0,5` aynı cevap;
  ondalık sayı yuvarlama hatası olmasın diye karşılaştırma `Fraction` ile.
- `tolerance` yalnızca yuvarlanmış bir sonuç istenen yerde veriliyor
  ("iki ondalık"); o durumda fark tolerans kadar olabiliyor.
- `accept` sayı olmayan cevaplar için ("tanımsız"). Büyük/küçük harf ve
  Türkçe `ı/i` farkı gözetilmiyor.
"""

from __future__ import annotations

import re
from fractions import Fraction

# Kullanıcının yazabileceği eksi işaretleri: klavyedeki tire, matematikteki
# eksi (U+2212) ve uzun tire.
_MINUS = str.maketrans({"−": "-", "–": "-", "—": "-"})

_NUMBER = re.compile(r"^[+-]?(\d+([.,]\d*)?|[.,]\d+)$")
_FRACTION = re.compile(r"^([+-]?\d+)\s*/\s*([+-]?\d+)$")


def parse_number(text: str) -> Fraction | None:
    """Bir cevabı sayıya çevirir; sayı değilse `None`.

    Kabul edilenler: `19`, `-4`, `−4`, `3.5`, `3,5`, `1/2`, `-3/4`.
    Binlik ayıracı yok: `1.000` ve `1,000` ondalık okunuyor, yani bir.
    Nokta ile virgül iki dilde farklı işler görüyor; ikisini de ondalık
    saymak tek tutarlı yol. Problemler bu yüzden büyük sayıları ayıraçsız
    istiyor.
    """
    cleaned = text.strip().translate(_MINUS).replace(" ", "")
    if not cleaned:
        return None

    fraction = _FRACTION.match(cleaned)
    if fraction:
        denominator = int(fraction.group(2))
        if denominator == 0:
            return None
        return Fraction(int(fraction.group(1)), denominator)

    if _NUMBER.match(cleaned):
        return Fraction(cleaned.replace(",", "."))
    return None


def _fold(text: str) -> str:
    """Harf büyüklüğü ve Türkçe `ı/i/İ/I` farkını siler."""
    return (
        text.strip()
        .replace("İ", "i").replace("I", "i").replace("ı", "i")
        .casefold()
    )


def is_correct(spec: dict, given: str) -> bool:
    """Tek bir alanın cevabı doğru mu?"""
    accepted = [_fold(item) for item in spec.get("accept", [])]
    if accepted and _fold(given) in accepted:
        return True

    expected = spec.get("value")
    if expected is None:
        return False

    number = parse_number(given)
    target = parse_number(str(expected))
    if number is None or target is None:
        return False

    tolerance = spec.get("tolerance")
    if tolerance is None:
        return number == target
    return abs(number - target) <= Fraction(str(tolerance))


def check_all(specs: list[dict], answers: list[str]) -> list[bool]:
    """Her alan için doğru/yanlış. Eksik cevap yanlış sayılıyor."""
    return [
        is_correct(spec, answers[index] if index < len(answers) else "")
        for index, spec in enumerate(specs)
    ]


def is_readable(spec: dict, given: str) -> bool:
    """Cevap en azından okunabiliyor mu?

    Yanlış bir sayı ile hiç sayı olmayan bir metin farklı geri bildirim
    alıyor: ikincisinde kullanıcıya "bunu sayı olarak okuyamadım" deniyor,
    yoksa "3 buçuk" yazan kişi cevabının yanlış olduğunu sanır.
    """
    if parse_number(given) is not None:
        return True
    return bool(spec.get("accept")) and bool(given.strip())
