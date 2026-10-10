## Regresyon

| Sınıf | Ne zaman | Önemli ayar |
|---|---|---|
| `LinearRegression()` | az sütun, yorum | — |
| `Ridge(alpha=1.0)`, `RidgeCV(alphas=...)` | çok/ilişkili sütun | büyük `alpha` güçlü ceza |
| `Lasso(alpha=...)`, `LassoCV(cv=5)` | bazı sütunlar sıfırlansın | büyük `alpha` daha çok sıfır |
| `ElasticNet(alpha, l1_ratio)`, `ElasticNetCV` | Lasso + Ridge karışımı | `l1_ratio` 0–1 |
| `HuberRegressor()` | aykırı değerli hedef | `epsilon` |
| `QuantileRegressor(quantile=0.9)` | ortalama değil yüzdelik | `quantile`, `alpha` |
| `PoissonRegressor()` | sayım hedefi (0, 1, 2, ...) | `alpha` |
| `SGDRegressor()` | çok büyük veri, `partial_fit` | `alpha`, `max_iter` |

## Sınıflandırma

| Sınıf | Ne zaman | Önemli ayar |
|---|---|---|
| `LogisticRegression()` | olasılık veren temel model | küçük `C` güçlü ceza |
| `LogisticRegression(l1_ratio=1, solver="saga")` | L1, seyrek katsayı | `C` |
| `LogisticRegression(C=np.inf)` | cezasız | — |
| `LogisticRegressionCV(Cs=10, cv=5)` | `C`'yi kendisi seçer | `Cs` |
| `SGDClassifier(loss="log_loss")` | çok büyük veri | `alpha` |
| `RidgeClassifier()` | hızlı, olasılık gerekmiyorsa | `alpha` |

## Okunacak nitelikler

| Nitelik | Ne |
|---|---|
| `coef_`, `intercept_` | katsayılar ve sabit |
| `alpha_`, `C_` | `...CV` sınıflarının seçtiği ceza |
| `n_iter_` | çözücünün attığı adım; `max_iter`'a eşitse yakınsamamış |
| `classes_` | `coef_` satırlarının sınıf sırası |

## Kurallar

- Cezalı modellerden önce `StandardScaler`: ceza bütün katsayılara aynı
  ölçüde uygulanır, ölçeksiz sütun haksız cezalanır.
- `alpha` (Ridge/Lasso) büyüdükçe, `C` (lojistik) küçüldükçe ceza artar.
- `penalty=` eskidi: L1 için `l1_ratio=1`, cezasız için `C=np.inf`.
