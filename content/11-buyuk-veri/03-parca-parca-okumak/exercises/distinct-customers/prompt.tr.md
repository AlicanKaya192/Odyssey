Farklı müşteri sayısını parçalarla doğru bul ve yanlış yolun ne kadar
şaştığını göster.

**Yapman gerekenler:**

1. 200 000 siparişlik dosyayı yaz.
2. Yalnızca `customer_id` sütununu (`usecols`) 50 000 satırlık parçalarla
   oku.
3. Aynı döngüde iki şey yap: müşterileri bir kümede (`set`) topla ve her
   parçanın `nunique()` sonucunu bir sayaca ekle.
4. Kümedeki müşteri sayısını, sayacı ve sayacın küme büyüklüğüne oranını
   (iki ondalık) ayrı satırlara yazdır.

**Beklenen çıktı:**

```
49031
126247
2.57
```

Yanlış yol aynı müşteriyi farklı parçalarda tekrar tekrar saydı.
