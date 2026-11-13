Aynı tabloyu üç biçimde yaz ve boyutlarını karşılaştır.

**Yapman gerekenler:**

1. Başlangıç kodu 200 000 siparişlik türlü `df`'yi hazırlıyor.
2. `df`'yi `orders.csv`, `orders.csv.gz` (ikisi de `index=False,
   lineterminator="\n"`) ve `orders.parquet` olarak yaz. Satır sonunu
   açıkça vermek boyutları her bilgisayarda aynı yapıyor.
3. `orders.csv` ve `orders.parquet` dosyalarını bir döngüyle gez; her
   satıra dosya adını ve MB cinsinden boyutunu (`os.path.getsize`, iki
   ondalık) yazdır.
4. Sonraki satıra gzip'in CSV'yi kaç kat küçülttüğünü (CSV boyutu / gzip'li
   boyut) tam sayıya yuvarlayıp yazdır. gzip'in çıktısı Python'un sıkıştırma
   kütüphanesine göre birkaç KB değişebiliyor; tam sayı her bilgisayarda aynı.
5. Son satıra CSV boyutunun Parquet boyutuna oranını (bir ondalık) yazdır.

**Beklenen çıktı:**

```
orders.csv 11.79
orders.parquet 4.29
4
2.7
```
