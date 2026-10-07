pandas ile DuckDB arasında gidip gelmek için gereken satırlar.

## pandas → DuckDB

```python
duckdb.sql("SELECT ... FROM orders")        # değişken adıyla
con = duckdb.connect()
con.register("t", orders)                   # başka bir adla göster
con.sql("SELECT ... FROM t")
```

DuckDB'ye verdiğin tabloda metin sütunlarını `category` yap: bu bölümün
ölçümünde aynı sorgu `str` ile 0,132 sn, `category` ile 0,003 sn sürdü.

## DuckDB → pandas

```python
duckdb.sql("SELECT ...").df()               # DataFrame
duckdb.sql("SELECT ...").fetchall()         # demet listesi
```

Sonuç büyükse `.df()` pahalı; mümkünse DuckDB'de özetleyip küçük sonucu al.

## Parametre

```python
duckdb.execute("SELECT ... WHERE city = ? AND quantity >= ?", ["Izmir", 3])
```

Kullanıcıdan, dosyadan ya da dışarıdan gelen her değer `?` ile verilir;
f-string ile sorguya eklenmez.

## Sonucu adım adım kullanmak

```python
cash = duckdb.sql("SELECT * FROM 'orders.parquet' WHERE payment = 'cash'")
duckdb.sql("SELECT city, count(*) FROM cash GROUP BY city")
```

`cash` bir tarif; kullanılınca çalışıyor.

## Birleştirme ve pencere

```sql
SELECT ...
FROM 'orders.parquet' AS o
JOIN customers AS c USING (customer_id);

SELECT *
FROM 'orders.parquet'
QUALIFY row_number() OVER (PARTITION BY customer_id ORDER BY order_time) = 1;
```

## Hangisi ne zaman?

| Durum | Seçim |
|---|---|
| Veri dosyada, büyük | DuckDB |
| Birleştirme, pencere, "her grubun ilki" | DuckDB (SQL daha kısa) |
| Veri bellekte, doğru türlerde, küçük-orta | pandas yeterli |
| Adım adım temizlik, grafik, `pivot` | pandas |
| Belleğe sığmayan veri | DuckDB |
