`Clipper` adında bir dönüştürücü yaz (`BaseEstimator`, `TransformerMixin`):

- `__init__(self, high=0.99)`: yalnızca `self.high = high`.
- `fit(X, y=None)`: her sütunun `high` yüzdeliğini `np.quantile(X, self.high,
  axis=0)` ile `self.upper_`'a yazsın, `self` döndürsün.
- `transform(X)`: `check_is_fitted(self)`, sonra `np.minimum(X, self.upper_)`.

`clip_values(train, test, high)` `Clipper(high=high)`'ı eğitimle `fit` edip testi
dönüştürsün ve liste listesi döndürsün.

**Beklenen çıktı:**

```
[[0.0], [4.0]]
```
