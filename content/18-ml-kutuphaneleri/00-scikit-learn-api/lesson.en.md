# The scikit-learn API

scikit-learn has more than a hundred models and transformers; there is no need
to learn each one separately, because they all use **the same interface**:
build, learn from data with `fit`, then use with `predict` or `transform`.
Someone who grasps this interface once can use a new model after five minutes
with its documentation. This section covers that shared contract, where the
learned values live and the two most common mistakes (an unfitted model, a
wrongly shaped input); at the end comes the idea of **data leakage**, which we
will return to throughout the module.

## fit, transform, predict

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

X = np.array([[1.0, 200], [2.0, 220], [3.0, 400], [4.0, 410]])
y = np.array([0, 0, 1, 1])
scaler = StandardScaler()
Xs = scaler.fit_transform(X)
print(scaler.mean_.tolist(), Xs.mean(axis=0).round(6).tolist())
model = LogisticRegression()
model.fit(Xs, y)
print(model.predict(Xs).tolist(), model.score(Xs, y))
print(model.predict_proba(Xs[:1]).round(3).tolist())
```

```text
[2.5, 307.5] [0.0, 0.0]
[0, 0, 1, 1] 1.0
[[0.852, 0.148]]
```

| Method | Who has it | What it does |
|---|---|---|
| `fit(X, y)` | all | learns from data, returns the object itself |
| `transform(X)` | transformers | applies what it learned to data |
| `fit_transform(X)` | transformers | both at once |
| `predict(X)` | models | a prediction |
| `predict_proba(X)` | most classifiers | class probabilities |
| `score(X, y)` | models | the default measure (accuracy for classification, R² for regression) |

- `X` is always **two-dimensional**: rows are samples, columns are features.
  `y` is the one-dimensional target.
- The transformer (`StandardScaler`) and the model (`LogisticRegression`) use
  the same `fit` pattern. That is why we will later chain the two in a
  **Pipeline**.
- `predict_proba` gives a probability for each class: the first sample is 0
  with probability 85.2%.

## Settings and what is learned

```python
from sklearn.base import clone
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(C=0.5, max_iter=500)
print(model.get_params()["C"], model.get_params()["max_iter"])
model.set_params(C=2.0)
print(model.C, hasattr(model, "coef_"))
twin = clone(model)
print(twin.C, twin is model)
```

```text
0.5 500
2.0 False
2.0 False
```

- What is given to the constructor are **hyperparameters**: you choose how the
  model learns (`C`, `max_iter`). They are read and changed with `get_params` /
  `set_params`; hyperparameter searches use this.
- What is **learned** from data ends with an underscore: `coef_`, `mean_`,
  `classes_`. It does not exist before `fit` (`hasattr` → `False`).
- `clone` builds a new, **unfitted** copy with the same settings.
  Cross-validation rebuilds the model from scratch this way in each fold.

## Two common mistakes

```python
import numpy as np
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LinearRegression

model = LinearRegression()
try:
    model.predict(np.array([[1.0]]))
except NotFittedError as error:
    print(type(error).__name__ + ":", str(error).split(".")[0])
model.fit(np.array([[1.0], [2.0], [3.0]]), np.array([2.0, 4.0, 6.0]))
print(model.coef_.round(3).tolist(), round(float(model.intercept_), 3))
try:
    model.predict(np.array([4.0]))
except ValueError as error:
    print("ValueError:", str(error).splitlines()[0])
print(model.predict(np.array([[4.0]])).round(3).tolist())
```

```text
NotFittedError: This LinearRegression instance is not fitted yet
[2.0] 0.0
ValueError: Expected 2D array, got 1D array instead:
[8.0]
```

- Predicting with a model that was not `fit` raises `NotFittedError`.
- Even data with **a single feature** is given in two dimensions: `[4.0]` could
  be one row or one column, scikit-learn does not guess and stops. The right
  form is `[[4.0]]` (one row, one column); for a NumPy array,
  `x.reshape(-1, 1)`.

## random_state

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=300, n_features=6, n_informative=3,
                           flip_y=0.1, random_state=0)
split = train_test_split(X, y, test_size=0.25, random_state=0)
X_train, X_test, y_train, y_test = split
scores = []
for seed in [0, 1, 2]:
    forest = RandomForestClassifier(n_estimators=5, random_state=seed)
    forest.fit(X_train, y_train)
    scores.append(round(forest.score(X_test, y_test), 3))
print(X_train.shape, X_test.shape, scores)
again = RandomForestClassifier(n_estimators=5, random_state=0).fit(X_train, y_train)
print(again.score(X_test, y_test) == scores[0])
```

```text
(225, 6) (75, 6) [0.84, 0.853, 0.867]
True
```

- Everything that uses randomness (`train_test_split`, a forest,
  `make_classification`) takes `random_state`. The same seed gives the same
  result.
- When the seed changed, the score moved between 0.84 and 0.867. **The result
  of a single seed is not a model's "true" score**; when comparing two models
  you need to know this margin (the validation tools section).

## A first look at data leakage

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=200, n_features=4, random_state=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
wrong = StandardScaler().fit(X)
right = StandardScaler().fit(X_train)
print(wrong.mean_.round(3).tolist())
print(right.mean_.round(3).tolist())
X_test_scaled = right.transform(X_test)
print(X_test_scaled.mean(axis=0).round(2).tolist())
```

```text
[0.018, 0.006, -0.014, 0.008]
[-0.109, -0.069, -0.041, -0.129]
[0.42, 0.37, 0.08, 0.34]
```

- `wrong` learned the mean from **all** the data: it also saw the test rows.
  The test set is no longer "never seen data"; the score can come out better
  than it will be in reality. This is called **data leakage**.
- The right way: a transformer is `fit` only on the **training** data, and only
  `transform` is applied to the test data. That is why the test data's mean is
  not exactly 0; it does not need to be.
- Keeping this rule by hand is hard; later a `Pipeline` will apply it by
  itself.

## Summary

- Every object: build → `fit` → `predict` / `transform`. `X` is
  two-dimensional.
- Hyperparameters in the constructor (`get_params`), learned values with an
  underscore (`coef_`). `clone` is an unfitted copy.
- `NotFittedError` and "Expected 2D array" are the two most common mistakes.
- With randomness, `random_state`; do not trust a single seed's score.
- Fit transformers only on the training data.
