Bu bölümün yazımları ve kuralları tek sayfada. Sonuçlar Orta Seviyenin
sekiz tablolu şemasında ölçüldü.

## Yazım

```sql
-- tek CTE
WITH ad AS (
    SELECT ...
)
SELECT ... FROM ad;

-- birden fazla: virgulle, her biri oncekileri gorur
WITH a AS (SELECT ...),
     b AS (SELECT ... FROM a)
SELECT ... FROM b;

-- sutunlara ad vermek
WITH x (product, cost) AS (
    SELECT name, price FROM products
)
SELECT product, cost FROM x;

-- ozyinelemeli
WITH r AS (
    SELECT ...                  -- baslangic: bir kez
    UNION ALL
    SELECT ... FROM ... JOIN r  -- kendini cagiran parca
)
SELECT ... FROM r
OPTION (MAXRECURSION 200);      -- istege bagli, cumlenin sonunda
```

## Kurallar

| Kural | Ölçülen |
|---|---|
| `WITH`'ten önceki cümle `;` ile biter | yoksa iki farklı sözdizimi hatası |
| CTE yalnızca hemen ardından gelen cümlede geçerli | ikinci cümlede `Invalid object name` |
| CTE başka bir CTE'yi ancak **kendinden önce** tanımlandıysa kullanır | `Invalid object name 'b'` |
| Aynı `WITH` içinde her ad bir kez | `Duplicate common table expression name` |
| CTE içinde `ORDER BY` yalnızca `TOP` / `OFFSET` ile | yoksa hata 1033 |
| CTE'nin içine `WITH` yazılamaz | sözdizimi hatası |
| CTE `SELECT`, `DELETE`, `UPDATE` önüne yazılabilir | değişiklik asıl tabloya gidiyor |

## Özyinelemeli CTE kuralları

| Kural | Ölçülen |
|---|---|
| İki parça `UNION ALL` ile | `UNION` → hata 252 |
| Sütun tipleri iki parçada aynı | yoksa `Types don't match between the anchor and the recursive part` |
| Kendini çağıran parçada toplama yok | `MAX`, `GROUP BY`, `HAVING` → hata 467 |
| Kendini çağıran parçada dış birleştirme yok | `LEFT JOIN` → hata 462 |
| Varsayılan sınır 100 adım | 101 satır geçti, 102 durdu |
| `OPTION (MAXRECURSION n)` | `0` sınırsız; en fazla 32767; CTE'nin içine yazılamaz |

## Hata metinleri

| Durum | Mesaj |
|---|---|
| `SET` ardından noktalı virgülsüz `WITH` | `Incorrect syntax near the keyword 'with'. ... the previous statement must be terminated with a semicolon.` |
| `SELECT` ardından noktalı virgülsüz `WITH` | `Incorrect syntax near 'x'. If this is intended to be a common table expression, you need to explicitly terminate the previous statement with a semi-colon.` |
| CTE içinde `ORDER BY` | `The ORDER BY clause is invalid in views, inline functions, derived tables, subqueries, and common table expressions, unless TOP, OFFSET or FOR XML is also specified.` |
| `UNION` ile özyineleme | `Recursive common table expression 'chain' does not contain a top-level UNION ALL operator.` |
| Tip uyuşmazlığı | `Types don't match between the anchor and the recursive part in column "path" of recursive query "chain".` |
| Sınır aşıldı | `The statement terminated. The maximum recursion 100 has been exhausted before statement completion.` |
| Sınır çok büyük | `The value 40000 specified for the MAXRECURSION option exceeds the allowed maximum of 32767.` |

## Kalıplar

```sql
-- her grubun ilki
WITH ranked AS (
    SELECT ..., ROW_NUMBER() OVER (PARTITION BY g ORDER BY x DESC, id) AS rn
    FROM t
)
SELECT ... FROM ranked WHERE rn = 1;

-- tekrarlari silmek (bir tanesi kalir)
WITH d AS (
    SELECT ROW_NUMBER() OVER (PARTITION BY anahtar ORDER BY id) AS rn
    FROM t
)
DELETE FROM d WHERE rn > 1;

-- agacta asagi
... UNION ALL SELECT e.* FROM t e JOIN r ON e.parent_id = r.id

-- agacta yukari
... UNION ALL SELECT e.* FROM t e JOIN r ON e.id = r.parent_id

-- ay dizisi
WITH months AS (
    SELECT CAST('2026-01-01' AS DATE) AS month
    UNION ALL
    SELECT DATEADD(month, 1, month) FROM months WHERE month < '2026-06-01'
)
SELECT month FROM months;
```
