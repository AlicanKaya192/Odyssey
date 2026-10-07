Aynı tabloyu üç biçimde yaz ve boyutlarını karşılaştır.

**Yapman gerekenler:**

1. Başlangıç kodu 200 000 siparişlik türlü `df`'yi hazırlıyor.
2. `df`'yi `orders.csv`, `orders.csv.gz` (ikisi de `index=False`) ve
   `orders.parquet` olarak yaz.
3. Üç dosyayı bir döngüyle gez; her satıra dosya adını ve MB cinsinden
   boyutunu (`os.path.getsize`, iki ondalık) yazdır.
4. Son satıra CSV boyutunun Parquet boyutuna oranını (bir ondalık) yazdır.

**Beklenen çıktı:**

```
orders.csv 11.99
orders.csv.gz 3.08
orders.parquet 4.29
2.8
```
