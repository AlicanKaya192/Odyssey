"Son `k` haftanın ortalaması" yönteminde `k` kaç olmalı? Ayarı doğrulama
deneylerinde seç, sonucu test deneylerinde ölç.

Başlangıç kodunda `weeks_mean(train, h, k)`, `cuts` (13 kesim günü) ve
`score(k, some_cuts)` (verilen kesimlerde ortalama MAE) hazır.

**Yapman gerekenler:**

1. Kesimleri ikiye ayır: ilk 10'u doğrulama, son 3'ü test. Yani
   `validation = cuts[:10]`, `test = cuts[10:]`.
2. `k = 1..8` için doğrulama MAE'sini hesapla ve iki ondalıkla liste olarak
   yazdır.
3. Doğrulamada en iyi `k`'yi bul; `k`'yi, doğrulama MAE'sini ve **aynı
   `k`'nin** test MAE'sini iki ondalıkla aynı satıra yazdır.
4. Hile yapsaydın: testte en iyi görünen `k`'yi ve test MAE'sini aynı satıra
   yazdır.
5. İki test MAE'si arasındaki farkı iki ondalıkla yazdır.

**Beklenen çıktı:**

```
[16.61, 15.84, 15.16, 15.2, 15.4, 15.82, 15.86, 16.17]
3 15.16 22.97
1 22.42
0.56
```

Doğrulamaya göre `k = 3` seçiliyor; dürüst sonuç onun testteki hatası. Testte
en iyi görünen `k`'yi seçip onu raporlamak, hatayı olduğundan küçük
gösterirdi: o kararı test verisine bakarak verirdin ve gerçek kullanımda o
avantaj olmazdı. Testin doğrulamadan belirgin biçimde zor çıkması da bir
bulgu: son deneyler yılın en oynak çeyreğine denk geliyor.
