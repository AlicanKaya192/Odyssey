## Pipeline

| Yazım | Ne yapar |
|---|---|
| `Pipeline([("scale", StandardScaler()), ("model", Ridge())])` | adlı adımlar |
| `make_pipeline(StandardScaler(), Ridge())` | adlar otomatik (`standardscaler`) |
| `pipe.set_params(model__alpha=1.0)` | iç adımın ayarı (`adım__ayar`) |
| `pipe["model"]`, `pipe.named_steps["model"]` | adıma ulaş |
| `pipe[:-1].transform(X)` | modelsiz hazırlık çıktısı |
| `pipe.fit(X, y)`, `pipe.predict(X)`, `pipe.score(X, y)` | bütün zincir |
| `make_pipeline(..., memory="cache")` | ağır adımların sonucunu diske önbelleğe al |

## Kendi dönüştürücün

```python
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted


class MyStep(BaseEstimator, TransformerMixin):
    def __init__(self, k=1.0):     # yalnızca ayarları sakla
        self.k = k

    def fit(self, X, y=None):      # öğren, sonuna _ koy, self döndür
        self.mean_ = X.mean(axis=0)
        return self

    def transform(self, X):        # uygula
        check_is_fitted(self)
        return (X - self.mean_) * self.k
```

## Hedef ve fonksiyon

| Yazım | Ne zaman |
|---|---|
| `FunctionTransformer(np.log1p)` | öğrenmeyen dönüşüm |
| `TransformedTargetRegressor(regressor=..., func=np.log, inverse_func=np.exp)` | çarpık hedef |

## Hatalar

| Belirti | Sebep |
|---|---|
| Rastgele veride yüksek çapraz doğrulama skoru | öğrenen adım pipeline'ın dışında |
| `Invalid parameter 'C' for estimator Pipeline` | `model__C` yazılmalı |
| `clone` sonrası ayar kayboldu | `__init__` ayarı başka adla sakladı |
| Kendi adımın `get_params()` boş | `BaseEstimator`'dan türetilmedi |
| Eksi fiyat tahmini | çarpık hedef dönüştürülmedi |
