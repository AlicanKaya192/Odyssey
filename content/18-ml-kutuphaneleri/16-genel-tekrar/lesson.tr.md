# Genel Tekrar

ML Kütüphaneleri modülünün sonuna geldin. scikit-learn'ün ortak
arayüzünden ön işlemeye ve pipeline'a, model seçiminden metriklere,
doğrusal modellerden boosting kütüphanelerine, statsmodels'in çıkarım
araçlarından modeli kaydetmeye ve açıklamaya kadar bir modelin baştan sona
yolunu gördün. Bu bölüm yolu bir kez daha yürüyor; sonunda hepsinin bir
arada çalıştığı bir örnek var.

<figure class="fig">
  <div class="flow">
    <span class="node">Hazırlık<br><small>00–04</small></span><span class="arrow">→</span>
    <span class="node">Değerlendirme<br><small>05–07</small></span><span class="arrow">→</span>
    <span class="node">Modeller<br><small>08–10, 14</small></span><span class="arrow">→</span>
    <span class="node">İstatistik<br><small>12–13</small></span><span class="arrow">→</span>
    <span class="node acc">Kayıt ve açıklama<br><small>11, 15</small></span>
  </div>
  <figcaption>Modülün yolu: veriyi hazırla, dürüst ölç, modeli seç, etkiyi sına, kaydet ve açıkla.</figcaption>
</figure>

## 1. Hazırlık (Bölüm 0–4)

| İş | Araç |
|---|---|
| Ortak arayüz | kur → `fit` → `predict` / `transform`; öğrenilen `coef_`, `mean_`; `clone` |
| Ölçek | `StandardScaler`, aykırı değerde `RobustScaler`; ağaçta gereksiz |
| Eksik ve kategori | `SimpleImputer(add_indicator=True)`, `OneHotEncoder(handle_unknown="ignore")`, `OrdinalEncoder` |
| Sütun grupları | `ColumnTransformer`, `remainder`, `make_column_selector`, `set_output(transform="pandas")` |
| Akış | `make_pipeline`, `adım__ayar`, kendi dönüştürücün, `FunctionTransformer` |
| Sütun seçmek | `VarianceThreshold`, `SelectKBest`, `SelectFromModel`, `RFECV` |

Veriden öğrenen her adım pipeline'ın **içinde**; dışarıda kalırsa çapraz
doğrulama sahte başarı gösterir. Varsayılan `remainder="drop"` sütunları
sessizce atar.

## 2. Değerlendirme (Bölüm 5–7)

| İş | Araç |
|---|---|
| Arama | `GridSearchCV`, `RandomizedSearchCV(loguniform, randint)`, `cv_results_` |
| Dürüst skor | iç içe doğrulama, ayrı test; `best_score_` iyimser |
| Bölücü | `StratifiedKFold`, `KFold(shuffle=True)`, `GroupKFold`, `TimeSeriesSplit` |
| Birden çok ölçü | `cross_validate(scoring=[...], return_train_score=True)` |
| Eğriler | `learning_curve`, `validation_curve` |
| Ölçü | `scoring="neg_..."`, `average="macro"`, AUC olasılıkla, `make_scorer` |
| Eşik | `TunedThresholdClassifierCV`, `FixedThresholdClassifier` |

Sıralı veride karıştır, aynı kişi iki tarafta olmasın, zamanda geçmişle
eğit. Eşiği test verisine bakarak seçme.

## 3. Modeller (Bölüm 8–10 ve 14)

| İş | Araç |
|---|---|
| Doğrusal | `RidgeCV`, `LassoCV`, `LogisticRegression(l1_ratio=1, solver="saga")`, `C=np.inf` |
| Eğri ilişki | `PolynomialFeatures` + cezalı model |
| Ağaç | `ccp_alpha`, `min_samples_leaf`, `NaN` kabul eder |
| Topluluk | `RandomForest`, `ExtraTrees`, `VotingClassifier`, `StackingClassifier` |
| Kümeleme | `KMeans`, `HDBSCAN`; ARI, siluet |
| Boyut | `PCA(n_components=0.95)`, `TSNE` yalnızca çizim |
| Boosting | `HistGradientBoostingClassifier`, `LGBMClassifier`; `eval_X`, `eval_y`, `early_stopping` |

`ConvergenceWarning` çoğu zaman ölçek eksikliğidir; `feature_importances_`
çok değerli sütunu kayırır; birleştirmek ancak farklı hatalar yapan
modellerde kazandırır.

## 4. İstatistik (Bölüm 12–13)

| İş | Araç |
|---|---|
| OLS | `sm.OLS(y, sm.add_constant(X))`, `summary().tables[1]`, `conf_int` |
| Tanı | `variance_inflation_factor`, `het_breuschpagan`, `cov_type="HC3"` |
| Tahmin aralığı | `get_prediction(...).summary_frame()`: `mean_ci`, `obs_ci` |
| Formül | `smf.ols("y ~ a + C(c)")`, `Treatment('...')`, `a * C(c)`, `I(a ** 2)` |
| GLM | `smf.logit` (olasılık oranı), `Poisson` + `offset`, negatif binom |

