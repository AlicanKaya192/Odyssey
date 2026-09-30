Günlük satışa kurulan modelin katsayı tablosunu oku ve hangi terimlerin
gerçekten iş gördüğüne karar ver.

Başlangıç kodunda `train` hazır.

**Yapman gerekenler:**

1. `(1, 1, 1)(0, 1, 1, 7)` modelini kur.
2. `sigma2` dışındaki her katsayı için adını, değerini (iki ondalık) ve
   p-değerini (üç ondalık) `ad katsayı p` biçiminde alt alta yazdır.
3. p-değeri 0.05'in üstünde olan katsayıların adlarını liste olarak yazdır.
4. En küçük katsayılı terimi (AR) çıkarıp `(0, 1, 1)(0, 1, 1, 7)` modelini
   kur. İki modelin AIC'sini bir ondalıkla aynı satıra yazdır (önce büyük
   model).
5. İki modelin kalıntı standart sapmasını
   (`fit.resid.iloc[8:].std()`) iki ondalıkla aynı satıra yazdır.

**Beklenen çıktı:**

```
ar.L1 0.11 0.001
ma.L1 -0.85 0.0
ma.S.L7 -0.86 0.0
[]
8258.7 8265.8
13.16 13.22
```

Üç katsayının da p-değeri küçük: tablo hiçbirini "gereksiz" göstermiyor ve
liste boş. AR katsayısı küçük (0.11) ama gerçek; çıkarınca AIC 7 puan
kötüleşiyor. Yine de kalıntının standart sapması neredeyse aynı ve dersteki
kayan başlangıç tablosunda iki model aynı hatayı veriyordu. **İstatistiksel
olarak anlamlı olmak, tahmini belirgin biçimde iyileştirmek demek değil.**
Bin gözlemde çok küçük etkiler de "anlamlı" çıkar; son sözü örnek dışı hata
söyler.
