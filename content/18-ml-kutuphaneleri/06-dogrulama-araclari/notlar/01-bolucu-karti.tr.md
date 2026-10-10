## Bölücüler

| Yazım | Ne zaman |
|---|---|
| `KFold(5, shuffle=True, random_state=0)` | regresyon, satırlar bağımsız |
| `StratifiedKFold(5, shuffle=True, random_state=0)` | sınıflandırma (sınıf oranı korunur) |
| `GroupKFold(5)` + `groups=` | aynı kişi/cihaz birden çok satırda |
| `StratifiedGroupKFold(5)` | grup + sınıf oranı |
| `TimeSeriesSplit(n_splits=5, test_size=, gap=)` | zaman sırası |
| `RepeatedStratifiedKFold(n_splits=5, n_repeats=10)` | küçük veride daha kararlı ortalama |
| `ShuffleSplit(n_splits=10, test_size=0.2)` | rastgele, birbirine karışabilen ayrımlar |
| `LeaveOneOut()` | çok küçük veri; her satır bir kez test |

## Araçlar

| Yazım | Ne verir |
|---|---|
| `cross_val_score(m, X, y, cv=cv, scoring="f1")` | tek ölçünün kat skorları |
| `cross_validate(m, X, y, cv=cv, scoring=[...], return_train_score=True)` | sözlük: `test_*`, `train_*`, süreler |
| `cross_val_predict(m, X, y, cv=cv)` | her satır için, onu görmemiş modelin tahmini |
| `learning_curve(m, X, y, train_sizes=[...])` | veri miktarına göre eğitim/test skoru |
| `validation_curve(m, X, y, param_name=, param_range=)` | tek ayara göre eğitim/test skoru |

## Kurallar

- `cv=5` sayısı: sınıflandırıcıda `StratifiedKFold`, regresyonda `KFold`;
  ikisi de **karıştırmaz**.
- Bölücü nesnesini bir kez kur, her yerde aynısını ver: modeller aynı
  katlarda karşılaştırılmış olur.
- Doğrulama, modelin yarın karşılaşacağı durumu taklit etmeli: yeni
  müşteri → grup, gelecek → zaman.
- `groups=` yalnızca grup bölücüleri kullanır; düz `KFold` onu yok sayar ve
  uyarı verir.
