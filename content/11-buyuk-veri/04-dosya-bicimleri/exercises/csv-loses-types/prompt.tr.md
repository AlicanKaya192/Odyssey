Türleri ayarlanmış bir tabloyu CSV'ye ve Parquet'ye yaz, geri oku ve
hangisinin türleri koruduğuna bak.

**Yapman gerekenler:**

1. Başlangıç kodu 20 000 siparişlik `df`'yi hazırlıyor (tarih ve
   kategoriler ayarlı).
2. `df`'yi `orders.csv` (`index=False`) ve `orders.parquet` olarak yaz.
3. İkisini de geri oku.
4. Her biri için bir satıra biçimin adını (`csv` / `parquet`) ve
   `order_time` ile `city` sütunlarının türünü yazdır.

**Beklenen çıktı:**

```
csv str str
parquet datetime64[us] category
```
