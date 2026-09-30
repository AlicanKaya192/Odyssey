Holt–Winters'ı Bölüm 15'in düzeneğinden geçir: 13 başlangıç, 28 günlük
ufuk, mevsimsel naife karşı.

Başlangıç kodunda `snaive(train, h)`, `cuts` (13 kesim günü) ve
`backtest(forecast)` hazır: `backtest`, verilen tahmin fonksiyonunun 13
deneydeki MAE'lerini numpy dizisi olarak döndürüyor.

**Yapman gerekenler:**

1. `hw(train, h)` fonksiyonunu yaz: trendsiz, toplamsal mevsimli
   (`seasonal_periods=7`) modeli `train` üzerinde kurup `h` günlük tahmini
   numpy dizisi olarak döndürsün (`.forecast(h).to_numpy()`).
2. `hw_trend(train, h)` fonksiyonunu yaz: aynısı, `trend="add"` ile.
3. Üç yöntemi `backtest`'ten geçir. Her biri için ortalama MAE'yi ve en kötü
   deneyi iki ondalıkla `ad ortalama en_kötü` biçiminde alt alta yazdır
   (adlar: `snaive`, `hw`, `hw trend`).
4. `hw`'nin mevsimsel naife göre deney deney farkını hesapla
   (`snaive − hw`): farkın ortalamasını, standart sapmasını (`ddof=1`, iki
   ondalık) ve `hw`'nin kazandığı deney sayısını aynı satıra yazdır.
5. `hw`'nin becerisini (`1 - ortalama_hw / ortalama_snaive`) iki ondalıkla
   yazdır.

**Beklenen çıktı:**

```
snaive 17.95 41.29
hw 15.91 38.57
hw trend 16.81 51.26
2.04 1.85 12
0.11
```

Trendsiz model 13 deneyin 12'sinde önde: fark küçük ama **tutarlı**. Trend
eklemek ortalamayı iyileştirmiyor ve en kötü deneyi belirgin biçimde
kötüleştiriyor: trend, yıl sonu yükselişini Ocak'a taşıyor. Bu seride doğru
seçim az bileşenli model; kazancı %11.
