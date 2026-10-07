400 000 satırlık CSV'yi 100 000 satırlık parçalarla tek bir Parquet
dosyasına çevir.

**Yapman gerekenler:**

1. `pd.read_csv("orders.csv", chunksize=100_000, dtype=NUMERIC)` ile oku.
2. Her parçaya `month` sütununu ekle (`order_time`'ın ilk 7 harfi).
3. İlk parçada `pq.ParquetWriter("orders.parquet", şema,
   compression="zstd")` aç, her parçayı `write_table` ile yaz, sonda kapat.
4. Yazdır: satır sayısı, satır grubu sayısı, CSV ve Parquet boyutları (MB,
   bir ondalık, aynı satırda).
5. Yalnızca `month` sütununu okuyup kaç farklı ay olduğunu yazdır.

**Beklenen çıktı:**

```
400000
4
24.1 7.1
12
```
