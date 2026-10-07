Aya göre bölünmüş klasörü DuckDB ile tek tablo gibi sorgula.

**Yapman gerekenler:**

1. Başlangıç kodu 200 000 siparişi `orders/month=YYYY-MM/part-0.parquet`
   düzeninde yazıyor.
2. `'orders/*/*.parquet'` ile bütün dosyalardaki sipariş sayısını bul ve
   yazdır.
3. `read_parquet('orders/*/*.parquet', hive_partitioning = true)` ile
   yılın ilk çeyreğini (`month <= '2024-03'`) seç; ay başına sipariş
   sayısını aya göre sıralı al ve her satıra ay ve sayıyı yazdır.

**Beklenen çıktı:**

```
200000
2024-01 16921
2024-02 15911
2024-03 16591
```
