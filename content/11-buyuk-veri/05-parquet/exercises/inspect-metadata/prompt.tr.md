Bir Parquet dosyasının özetini veriyi hiç okumadan çıkar.

**Yapman gerekenler:**

1. Başlangıç kodu 200 000 siparişi 50 000 satırlık gruplarla
   `orders.parquet` olarak yazıyor.
2. Dosyayı `pq.ParquetFile` ile aç.
3. Satır sayısını, satır grubu sayısını ve sütun sayısını aynı satıra
   yazdır (`metadata.num_rows`, `num_row_groups`, `num_columns`).
4. Sütun adlarını (`schema_arrow.names`) bir döngüyle, her biri ayrı
   satırda yazdır.
5. İlk satır grubunun satır sayısını yazdır.

**Beklenen çıktı:**

```
200000 4 8
order_id
order_time
customer_id
city
category
quantity
unit_price
payment
50000
```
