Hisse fiyatına dört ARIMA adayı kur ve yalın rastgele yürüyüşün ötesine
geçmenin bir şey kazandırıp kazandırmadığına bak.

Başlangıç kodunda `k` (fiyat, numpy dizisi olarak) hazır.

**Yapman gerekenler:**

1. Dört aday: `(0, 1, 0)`, `(1, 1, 0)`, `(0, 1, 1)`, `(1, 1, 1)`. Her biri
   için AIC'yi bir ondalıkla `mertebe AIC` biçiminde alt alta yazdır.
2. En küçük ile en büyük AIC arasındaki farkı bir ondalıkla yazdır.
3. `(1, 1, 1)` modelinin AR ve MA katsayılarını (`ar.L1`, `ma.L1`) iki
   ondalıkla aynı satıra yazdır.
4. `(0, 1, 0)` modelinin 3 adımlık tahminini ve serinin son değerini iki
   ondalıkla aynı satıra yazdır (önce tahmin listesi).

**Beklenen çıktı:**

```
(0, 1, 0) 3503.1
(1, 1, 0) 3503.8
(0, 1, 1) 3503.9
(1, 1, 1) 3503.1
0.8
0.63 -0.57
[166.44, 166.44, 166.44] 166.44
```

Dört modelin AIC'si bir puanın içinde: fazladan terimler hiçbir şey
kazandırmıyor. `(1, 1, 1)`'in iki katsayısı yakın büyüklükte ve ters işaretli:
birbirini götürüyor. En yalın modelin tahmini son değerin kendisi: rastgele
yürüyüş için en iyi tahmin naif, ve ARIMA bunu doğruluyor.
