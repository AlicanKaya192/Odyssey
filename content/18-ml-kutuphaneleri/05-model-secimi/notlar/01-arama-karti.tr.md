## Araçlar

| Yazım | Ne yapar |
|---|---|
| `GridSearchCV(est, {"adım__ayar": [...]}, cv=5)` | bütün kombinasyonlar |
| `RandomizedSearchCV(est, dağılımlar, n_iter=30, random_state=0)` | rastgele kombinasyonlar |
| `HalvingGridSearchCV` (`from sklearn.experimental import enable_halving_search_cv`) | adayları az veriyle eleyip kalanlara daha çok veri |
| `scoring="f1"`, `scoring="neg_mean_absolute_error"` | skor ölçüsü |
| `n_jobs=-1` | çekirdeklere dağıt |
| `refit=True` (varsayılan) | en iyi ayarla bütün eğitime yeniden eğit |

## Sonuçlar

| Yazım | Ne verir |
|---|---|
| `search.best_params_` | en iyi ayarlar |
| `search.best_score_` | onun çapraz doğrulama ortalaması (iyimser) |
| `search.best_estimator_` | eğitilmiş en iyi model |
| `pd.DataFrame(search.cv_results_)` | bütün adaylar: ortalama, sapma, sıra |
| `search.score(X_test, y_test)` | ayrı test skoru |

## Dağılımlar

| Yazım | Ne için |
|---|---|
| `randint(2, 12)` | tam sayı (derinlik, ağaç sayısı) |
| `loguniform(1e-3, 1e2)` | katlanarak değişen (`C`, `alpha`, öğrenme hızı) |
| `uniform(0, 1)` | 0–1 arası düz |
| `np.logspace(-3, 2, 6)` | ızgarada log ölçekli liste |

## Kurallar

- Arama eğitim verisinde; test en sonda bir kez.
- Farklar sapmadan küçükse en basit ayarı seç.
- Aday sayısı arttıkça `best_score_` daha iyimser; rapora iç içe doğrulama ya
  da ayrı test.
- Önce kaba ve geniş ara (log ölçek), sonra iyi çıkan bölgede daralt.
