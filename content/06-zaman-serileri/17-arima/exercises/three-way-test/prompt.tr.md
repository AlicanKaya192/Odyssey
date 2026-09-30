Mevsimsel naif, Holt–Winters ve ARIMA'yı Bölüm 15'in düzeneğinde yan yana
sına: 13 başlangıç, 28 günlük ufuk.

Başlangıç kodunda `snaive`, `hw` ve `backtest(forecast)` hazır.
(Bu alıştırma 13 kez ARIMA kurduğu için birkaç saniye sürer.)

**Yapman gerekenler:**

1. `arima(train, h)` fonksiyonunu yaz: `(0, 1, 1)(0, 1, 1, 7)` modelini
   `train` üzerinde kurup `h` günlük tahmini numpy dizisi olarak döndürsün.
2. Üç yöntemi `backtest`'ten geçir. Her biri için ortalama MAE'yi ve en kötü
   deneyi iki ondalıkla `ad ortalama en_kötü` biçiminde alt alta yazdır
   (adlar: `snaive`, `hw`, `arima`).
3. ARIMA'nın mevsimsel naife karşı: `snaive − arima` farkının ortalamasını
   (iki ondalık) ve ARIMA'nın kazandığı deney sayısını aynı satıra yazdır.
4. ARIMA'nın Holt–Winters'a karşı: `hw − arima` farkının ortalamasını,
   standart sapmasını (`ddof=1`, iki ondalık) ve ARIMA'nın kazandığı deney
   sayısını aynı satıra yazdır.

**Beklenen çıktı:**

```
snaive 17.95 41.29
hw 15.91 38.57
arima 15.94 52.2
2.02 11
-0.02 5.13 9
```

ARIMA mevsimsel naifi 13 deneyin 11'inde geçiyor. Holt–Winters'a karşı ise
9 deneyde önde olmasına rağmen ortalama fark sıfır: kazandığı deneylerde az,
kaybettiklerinde çok fark var. Berabere. İki farklı
model aynı yere varıyor; serinin geçmişinden çıkarılabilecek bilgi bu kadar.
En kötü deneyde ARIMA belirgin biçimde geride: aynı ortalamada, daha büyük
risk.
