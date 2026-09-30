Yıllık yolcu toplamını üç modelle tahmin et: trendsiz, toplamsal trendli ve
çarpımsal trendli.

Başlangıç kodunda `annual` (2013–2024 yıllık toplamlar), `train` (2013–2022)
ve `test` (2023–2024) hazır.

**Yapman gerekenler:**

1. Üç model kur (hepsi `ExponentialSmoothing(train, ...).fit()`):
   - `"flat"`: trend yok
   - `"additive"`: `trend="add"`
   - `"multiplicative"`: `trend="mul"`
2. Her biri için iki yıllık tahmini (`forecast(2)`) tam sayıya yuvarlanmış
   liste olarak ve ortalama mutlak hatayı bir ondalıkla `ad [tahminler] MAE`
   biçiminde alt alta yazdır.
3. Gerçek değerleri liste olarak yazdır.
4. Eğitim verisinde yıllık ortalama büyüme oranını hesapla
   (`train.pct_change().mean() * 100`) ve bir ondalığa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
flat [3816, 3816] 621.5
additive [4071, 4326] 239.3
multiplicative [4233, 4690] 23.5
[4195, 4680]
10.7
```

Trendsiz model son düzeyde kalıyor. Toplamsal trend her yıl aynı miktarı
ekliyor ve ikinci yılda iyice geride kalıyor. Çarpımsal trend her yıl aynı
**oranla** büyütüyor; seri yılda %10 dolayında büyüdüğü için gerçeğin yanından
gidiyor.
