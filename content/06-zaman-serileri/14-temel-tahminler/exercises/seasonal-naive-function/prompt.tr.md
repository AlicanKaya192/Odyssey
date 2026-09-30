Mevsimsel naifi, her sıklıkta ve her ufukta çalışan bir fonksiyon olarak
yaz.

**Yapman gerekenler:**

1. `seasonal_naive(train, h, m)` fonksiyonunu yaz:
   - Son `m` değeri al (`train.iloc[-m:].to_numpy()`).
   - `h` adım için `last[i % m]` değerlerini üret.
   - İndeksi, eğitimin son tarihinden **sonraki** `h` tarih olsun:
     `pd.date_range(train.index[-1], periods=h + 1, freq=train.index.freq)[1:]`.
   - Bir seri döndürsün.
2. Günlük satışta (`s`, 3 Aralık 2024'e kadar) `m=7`, `h=10` ile çağır. Dönen
   serinin değerlerini liste olarak yazdır.
3. Aynı tahminin ilk ve son tarihini aynı satıra yazdır.
4. Aylık yolcuda (`p`, 2023 sonuna kadar) `m=12`, `h=12` ile çağır. Değerleri
   liste olarak yazdır.
5. Yolcu tahminini 2024'ün gerçek değerleriyle karşılaştır: ortalama mutlak
   hatayı ve yanlılığı (hataların ortalaması) iki ondalıkla aynı satıra
   yazdır.

**Beklenen çıktı:**

```
[297, 297, 336, 432, 393, 269, 290, 297, 297, 336]
2024-12-04 2024-12-13
[293, 279, 321, 323, 344, 395, 425, 448, 369, 350, 303, 345]
40.42 40.42
```

Ufuk 10 olduğunda son üç değer haftanın ilk üç gününü yeniden alıyor: `i % 7`
ufkun mevsimin katı olmasını gerektirmiyor. Yolcu tahmininde MAE ile yanlılık
aynı sayı: on iki ayın hepsinde tahmin düşük kalmış, çünkü seri büyüyor ve
kopya bir yıl geriden geliyor.
