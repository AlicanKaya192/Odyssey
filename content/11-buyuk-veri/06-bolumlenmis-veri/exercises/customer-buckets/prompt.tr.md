Siparişleri müşteri numarasına göre dört kovaya böl; bir müşterinin
siparişlerini yalnızca bir kova okuyarak bul.

**Yapman gerekenler:**

1. `make_orders(200_000)` ile `df` tablosunu kur.
2. `bucket = customer_id % 4` sütununu ekle; her kovayı
   `buckets/bucket=<n>/part-0.parquet` olarak yaz (`bucket` sütunu
   çıkarılmış, `index=False`).
3. `customer = 1234` için kova numarasını hesapla ve yazdır.
4. Yalnızca o kovanın dosyasını oku; dosyadaki satır sayısını yazdır.
5. Okunan tabloda bu müşterinin sipariş sayısını yazdır.
6. Aynı sayıyı `df`'den doğrudan süzerek bul ve iki sayının eşit olup
   olmadığını yazdır.

**Beklenen çıktı:**

```
2
50183
7
True
```

Dört dosyadan yalnızca biri okundu, sonuç doğru.
