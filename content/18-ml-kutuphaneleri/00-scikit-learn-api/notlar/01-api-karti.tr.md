## Sözleşme

| Yazım | Ne |
|---|---|
| `model = Sinif(ayar=...)` | kur; ayarlar hiperparametre |
| `model.fit(X, y)` | öğren; `self` döner, zincirlenebilir |
| `model.predict(X)` | tahmin |
| `model.predict_proba(X)` | sınıf olasılıkları |
| `model.score(X, y)` | doğruluk / R² |
| `tr.fit(X)`, `tr.transform(X)`, `tr.fit_transform(X)` | dönüştürücü |
| `model.get_params()`, `model.set_params(C=1)` | ayarları oku / değiştir |
| `sklearn.base.clone(model)` | aynı ayarla eğitilmemiş kopya |
| `model.coef_`, `scaler.mean_`, `model.classes_` | öğrenilenler (sonda `_`) |

## Veri şekli

| Girdi | Şekil |
|---|---|
| `X` | `(örnek sayısı, özellik sayısı)`, iki boyutlu |
| `y` | `(örnek sayısı,)`, tek boyutlu |
| tek özellik | `x.reshape(-1, 1)` |
| tek örnek | `x.reshape(1, -1)` ya da `[[...]]` |

## Hatalar

| Belirti | Sebep |
|---|---|
| `NotFittedError` | `fit` çağrılmadı |
| `Expected 2D array, got 1D array` | `X` tek boyutlu |
| `X has 3 features, but ... is expecting 4` | eğitimdeki sütunlar ile tahmindeki farklı |
| Her çalıştırmada farklı skor | `random_state` yok |
| Test skoru şüpheli iyi | dönüştürücü bütün veriyle `fit` edildi (sızıntı) |
| "%90 doğruluk" ama model işe yaramıyor | dengesiz veri; taban çizgisiyle karşılaştır |
