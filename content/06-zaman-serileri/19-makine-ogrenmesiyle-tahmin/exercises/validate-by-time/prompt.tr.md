Aynı modeli iki farklı çapraz doğrulamayla ölç: karıştırılmış `KFold` ve
`TimeSeriesSplit`.

**Yapman gerekenler:**

1. Model: `HistGradientBoostingRegressor(random_state=0)`.
2. `cross_val_score` ile MAE hesapla (`scoring="neg_mean_absolute_error"`;
   sonucu eksi ile çarp). İki bölme:
   - `KFold(5, shuffle=True, random_state=0)`
   - `TimeSeriesSplit(5)`
3. Her biri için beş parçanın hatasını bir ondalıkla liste olarak ve
   ortalamasını iki ondalıkla, `[liste] ortalama` biçiminde alt alta yazdır
   (önce `KFold`).
4. `TimeSeriesSplit(5)`'in ilk ve son parçasında eğitim ve test satır
   sayılarını `eğitim test` biçiminde iki satırda yazdır.

**Beklenen çıktı:**

```
[11.8, 12.0, 12.0, 12.4, 11.3] 11.88
[24.9, 11.8, 15.0, 14.5, 12.7] 15.78
178 178
890 178
```

Karıştırılmış doğrulama beş parçada da benzer ve küçük bir hata veriyor: model
her test gününün komşularını eğitimde gördü. Zamana göre doğrulama daha büyük
ve daha oynak: ilk parçada eğitim çok kısa, hata büyük. Gerçekte yapacağın iş
ikincisi; dürüst sayı o.
