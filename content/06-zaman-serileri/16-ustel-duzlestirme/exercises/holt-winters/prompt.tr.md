Günlük satışa mevsimli bir model kur, bileşenlerini oku ve tahminini
grafikte gör.

Başlangıç kodunda `train` (5 Kasım 2024'e kadar) ve `test` (sonraki 28 gün)
hazır.

**Yapman gerekenler:**

1. Trendsiz, toplamsal mevsimli modeli kur:
   `ExponentialSmoothing(train, seasonal="add", seasonal_periods=7).fit()`.
2. `α` ve `γ` katsayılarını (`smoothing_level`, `smoothing_seasonal`) iki
   ondalıkla aynı satıra yazdır.
3. Son düzeyi (`fit.level.iloc[-1]`) bir ondalıkla yazdır.
4. Son 7 mevsim payını (`fit.season.iloc[-7:]`) bir ondalıkla liste olarak
   yazdır. (Sıra: çarşambadan salıya.)
5. 28 günlük tahmini al ve ilk 7 gününü bir ondalıkla liste olarak yazdır.
6. Tahminin ortalama mutlak hatasını ve yanlılığını iki ondalıkla aynı satıra
   yazdır.
7. Grafik çiz: eğitimin son 28 günü ve test (gri), üstüne tahmin.
   `chart.png` olarak kaydet.

**Beklenen çıktı:**

```
0.18 0.13
314.0
[-23.2, -11.1, 35.3, 96.0, 48.3, -39.3, -41.3]
[290.8, 302.9, 349.3, 410.0, 362.3, 274.7, 273.8]
11.73 7.68
```

Tahminin ilk haftası, son düzey ile o günün mevsim payının toplamı:
dördüncü değer (cumartesi) 314.0 + 96.0. Yanlılık artı: tahmin ortalamada
biraz düşük, çünkü model trend taşımıyor ve Kasım sonunda satışlar yükseliyor.
Grafikte tahminin her hafta aynı yedi sayıyı tekrarladığını göreceksin.
