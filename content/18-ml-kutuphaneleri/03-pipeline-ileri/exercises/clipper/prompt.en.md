Write a transformer named `Clipper` (`BaseEstimator`, `TransformerMixin`):

- `__init__(self, high=0.99)`: only `self.high = high`.
- `fit(X, y=None)`: write each column's `high` percentile to `self.upper_` with
  `np.quantile(X, self.high, axis=0)` and return `self`.
- `transform(X)`: `check_is_fitted(self)`, then `np.minimum(X, self.upper_)`.

`clip_values(train, test, high)` should `fit` `Clipper(high=high)` on the
training data, transform the test and return a list of lists.

**Expected output:**

```
[[0.0], [4.0]]
```
