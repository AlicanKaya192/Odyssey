DuckDB ile en sık yazacağın satırlar.

## Sorgu ve sonuç

```python
import duckdb

r = duckdb.sql("SELECT ... FROM 'orders.parquet'")
print(r)              # kutulu tablo
r.fetchall()          # [(...), (...)] demet listesi
r.fetchone()          # ilk satır, bir demet
r.df()                # pandas DataFrame
```

## Dosyaları okumak

```sql
FROM 'orders.parquet'                       -- tek dosya
FROM 'orders.csv'                           -- CSV de olur
FROM 'orders/*/*.parquet'                   -- joker: bütün dosyalar
FROM read_parquet('orders/*/*.parquet', hive_partitioning = true)
FROM read_csv('zip.csv', types = {'zip': 'VARCHAR'})   -- türü elle ver
```

## Tabloyu tanımak

```sql
DESCRIBE SELECT * FROM 'orders.csv';
SUMMARIZE SELECT * FROM 'orders.parquet';
SELECT column_name, column_type FROM (DESCRIBE SELECT * FROM 'orders.csv');
```

## Kalıcı veritabanı

```python
con = duckdb.connect("shop.duckdb")
con.sql("CREATE TABLE orders AS SELECT * FROM 'orders.parquet'")
con.sql("SELECT count(*) FROM orders")
con.close()
```

## Dosyaya yazmak

```sql
COPY (SELECT ...) TO 'out.csv' (HEADER);
COPY (SELECT ...) TO 'out.parquet' (FORMAT parquet, COMPRESSION zstd);
COPY (SELECT ...) TO 'out' (FORMAT parquet, PARTITION_BY (month));
```

`PARTITION_BY` bölüm klasörlerini kendisi açıyor: `out/month=2024-01/data_0.parquet`.

## İşe yarayan işlevler

| İşlev | Ne yapar |
|---|---|
| `count(*)`, `sum`, `avg`, `min`, `max` | Bildiğin toplu işlevler |
| `count(DISTINCT x)` | Kesin farklı değer sayısı |
| `approx_count_distinct(x)` | Yaklaşık farklı değer sayısı (az bellek) |
| `strftime(t, '%Y-%m')` | Tarihi metne çevirir |
| `round(x, 2)` | Yuvarlar |
| `x::DOUBLE`, `x::VARCHAR` | Tür çevirir |
| <code>a &#124;&#124; b</code> | Metinleri birleştirir |

## Bu patikanın ölçümü (bir milyon sipariş, şehir başına ciro)

| Yol | Süre |
|---|---|
| pandas, CSV | 1,78 sn |
| DuckDB, CSV | 0,208 sn |
| pandas, Parquet | 0,059 sn |
| DuckDB, Parquet | 0,011 sn |
