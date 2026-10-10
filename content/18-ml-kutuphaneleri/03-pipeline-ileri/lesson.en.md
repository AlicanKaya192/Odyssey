# Pipelines and Your Own Transformer

A `Pipeline` chains preparation steps and a model one after another in a
single object. We used it in shortcut form in earlier sections; this section
shows three things: how to reach the steps and their settings, **why** a
pipeline prevents leakage (we will see it by measuring an 88% "success" on
random data), and how to write a step scikit-learn does not have as your own
transformer.

## Steps and their settings

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler

pipe = Pipeline([("scale", StandardScaler()), ("model", LogisticRegression(C=1.0))])
print(list(pipe.named_steps))
auto = make_pipeline(StandardScaler(), LogisticRegression())
print(list(auto.named_steps))
pipe.set_params(model__C=0.1)
print(pipe.get_params()["model__C"], pipe["model"].C)
print(type(pipe[:-1]).__name__, len(pipe[:-1]))
```

```text
['scale', 'model']
['standardscaler', 'logisticregression']
0.1 0.1
Pipeline 1
```

- With `Pipeline([(name, step), ...])` you give the names; `make_pipeline`
  uses the lower-cased class name.
- An inner step's setting is written as **`step__setting`** (two underscores):
  `model__C`. A hyperparameter search works on the whole pipeline with these
  names.
- `pipe["model"]` reaches a step by name, `pipe[:-1]` by slicing; the slice is
  a pipeline too (the preparation part without the model). To see the
  prepared data, `pipe[:-1].transform(X)`.
- All steps but the last must be transformers; the last can be a model or a
  transformer.

## Why does a pipeline prevent leakage?

```python
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(6)
X = rng.normal(size=(100, 5000))
y = rng.integers(0, 2, 100)
X_selected = SelectKBest(f_classif, k=20).fit_transform(X, y)
wrong = cross_val_score(LogisticRegression(), X_selected, y, cv=5).mean()
pipe = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression())
right = cross_val_score(pipe, X, y, cv=5).mean()
print(round(wrong, 2), round(right, 2))
```

```text
0.88 0.58
```

- The data is **completely random**: 5000 noise columns, a random target. The
  true success should be around 50%.
- The wrong way: choose the 20 columns most related to the target from all the
  data, **then** cross-validate. The selection also saw the test folds'
  answers; among 5000 random columns, those that happen to agree with the
  target got chosen. Result: 88%, completely fake.
- The right way: the selection is inside the pipeline. Cross-validation
  `clone`s the pipeline in each fold and `fit`s it on that fold's training data
  only; the selection never sees the test fold. Result: 58%, close to chance.
- The rule: **every step that learns something from data** (scaling, filling,
  selecting, encoding) must be inside the pipeline.

## Your own transformer

```python
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted


class Clipper(BaseEstimator, TransformerMixin):
    def __init__(self, low=0.01, high=0.99):
        self.low = low
        self.high = high

    def fit(self, X, y=None):
        X = np.asarray(X, dtype=float)
        self.lower_ = np.quantile(X, self.low, axis=0)
        self.upper_ = np.quantile(X, self.high, axis=0)
        return self

    def transform(self, X):
        check_is_fitted(self)
        return np.clip(np.asarray(X, dtype=float), self.lower_, self.upper_)


X = np.array([[1.0], [2.0], [3.0], [4.0], [100.0]])
clip = Clipper(low=0.0, high=0.75)
print(clip.fit_transform(X).ravel().tolist(), clip.upper_.tolist())
print(clip.get_params())
```

```text
[1.0, 2.0, 3.0, 4.0, 4.0] [4.0]
{'high': 0.75, 'low': 0.0}
```

- A step that limits (clips) outliers is not ready-made in scikit-learn; a
  class that follows the contract enters a pipeline.
- **`__init__` only stores the settings** and does nothing else; parameter
  names must equal attribute names. `BaseEstimator` writes `get_params` /
  `set_params` itself by relying on this rule (`clone` and searches use it).
- **`fit` learns** (the limits from the training data), puts the results in
  attributes with an underscore and returns `self`.
- **`transform` applies**; `check_is_fitted` gives a clear error if not
  fitted. `TransformerMixin` adds `fit_transform` by itself.
- The value 100 was clipped to the training data's 75th percentile (4).

## A shortcut: FunctionTransformer

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer

X = np.array([[1.0], [10.0], [100.0], [1000.0]])
y = np.array([1.0, 2.0, 3.0, 4.0])
plain = LinearRegression().fit(X, y)
logged = make_pipeline(FunctionTransformer(np.log10), LinearRegression()).fit(X, y)
print(round(plain.score(X, y), 3), round(logged.score(X, y), 3))
print(logged.predict([[10_000.0]]).round(2).tolist())
```

```text
0.679 1.0
[5.0]
```

- If a step **learns nothing** from data (a logarithm, a ratio, selecting
  columns), no class is needed: `FunctionTransformer(function)`.
- On a logarithmic relationship a plain linear model got R² 0.679; with the
  logarithm the relationship became an exact line (1.0) and the prediction for
  10,000 is 5.
- Writing a learning step (subtracting a mean with `np.mean`) as a function
  causes leakage: the function takes **the current** data's mean on every
  call, not the training mean.

## Summary

- `Pipeline` / `make_pipeline`; an inner setting is `step__setting`;
  `pipe["name"]`, `pipe[:-1]`.
- Every step that learns from data goes inside the pipeline; otherwise
  cross-validation shows a fake success.
- Your own transformer: `BaseEstimator` + `TransformerMixin`, `__init__` only
  settings, `fit` learns and returns `self`, `transform` applies.
- For a step that learns nothing, `FunctionTransformer`.
