Ödeme türüne göre bölünmüş dosyaları oku; ödeme sütununu klasör
adlarından geri kur.

**Yapman gerekenler:**

1. Başlangıç kodu 100 000 siparişi `orders/payment=<tür>/part-0.parquet`
   düzeninde yazıyor; dosyaların içinde `payment` sütunu yok.
2. `Path("orders").glob("payment=*/*.parquet")` ile dosyaları sıralı gez.
3. Her dosyayı oku; klasör adından ödeme türünü al
   (`f.parent.name.split("=")[1]`) ve tabloya `payment` sütunu olarak
   ekle.
4. Parçaları birleştir; ödeme türü başına satır sayısını, adlara göre sıralı
   olarak her satıra yazdır.
5. Son satıra toplam satır sayısını yazdır.

**Beklenen çıktı:**

```
card 72243
cash 7872
transfer 19885
100000
```
