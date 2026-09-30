Tahmini teslim et: Ocak 2025'in ilk 28 günü, nokta tahmini ve sınanmış bir
%80 aralıkla.

Başlangıç kodunda `features`, `log_model` ve `cuts` hazır.

**Yapman gerekenler:**

1. 13 deneyin **oransal** hatalarını topla: her kesimde
   `gerçek / tahmin - 1` (28 değer); 13 × 28'lik bir numpy dizisi.
2. Oransal hatanın ortalamasını ve %10 ile %90 yüzdeliklerini üç ondalıkla aynı
   satıra yazdır.
3. Aralığı sına: her deney için yüzdelikleri **öbür 12 deneyin** hatalarından
   al (`np.delete(errors, i, axis=0)`) ve o deneyin hatalarının kaçının
   aralıkta kaldığını ölç. 13 kapsamanın ortalamasını üç ondalıkla yazdır.
4. Modeli bütün seriyle eğitip 1–28 Ocak 2025'i tahmin et
   (`pd.date_range("2025-01-01", periods=28, freq="D")`). 28 günün toplamını
   tam sayı olarak yazdır.
5. İlk gün için tahmini ve %80 aralığın alt ve üst ucunu
   (`tahmin * (1 + yüzdelik)`) tam sayı olarak aynı satıra yazdır.
6. Grafik çiz: 2024'ün son 42 günü, tahmin ve `fill_between` ile aralık.
   `chart.png` olarak kaydet.

**Beklenen çıktı:**

```
0.003 -0.309 0.258
0.797
7541
255 177 321
```

Model yansız (ortalama hata sıfıra çok yakın) ama belirsizlik büyük: %80
aralık tahminin %31 altından %26 üstüne. Sınandığında söylediğini tutuyor
(0.80). Aralığın aşağı doğru daha uzun olması yağmurdan: yağmurlu bir gün
tahminin çok altında kalıyor. Teslim ettiğin şey tek bir sayı değil: bir
tahmin, dürüst bir aralık ve hatanın kaynağı.
