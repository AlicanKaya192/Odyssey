## Araçlar

| Yazım | Sorusu |
|---|---|
| `permutation_importance(m, X_test, y_test, n_repeats=10)` | sütun ne kadar işe yarıyor? |
| `... scoring="neg_mean_absolute_error"` | önemi başka bir ölçüyle |
| `r.importances_mean`, `r.importances_std` | ortalama düşüş, sapma |
| `partial_dependence(m, X, ["col"])` | sütun değişince ortalama tahmin |
| `partial_dependence(..., kind="individual")` | her satırın kendi eğrisi (ICE) |
| `PartialDependenceDisplay.from_estimator(m, X, ["a", "b"])` | çizim |
| `... kind="both", subsample=60` | ortalama + örnek satır eğrileri |
| `PartialDependenceDisplay.from_estimator(m, X, [("a", "b")])` | iki sütunun birlikte etkisi |

## Hangi önem?

| Önem | Nereden | Zayıflığı |
|---|---|---|
| `feature_importances_` (ağaç) | eğitimdeki saflık artışı | çok değerli sütunu kayırır |
| LightGBM `gain` | eğitimdeki kayıp azalması | eğitim verisinden |
| `coef_` (doğrusal) | katsayı | ölçeğe bağlı |
| permütasyon (test) | görülmemiş veride skor düşüşü | bağlı sütunlarda bölünür |

## Kurallar

- Permütasyon önemini **test** verisinde hesapla; eğitim verisinde ezberi de
  önem sayar.
- Tam sayı sütunu kısmi bağımlılıktan önce `float`'a çevir.
- Bağlı sütunları (korelasyon, VIF) önce bul; önemlerini birlikte yorumla.
- Model neye baktığını gösterir; neden-sonuç için deney gerekir.
