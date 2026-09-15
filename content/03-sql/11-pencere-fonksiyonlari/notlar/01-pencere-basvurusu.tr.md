Bu bölümün işlevleri tek sayfada. Sonuçlar Orta Seviyenin sekiz tablolu
şemasında ölçüldü.

## Yazım

```sql
ISLEV(...) OVER (
    PARTITION BY grup_sutunu     -- istege bagli
    ORDER BY sira_sutunu         -- siralama islevlerinde sart
    ROWS BETWEEN ... AND ...     -- istege bagli: cerceve
)
```

## Sıralama işlevleri

| İşlev | Eşitlikte | Stok örneği (99, 99, 60) |
|---|---|---|
| `ROW_NUMBER()` | farklı numara; eşitlerden hangisinin önce geldiği belli değil | 1, 2, 3 |
| `RANK()` | aynı numara, sonra atlıyor | 1, 1, 3 |
| `DENSE_RANK()` | aynı numara, atlamıyor | 1, 1, 2 |
| `NTILE(n)` | satırları n gruba bölüyor; artanlar baştakilere | 12 satır, n = 5 → 3, 3, 2, 2, 2 |
| `PERCENT_RANK()` | 0 ile 1 arası sıra | ACC stokları: 0,0 … 1,0 |
| `CUME_DIST()` | bu değere kadar olanların oranı | ACC'de en az stok: 0,1667 |

## Önceki, sonraki, uçlar

| İşlev | Ne veriyor |
|---|---|
| `LAG(x)` | bir önceki satırın değeri; yoksa `NULL` |
| `LAG(x, 1, 0)` | yoksa `0` |
| `LAG(x, 2)` | iki satır öncesi |
| `LEAD(x)` | bir sonraki satırın değeri |
| `FIRST_VALUE(x)` | çerçevenin ilk değeri |
| `LAST_VALUE(x)` | çerçevenin son değeri — **varsayılan çerçevede satırın kendisi** |

## Toplama işlevleri pencereyle

| Yazım | Ne veriyor | Ölçüldü |
|---|---|---|
| `SUM(x) OVER ()` | bütün sonucun toplamı | — |
| `SUM(x) OVER (PARTITION BY g)` | grubun toplamı | — |
| `SUM(x) OVER (ORDER BY t)` | birikimli; **eşitler birlikte** | 1001'in üç kalemi: 1815, 1815, 1815 |
| `SUM(SUM(x)) OVER (...)` | `GROUP BY` sonucunun üstüne pencere | kategori toplamı 99165.00 |
| `COUNT(*) OVER (PARTITION BY g)` | grubun satır sayısı, her satırda | 1. müşteri: 3 |
| `AVG(x) OVER (...)` | tam sayı sütunda tam sayı | 19 (doğrusu 19,33) |

## Çerçeveler

| Yazım | Hesaba giren satırlar |
|---|---|
| çerçeve yok, `ORDER BY` yok | grubun tamamı |
| çerçeve yok, `ORDER BY` var | baştan **bu değere** kadar (eşitler birlikte) |
| `ROWS UNBOUNDED PRECEDING` | baştan **bu satıra** kadar |
| `ROWS BETWEEN 1 PRECEDING AND CURRENT ROW` | önceki satır ve bu satır |
| `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` | önceki, bu, sonraki |
| `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` | grubun tamamı |
| `RANGE BETWEEN 1 PRECEDING AND CURRENT ROW` | hata — `RANGE` sayı almıyor |

## Nerede yazılabiliyor

| Yer | Yazılabilir mi |
|---|---|
| `SELECT` | evet |
| `ORDER BY` | evet |
| `WHERE` | hayır |
| `UPDATE ... SET` | hayır |

Süzmek için numaralı sorgu `FROM (...) AS t` içine alınıyor ve `WHERE`
dışarıda yazılıyor.

## Hata metinleri

| Yazım | Mesaj |
|---|---|
| `ROW_NUMBER() OVER ()` | `The function 'ROW_NUMBER' must have an OVER clause with ORDER BY.` |
| `WHERE ROW_NUMBER() OVER (...) <= 3` | `Windowed functions can only appear in the SELECT or ORDER BY clauses.` |
| `... AS rn ... WHERE rn <= 3` (aynı sorguda) | `Invalid column name 'rn'.` |
| `RANGE BETWEEN 1 PRECEDING AND CURRENT ROW` | `RANGE is only supported with UNBOUNDED and CURRENT ROW window frame delimiters.` |

## Kalıplar

```sql
-- her grubun ilki
SELECT * FROM (
    SELECT ..., ROW_NUMBER() OVER (PARTITION BY g ORDER BY x DESC, id) AS rn
    FROM t
) AS s
WHERE rn = 1;

-- birikimli toplam
SUM(x) OVER (ORDER BY t, id ROWS UNBOUNDED PRECEDING)

-- onceki satirla fark
x - LAG(x) OVER (PARTITION BY g ORDER BY t)

-- toplamdaki pay
100.0 * x / SUM(x) OVER ()
```
