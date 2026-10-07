Bir Parquet dosyasına DuckDB ile üç soru sor.

**Yapman gerekenler:**

1. `make_orders(100_000)` tablosunu `orders.parquet` olarak yaz
   (`index=False`).
2. Tek bir `duckdb.sql(...)` sorgusuyla şu üçünü al ve `fetchone()` ile
   oku:
   - sipariş sayısı (`count(*)`),
   - farklı şehir sayısı (`count(DISTINCT city)`),
   - toplam satılan adet (`sum(quantity)`).
3. Üç değeri ayrı satırlara yazdır.

**Beklenen çıktı:**

```
100000
8
222191
```
