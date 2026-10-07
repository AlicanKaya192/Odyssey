Diskteki siparişleri bellekteki müşteri tablosuyla birleştirip segment
başına ciroyu bul.

**Yapman gerekenler:**

1. Başlangıç kodu 200 000 siparişi `orders.parquet` olarak yazıyor ve
   `customers` tablosunu (`customer_id`, `segment`) kuruyor.
2. Tek bir DuckDB sorgusunda `'orders.parquet'` ile `customers`'ı
   `customer_id` üzerinden birleştir.
3. Segment başına sipariş sayısını ve milyon TL olarak ciroyu
   (`quantity * unit_price` toplamı / 1e6, iki ondalık) bul; segmente göre
   sırala.
4. Her satıra segmenti, sipariş sayısını ve ciroyu yazdır.

**Beklenen çıktı:**

```
new 66603 109.69
regular 67034 109.75
vip 66363 107.99
```
