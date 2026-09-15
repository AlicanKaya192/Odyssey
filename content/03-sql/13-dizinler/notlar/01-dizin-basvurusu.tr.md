Bu bölümün yazımları ve ölçümleri tek sayfada. Ölçümler 20 000 satırlık
`events` tablosunda yapıldı; tablonun verisi 150 sayfa.

## Yazım

```sql
-- tek sutun
CREATE INDEX ix_events_created ON events (created_at);

-- bilesik: once ilk sutuna, sonra ikinciye gore sirali
CREATE INDEX ix_events_customer_created ON events (customer_id, created_at);

-- kapsayan: amount siralamaya girmez, dizinde durur
CREATE INDEX ix_events_created ON events (created_at) INCLUDE (amount);

-- suzgecli: yalnizca kosula uyan satirlar
CREATE INDEX ix_events_amount ON events (amount) WHERE amount IS NOT NULL;

-- benzersiz
CREATE UNIQUE INDEX ux_customers_name ON customers (name);

-- silmek: tablo adi sart
DROP INDEX ix_events_created ON events;
```

## Dizinleri görmek

```sql
SELECT name, type_desc
FROM sys.indexes
WHERE object_id = OBJECT_ID('events') AND type > 0;
```

`type > 0` tablonun dizinsiz hâlini (heap) dışarıda bırakıyor. Her
tablonun birincil anahtarı `CLUSTERED` olarak görünüyor.

## Plan terimleri

| Terim | Anlamı |
|---|---|
| Clustered Index Seek | birincil anahtarla doğrudan satıra |
| Clustered Index Scan | tablonun tamamı |
| Index Seek | kümelenmemiş dizinde doğrudan yere |
| Index Scan | kümelenmemiş dizinin tamamı |
| Key Lookup | dizinde olmayan sütun için tabloya dönüş, satır başına |

## Ölçülenler

| Durum | Okuma |
|---|---|
| `id = 10000` | 2 |
| bir gün, dizinsiz | 150 |
| bir gün, `created_at` dizini | 2 |
| bir gün, `YEAR`/`MONTH`/`DAY` ile | 42 |
| bir gün, `CAST(created_at AS DATE)` ile | 2 |
| bir gün, `SELECT *` | 150 (dizin kullanılmadı) |
| bir gün `created_at, amount`, `INCLUDE (amount)` ile | 3 |
| 15 satın alma, Index Seek + Key Lookup | 130 |
| müşteri 3, `(customer_id, created_at)` | 11 |
| müşteri 3, `(created_at, customer_id)` | 52 |
| `LIKE 'S0050%'` / `LIKE '%0050'` | 3 / 54 |
| `amount > 490`, süzgeçli dizin | 2 |
| tek satır `INSERT`, dizinsiz / beş dizinle | 2 / 22 |

## Hata metinleri

| Durum | Mesaj |
|---|---|
| tekrarlı sütuna benzersiz dizin | `The CREATE UNIQUE INDEX statement terminated because a duplicate key was found ...` |
| benzersiz dizine tekrar eklemek | `Cannot insert duplicate key row in object ... with unique index ...` |
| aynı adla ikinci dizin | `The operation failed because an index or statistics with name ... already exists on table ...` |
| olmayan dizini silmek | `Cannot drop the index ..., because it does not exist or you do not have permission.` |
| `DROP INDEX` tablo adı olmadan | `Must specify the table name and index name for the DROP INDEX statement.` |
| `UNIQUE` kuralının dizinini silmek | `An explicit DROP INDEX is not allowed on index ... It is being used for UNIQUE KEY constraint enforcement.` |

## Ölçmek

```sql
SET STATISTICS IO ON;
SELECT ...;          -- mesajda: Table '...'. Scan count ..., logical reads ...
SET STATISTICS IO OFF;
```

Bu uygulamanın sonuç tablosu mesajları göstermiyor; SQL Server Management
Studio'da *Messages* sekmesinde görünüyor.
