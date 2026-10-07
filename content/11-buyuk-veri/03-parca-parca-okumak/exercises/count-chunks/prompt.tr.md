100 000 siparişlik dosyayı 30 000 satırlık parçalarla oku ve parçaları
say.

**Yapman gerekenler:**

1. `write_orders_csv("orders.csv", 100_000)` ile dosyayı yaz.
2. `pd.read_csv(..., chunksize=30_000)` okuyucusunu bir döngüyle gez; her
   parçanın satır sayısını bir listeye ekle.
3. Listeyi yazdır.
4. Toplam satır sayısını ve parça sayısını aynı satıra yazdır.

**Beklenen çıktı:**

```
[30000, 30000, 30000, 10000]
100000 4
```

Son parça kısa kaldı: dosya parça büyüklüğüne tam bölünmüyor.
