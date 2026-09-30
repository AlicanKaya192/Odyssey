`two_walks.csv` içinde birbirinden **bağımsız** üretilmiş iki rastgele
yürüyüş var (`date`, `a`, `b`; 500 iş günü). Aralarında hiçbir bağ yok. Bunu
veriden görmeye çalış.

**Yapman gerekenler:**

1. Dosyayı tarih indeksli `w` tablosu olarak oku.
2. `a` ile `b`'nin **düzeylerinin** korelasyonunu üç ondalığa yuvarlayıp
   yazdır.
3. **Değişimlerinin** (`w.diff()`) korelasyonunu üç ondalığa yuvarlayıp
   yazdır.
4. Düzeylerin korelasyonu dönemden döneme ne kadar oynuyor? Seriyi 100'er
   günlük beş parçaya böl (`w.iloc[0:100]`, `w.iloc[100:200]`, ...) ve her
   parçadaki düzey korelasyonunu iki ondalığa yuvarlayıp liste olarak yazdır.
5. Aynı beş parça için değişimlerin korelasyonunu iki ondalıkla liste olarak
   yazdır.

**Beklenen çıktı:**

```
0.907
0.001
[-0.3, 0.54, 0.79, 0.34, -0.45]
[-0.15, -0.01, 0.01, 0.1, 0.05]
```

Düzeylerin korelasyonu bütün seride 0.9 dolayında; ama parça parça bakınca
büyük artılarla büyük eksiler arasında savruluyor. Gerçek bir ilişki böyle
davranmaz. Değişimlerin korelasyonu her parçada sıfırın yakınında: iki seri
arasında bağ yok.
