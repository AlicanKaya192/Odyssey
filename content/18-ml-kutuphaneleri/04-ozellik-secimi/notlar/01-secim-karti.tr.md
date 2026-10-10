## Yöntemler

| Tür | Yazım | Ne zaman |
|---|---|---|
| Sabit sütun | `VarianceThreshold(threshold=0)` | her zaman önce |
| Filtre | `SelectKBest(f_classif, k=10)` | hızlı ilk eleme (sınıflandırma) |
| Filtre | `SelectKBest(f_regression, k=10)` | regresyon |
| Filtre | `SelectKBest(mutual_info_classif, k=10)` | doğrusal olmayan ilişki |
| Filtre | `SelectPercentile(f_classif, percentile=20)` | yüzde ile |
| Gömülü | `SelectFromModel(LogisticRegression(penalty="l1", solver="liblinear"))` | seyrek doğrusal |
| Gömülü | `SelectFromModel(RandomForestClassifier(), max_features=10, threshold=-np.inf)` | ağaç önemi |
| Sarmalayıcı | `RFECV(model, cv=5)` | birlikte değerlendirme, pahalı |
| Sarmalayıcı | `SequentialFeatureSelector(model, n_features_to_select=5)` | ileri / geri ekleme |

## Okumak

| Yazım | Ne verir |
|---|---|
| `sel.get_support()` | seçilenler (True/False) |
| `sel.get_support(indices=True)` | seçilenlerin sırası |
| `sel.get_feature_names_out(names)` | seçilen adlar |
| `kb.scores_`, `kb.pvalues_` | filtre puanları |
| `rfe.ranking_`, `rfe.n_features_` | eleme sırası, seçilen sayı |

## Kurallar

- Seçim pipeline'ın içinde; yoksa çapraz doğrulama sahte başarı gösterir.
- `k` bir hiperparametre: `GridSearchCV` ile `selectkbest__k`.
- Kopya sütunlar: filtre ikisini de seçer, L1 birini, orman önemi bölüştürür.
- Sütun atmak bilgiyi atmaktır; skor düşmüyorsa ve model sadeleşiyorsa at.
