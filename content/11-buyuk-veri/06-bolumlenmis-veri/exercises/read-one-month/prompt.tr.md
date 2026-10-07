Aya göre bölünmüş veriden yalnızca Haziran'ı oku ve bütün klasörleri
okumakla karşılaştır.

**Yapman gerekenler:**

1. Başlangıç kodu 200 000 siparişi `orders/month=YYYY-MM/part-0.parquet`
   düzeninde yazıyor.
2. Yalnızca `orders/month=2024-06/part-0.parquet` dosyasını oku. Satır
   sayısını ve cirosunu (`quantity * unit_price` toplamı, iki ondalık)
   aynı satıra yazdır.
3. Bütün dosyaları (`Path("orders").glob("month=*/*.parquet")`) okuyup
   birleştir; kaç dosya okunduğunu yazdır.
4. Birleşik tablodan `order_time`'ın ayı 6 olanları süz; iki yoldan gelen
   satır sayısının aynı olup olmadığını yazdır.

**Beklenen çıktı:**

```
16392 26273056.88
12
True
```
