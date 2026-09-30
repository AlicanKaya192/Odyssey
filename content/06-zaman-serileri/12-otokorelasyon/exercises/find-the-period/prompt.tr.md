Saatlik elektrik tüketiminin mevsim boyunu bilmediğini düşün. ACF'ye sor.

**Yapman gerekenler:**

1. `values = acf(load, nlags=200)` hesapla.
2. 2–30 gecikmeleri arasında en yüksek ACF'nin gecikmesini ve değerini (iki
   ondalık) aynı satıra yazdır.
3. Aynı aralıkta en **düşük** ACF'nin gecikmesini ve değerini yazdır.
4. 100–200 gecikmeleri arasında en yüksek ACF'nin gecikmesini ve değerini
   yazdır.
5. 24'ün katlarındaki ACF'yi (24, 48, 72, ..., 168) iki ondalığa yuvarlayıp
   liste olarak yazdır.

**Beklenen çıktı:**

```
24 0.88
13 -0.47
168 0.87
[0.88, 0.77, 0.77, 0.76, 0.74, 0.81, 0.87]
```

İlk tepe 24. gecikmede: günlük periyot. Yarım gün sonrası (12–13 saat) ters yönde:
gündüz ve gece. Uzak aralıktaki tepe 168'de: haftalık periyot. Son satırda ACF 24'ün
katlarında önce düşüyor, sonra 168'de yeniden yükseliyor: yedi gün sonrası,
üç gün sonrasına göre bugüne daha çok benziyor.
