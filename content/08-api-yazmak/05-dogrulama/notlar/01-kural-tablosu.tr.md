Hazır kuralların hepsi tek tabloda, `422` cevabındaki `type` adlarıyla.

## Sayılar

| Kural | Anlamı | Bozulunca `type` |
|---|---|---|
| `gt=0` | 0'dan büyük | `greater_than` |
| `ge=1` | 1 ya da büyük | `greater_than_equal` |
| `lt=100` | 100'den küçük | `less_than` |
| `le=5` | 5 ya da küçük | `less_than_equal` |
| `multiple_of=0.5` | 0,5'in katı | `multiple_of` |

`Field(gt=0, multiple_of=0.5)` olan fiyata `1.25` → `422` multiple_of
(ölçtük).

## Metinler

| Kural | Anlamı | Bozulunca `type` |
|---|---|---|
| `min_length=1` | en az 1 karakter | `string_too_short` |
| `max_length=100` | en fazla 100 karakter | `string_too_long` |
| `pattern=r"..."` | düzenli ifadeye uymalı | `string_pattern_mismatch` |

## Listeler

`Field(max_length=3)` bir **listede** öğe sayısını sınırlar:
`tags: list[str] = Field(default=[], max_length=3)` olan alana dört etiket
→ `422` too_long, mesaj `List should have at most 3 items after
validation, not 4`.

## Sık kullanılan kalıplar (`pattern`)

| Kalıp | Ne ister? | Örnek |
|---|---|---|
| `^[0-9]{13}$` | tam 13 rakam | `9780441013593` |
| `^[a-z0-9_]+$` | küçük harf, rakam, alt çizgi | `ada_99` |
| `^[A-Z]{2}$` | iki büyük harf | `TR` |
| `^\d{4}-\d{2}-\d{2}$` | tarih biçimi | `2026-10-07` |

`^` başı, `$` sonu bağlar: yazılmazsa kalıp metnin **bir yerinde** geçmek
yeter (`"abc9780441013593xyz"` de uyar). Kalıbı her zaman `r"..."` ile
yaz; ters bölü (`\d`) öyle bozulmaz.

## Nereye ne yazılır?

| Yer | Yazım |
|---|---|
| Gövde (model alanı) | `year: int = Field(ge=1450)` |
| Sorgu | `limit: Annotated[int, Query(ge=1)] = 10` |
| Yol | `book_id: Annotated[int, Path(gt=0)]` |

Kuralların adları üçünde de aynı.
