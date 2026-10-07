Bir CSV'yi belleğe hiç tamamen almadan tek bir Parquet dosyasına çevir.

**Yapman gerekenler:**

1. `write_orders_csv("orders.csv", 300_000)` ile CSV'yi yaz.
2. CSV'yi 100 000 satırlık parçalarla oku (`parse_dates=["order_time"]`).
3. Her parçayı `pa.Table.from_pandas(chunk, preserve_index=False)` ile
   `pyarrow` tablosuna çevir. İlk parçada `pq.ParquetWriter("orders.parquet",
   table.schema)` ile yazıcıyı aç; her parçayı `write_table` ile yaz.
4. Döngüden sonra yazıcıyı kapat.
5. Dosyanın satır ve satır grubu sayısını aynı satıra yazdır.
6. CSV'deki ve Parquet'deki `quantity` toplamlarını aynı satıra yazdır.

**Beklenen çıktı:**

```
300000 3
667058 667058
```

Üç parça, üç satır grubu; iki toplam aynı.
