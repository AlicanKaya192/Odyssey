SQL patikasının tamamı tek sayfada. Ayrıntılar ve ölçümler her bölümün
kendi notlarında.

## Sorgunun iskeleti

```sql
SELECT   sutunlar, hesaplar AS ad, TOPLAMA(...), PENCERE() OVER (...)  -- 5
FROM     tablo t                                                       -- 1
JOIN     diger d ON d.anahtar = t.anahtar                              -- 1
WHERE    satirin kosulu                                                -- 2
GROUP BY gruplama sutunlari                                            -- 3
HAVING   grubun kosulu                                                 -- 4
ORDER BY siralama                                                      -- 6
-- TOP n, SELECT'in hemen arkasina yaziliyor                           -- 7
```

Numara, sunucunun çalıştırdığı sıra. Takma ad yalnızca `ORDER BY`'da
görünüyor.

## Süzmek (01, 03)

| Yazım | Not |
|---|---|
| `=`, `<>`, `<`, `>=` | `NULL` ile çalışmıyor |
| `IS NULL`, `IS NOT NULL` | `NULL`'un tek doğru sınaması |
| `IN (...)`, `NOT IN (...)` | listede `NULL` varsa `NOT IN` hiç satır getirmiyor |
| `BETWEEN a AND b` | iki uç dahil |
| `LIKE 'M%'`, `'%e'`, `'_a%'` | `%` her şey, `_` tek karakter |
| `AND`, `OR`, `NOT` | parantezle grupla |

## Sıralamak ve sınırlamak (02)

`ORDER BY sütun [ASC|DESC]` — `NULL` artan sırada başta. `TOP n`,
`TOP n WITH TIES`, `OFFSET ... FETCH`. Sıra önemliyse `ORDER BY` şart.

## Hesaplamak (04)

Aritmetik (`7 / 2` = 3), `CAST`, `TRY_CAST`, `ROUND`, `CONCAT`,
`COALESCE`, `NULLIF`, `CASE WHEN ... THEN ... ELSE ... END`, `LEN`,
`UPPER`, `LEFT`, `SUBSTRING`, `REPLACE`, `TRIM`.

## Gruplamak (05)

`COUNT(*)`, `COUNT(sütun)` (`NULL`'u saymaz), `COUNT(DISTINCT ...)`,
`SUM`, `AVG` (tam sayıda tam sayı), `MIN`, `MAX`. `SELECT`'teki toplama
dışı her sütun `GROUP BY`'da olmalı.

## Birleştirmek (06)

| Tür | Eşleşmeyen |
|---|---|
| `JOIN` | düşer |
| `LEFT JOIN` | soldaki kalır, sağ `NULL` |
| `FULL JOIN` | ikisi de kalır |

Sağ tabloya ait koşul `LEFT JOIN`'de `ON`'a. Birleştirme satır çoğaltır:
`COUNT(DISTINCT ...)`.

## Alt sorgu (07)

`WHERE x = (SELECT ...)` tek değer ister; `IN (SELECT ...)`, `EXISTS`,
`NOT EXISTS`, `FROM (SELECT ...) AS t`.

## Değiştirmek (08)

```sql
INSERT INTO t (a, b) VALUES (1, 'x'), (2, 'y');
UPDATE t SET a = a + 1 WHERE ...;       -- WHERE'siz: her satir
DELETE FROM t WHERE ...;
BEGIN TRAN; ...; ROLLBACK;              -- once dene
```

## Tablo tasarımı (09)

```sql
CREATE TABLE t (
    id INT IDENTITY(1,1) PRIMARY KEY,
    code NVARCHAR(10) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    status NVARCHAR(20) NOT NULL DEFAULT 'open',
    parent_id INT NULL REFERENCES parents (id) ON DELETE CASCADE
);
ALTER TABLE t ADD c INT NULL;   DROP TABLE t;
```

## Tarih ve metin (10)

`DATEADD`, `DATEDIFF` (sınır sayar), `EOMONTH`, `DATEFROMPARTS`, dönem
için `>= başlangıç AND < sonraki başlangıç`, `DATETIME`'a `'YYYYMMDD'`,
`CHARINDEX`, `STRING_AGG ... WITHIN GROUP (ORDER BY ...)`, `FORMAT` en
sonda, Türkçe I için `COLLATE`.

## Pencere (11)

`ROW_NUMBER` / `RANK` / `DENSE_RANK`, `SUM(...) OVER (ORDER BY ... ROWS
UNBOUNDED PRECEDING)`, `LAG`, `LEAD`, `x / SUM(x) OVER ()`. Grubun ilki:
iç sorgu + dışarıda `WHERE rn = 1`.

## WITH (12)

`WITH a AS (...), b AS (... FROM a) SELECT ...;` — önceki cümle `;` ile
biter. Özyineleme: başlangıç + `UNION ALL` + kendini çağıran parça;
`OPTION (MAXRECURSION n)` cümlenin sonunda.

## Dizin (13)

`CREATE INDEX ix ON t (a, b) INCLUDE (c) WHERE ...;` — ilk sütunla
aranır; sütuna işlev, başı `%` olan `LIKE` taramaya düşürür; her dizin
yazmayı pahalılaştırır. Ölçmek: `SET STATISTICS IO ON`.

## Görünüm ve yordam (14)

`CREATE VIEW dbo.v AS SELECT ...` (`ORDER BY` yok, sütunları adıyla),
`WITH CHECK OPTION`; `CREATE PROCEDURE dbo.p @x INT, @y INT OUTPUT AS
...`, `EXEC dbo.p 1, @n OUTPUT`, `THROW 50001, N'...', 1;`. İkisi de kendi
toplu işinde: araya `GO`.
