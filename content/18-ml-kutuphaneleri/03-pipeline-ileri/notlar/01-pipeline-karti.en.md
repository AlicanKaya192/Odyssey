## Pipeline

| Code | What it does |
|---|---|
| `Pipeline([("scale", StandardScaler()), ("model", Ridge())])` | named steps |
| `make_pipeline(StandardScaler(), Ridge())` | automatic names (`standardscaler`) |
| `pipe.set_params(model__alpha=1.0)` | an inner step's setting (`step__setting`) |
| `pipe["model"]`, `pipe.named_steps["model"]` | reach a step |
| `pipe[:-1].transform(X)` | the preparation output without the model |
| `pipe.fit(X, y)`, `pipe.predict(X)`, `pipe.score(X, y)` | the whole chain |
| `make_pipeline(..., memory="cache")` | cache heavy steps' results on disk |

## Your own transformer

```python
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted


class MyStep(BaseEstimator, TransformerMixin):
    def __init__(self, k=1.0):     # only store the settings
        self.k = k

    def fit(self, X, y=None):      # learn, end with _, return self
        self.mean_ = X.mean(axis=0)
        return self

    def transform(self, X):        # apply
        check_is_fitted(self)
        return (X - self.mean_) * self.k
```

## Target and function

| Code | When |
|---|---|
| `FunctionTransformer(np.log1p)` | a transformation that learns nothing |
| `TransformedTargetRegressor(regressor=..., func=np.log, inverse_func=np.exp)` | a skewed target |

## Errors

| Symptom | Cause |
|---|---|
| A high cross-validation score on random data | a learning step is outside the pipeline |
| `Invalid parameter 'C' for estimator Pipeline` | it must be `model__C` |
| A setting lost after `clone` | `__init__` stored the setting under another name |
| Your step's `get_params()` is empty | not derived from `BaseEstimator` |
| A negative price prediction | a skewed target was not transformed |
