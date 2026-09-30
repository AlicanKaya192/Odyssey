`web_traffic.csv` bir sitenin günlük ziyaret sayısı. İçinde birkaç
olağandışı gün var: onların düzleştirmeyi nasıl bozduğunu gör, sonra hareketli
pencereyle bul.

**Yapman gerekenler:**

1. Dosyayı tarih indeksli oku; `visits` sütununu `visits` serisine al.
2. 14 Mart 2024 için 7 günlük hareketli **ortalamayı** (tam sayıya
   yuvarlanmış) ve hareketli **ortancayı** aynı satıra yazdır.
3. Her günü kendi geçmişiyle karşılaştır: `base = visits.shift(1).rolling(28)`
   ve `z = (visits - base.mean()) / base.std()`.
4. 14 Mart 2024'ün z değerini bir ondalığa yuvarlayıp yazdır.
5. `z` mutlak değeri 3'ten büyük olan günleri `"%m-%d"` biçiminde liste
   olarak yazdır.
6. O günlerin z değerlerini bir ondalığa yuvarlayıp liste olarak yazdır.

**Beklenen çıktı:**

```
4587 4090.0
11.2
['03-14', '06-20', '10-08']
[11.2, 8.9, -6.5]
```

Tek bir sıçrama günü ortalamayı ortancanın 500 ziyaret üstüne çekti; ortanca
yerinde kaldı. Z skoru üç günü yakaladı: ikisi yukarı yönlü (kampanya), biri aşağı
yönlü (kesinti). `shift(1)` olmadan olağandışı gün kendi tabanına girer ve
sapması küçük görünür.
