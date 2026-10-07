Bellekteki bir pandas tablosunu DuckDB ile değişken adından sorgula.

**Yapman gerekenler:**

1. `df = make_orders(100_000)` tablosunu kur.
2. `duckdb.sql(...)` içinde `FROM df` yazarak ödeme türü başına sipariş
   sayısını bul; sayıya göre büyükten küçüğe sırala.
3. Sonucu `fetchall()` ile al ve her satıra ödeme türünü ve sayıyı yazdır.

**Beklenen çıktı:**

```
card 72243
transfer 19885
cash 7872
```