Sabit terimi unutma; büyük p "etki yok" değil; tek ev için `obs_ci`.

## 5. Kayıt ve açıklama (Bölüm 11 ve 15)

| İş | Araç |
|---|---|
| Kaydetmek | `joblib.dump({...}, compress=3)`; sürüm, sütunlar, eşik birlikte |
| Güvenli yüklemek | `InconsistentVersionWarning`'ı hataya çevir; güvenmediğin dosyayı açma |
| Önem | `permutation_importance(model, X_test, y_test)` |
| Etki biçimi | `partial_dependence`, `PartialDependenceDisplay(kind="both")` |

## Hepsi birlikte

```python
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import (GridSearchCV, StratifiedKFold,
                                     cross_val_score, train_test_split)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

rng = np.random.default_rng(16)
df = pd.DataFrame({
    "tenure": rng.integers(1, 72, 1500).astype(float),
    "monthly": rng.uniform(20, 120, 1500).round(2),
    "plan": rng.choice(["basic", "plus", "pro"], 1500),
    "support": rng.poisson(1.5, 1500).astype(float),
})
plan_effect = df["plan"].map({"basic": 0.6, "plus": 0.0, "pro": -0.6})
logit = (-0.04 * df["tenure"] + 0.02 * df["monthly"] + 0.5 * df["support"]
         + plan_effect - 0.5)
df["churn"] = (rng.random(1500) < 1 / (1 + np.exp(-logit))).astype(int)
df.loc[rng.random(1500) < 0.08, "monthly"] = np.nan
print(round(df["churn"].mean(), 3), int(df["monthly"].isna().sum()))

X, y = df.drop(columns="churn"), df["churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,
                                                    random_state=0)
numeric = ["tenure", "monthly", "support"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()),
     numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["plan"]),
])
pipe = make_pipeline(prep, LogisticRegression())
cv = StratifiedKFold(5, shuffle=True, random_state=0)
search = GridSearchCV(pipe, {"logisticregression__C": [0.01, 0.1, 1, 10]},
                      cv=cv, scoring="roc_auc").fit(X_train, y_train)
print(search.best_params_, round(search.best_score_, 3))

boost = make_pipeline(
    ColumnTransformer([("cat", OrdinalEncoder(), ["plan"])],
                      remainder="passthrough"),
    HistGradientBoostingClassifier(random_state=0))
boost_auc = cross_val_score(boost, X_train, y_train, cv=cv, scoring="roc_auc")
print(round(boost_auc.mean(), 3))

best = search.best_estimator_
print(round(roc_auc_score(y_test, best.predict_proba(X_test)[:, 1]), 3))
perm = permutation_importance(best, X_test, y_test, scoring="roc_auc",
                              n_repeats=10, random_state=0)
order = perm.importances_mean.argsort()[::-1]
print([X.columns[i] for i in order])
joblib.dump({"model": best, "columns": list(X.columns)}, "churn.joblib")
loaded = joblib.load("churn.joblib")
print(bool((loaded["model"].predict(X_test) == best.predict(X_test)).all()))
```

```text
0.553 123
{'logisticregression__C': 0.1} 0.777
0.72
0.814
['tenure', 'support', 'monthly', 'plan']
True
```

- **Veri:** 1500 abone; terk oranı %55,3; aylık ücretin 123 hücresi eksik.
  Terki üreten kural doğrusal (lojistik): kısa süreli, çok destek isteyen,
  `basic` planlı abone daha çok terk ediyor.
- **Hazırlık:** `ColumnTransformer` sayılara medyanla doldurma + ölçek,
  plana one-hot uyguluyor; hepsi pipeline'ın içinde, sızıntı yok.
- **Değerlendirme:** `StratifiedKFold` ile karıştırarak, AUC ile `C` arandı:
  en iyisi 0,1, çapraz doğrulama AUC'si 0,777.
- **Model karşılaştırması:** aynı katlarda boosting 0,72. Veri doğrusal bir
  kuralla üretildiği için doğrusal model önde; "en güçlü model" her veride
  en iyisi değil, ölçülür.
- **Test:** seçilen model test verisinde bir kez ölçüldü: AUC 0,814.
- **Açıklama:** permütasyon önemi sırası `tenure`, `support`, `monthly`,
  `plan`; kuralın en büyük etkisi süredeydi.
- **Kayıt:** model ve sütun listesi tek dosyada; yüklenen model aynı
  tahminleri veriyor.

## Sonra

Notlarda bütün modülün tek sayfalık özeti ve buradan nereye gidileceği var.
Temel Kütüphaneler patikasının dört modülü burada bitiyor: Python
Kütüphaneleri (Başlangıç ve İleri), Veri Bilimi Kütüphaneleri ve ML
Kütüphaneleri.
