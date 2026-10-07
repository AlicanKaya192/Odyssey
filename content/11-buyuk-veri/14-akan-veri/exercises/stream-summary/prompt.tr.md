İlk 50 000 ödemenin özetini, olayları bir listede tutmadan çıkar.

**Yapman gerekenler:**

1. `for event in payments(50_000):` döngüsünde şunları güncelle: ödeme
   sayısı, toplam tutar, 1000'den büyük ödemelerin sayısı, en büyük ödeme
   (olayın kendisi).
2. Döngüden sonra sırayla yazdır: ödeme sayısı, toplam (iki ondalık),
   ortalama (iki ondalık), 1000'den büyük ödeme sayısı.
3. Son satıra en büyük ödemenin `event_id`'sini ve tutarını yazdır.

Listeye (`list(...)`, `append`) ihtiyacın yok.

**Beklenen çıktı:**

```
50000
6185404.53
123.71
60
24849 3423.02
```
