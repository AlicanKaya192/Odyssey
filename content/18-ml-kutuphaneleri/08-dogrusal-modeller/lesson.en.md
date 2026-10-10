# Linear Models

You wrote linear regression, Ridge, Lasso and logistic regression from
scratch with NumPy in the ML Algorithms module. This section covers the
**use** of their scikit-learn versions: when coefficients can be compared,
how `RidgeCV` / `LassoCV` choose the penalty themselves, why logistic
regression warns that it "did not converge", how the L1 penalty is written in
this version, and how a linear model learns a curved relationship.

## Coefficients and scale

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(0)
area = rng.uniform(50, 200, 300)        # square metres
rooms = rng.integers(1, 6, 300)
age = rng.uniform(0, 40, 300)            # years
price = 3 * area + 20 * rooms - 2 * age + rng.normal(0, 30, 300)
X = pd.DataFrame({"area": area, "rooms": rooms, "age": age})
raw = LinearRegression().fit(X, price)
print({c: round(float(v), 2) for c, v in zip(X.columns, raw.coef_)})
scaled = make_pipeline(StandardScaler(), LinearRegression()).fit(X, price)
print({c: round(float(v), 1) for c, v in zip(X.columns, scaled[-1].coef_)})
```

```text
{'area': 2.96, 'rooms': 20.21, 'age': -2.05}
{'area': 132.2, 'rooms': 28.4, 'age': -22.7}
```

- `coef_` holds the coefficients in column order, `intercept_` the constant
  term. The raw coefficients are close to the 3, 20, −2 that made the data:
  "3 per square metre, 20 per room".
- Looking at raw coefficients and saying "rooms matter most" is wrong: rooms
  range over 1–5, area over 50–200. Numbers in different units are not
  compared.
- In the scaled model a coefficient is "the effect of a one standard
  deviation change": area, at 132.2, is clearly the strongest. To **compare**
  coefficients, scale first; to **interpret** them (per unit), use the raw
  model.

## RidgeCV: many columns, few rows

```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.model_selection import train_test_split

X, y = make_regression(n_samples=80, n_features=60, n_informative=10,
                       noise=30, random_state=3)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=3)
ols = LinearRegression().fit(X_train, y_train)
ridge = RidgeCV(alphas=np.logspace(-3, 3, 13)).fit(X_train, y_train)
print(round(ols.score(X_train, y_train), 3), round(ols.score(X_test, y_test), 3))
print(round(ridge.alpha_, 2), round(ridge.score(X_train, y_train), 3),
      round(ridge.score(X_test, y_test), 3))
```

```text
1.0 -5.401
3.16 0.99 0.87
```

- 60 training rows, 60 columns: plain linear regression memorises the
  training data **completely** (R² 1.0) and gets R² −5.4 on the test, far
  worse than predicting the mean.
- `RidgeCV` chooses the penalty itself from the given `alphas` (3.16) and the
  test R² is 0.87. The training score dropped a little, the test score was
  rescued.
- By default `RidgeCV` computes leave-one-out validation from a single
  decomposition, without retraining the model for each `alpha`; no need to
  write `GridSearchCV(Ridge(), ...)`. Its counterpart for logistic
  regression is `LogisticRegressionCV`.

## LassoCV: prediction or selection?

```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import Lasso, LassoCV
from sklearn.model_selection import cross_val_score

X, y, true = make_regression(n_samples=200, n_features=30, n_informative=5,
                             noise=10, coef=True, random_state=5)
lasso = LassoCV(cv=5, random_state=0).fit(X, y)
print(round(lasso.alpha_, 3), int((lasso.coef_ != 0).sum()))
print(np.flatnonzero(true).tolist())
strong = Lasso(alpha=5).fit(X, y)
print(np.flatnonzero(strong.coef_).tolist())
for alpha in [lasso.alpha_, 5]:
    print(round(cross_val_score(Lasso(alpha=alpha), X, y, cv=5).mean(), 3))
```

```text
0.257 23
[9, 18, 20, 21, 29]
[9, 18, 20, 21, 29]
0.994
0.987
```

- Only 5 of the 30 columns affect the target (we got the true coefficients
  with `coef=True`: 9, 18, 20, 21, 29).
- `LassoCV` chose the best penalty for **prediction** (0.257) and left 23
  columns non-zero: the true 5 plus 18 noise columns with small
  coefficients.
- A stronger penalty (`alpha=5`) left exactly the true 5 columns; the
  prediction score fell only slightly, from 0.994 to 0.987.
- The lesson: a cross-validated Lasso predicts well but is too generous for
  **selecting** columns. If the goal is few, correct columns, the penalty is
  raised a little.

## LogisticRegression and convergence

```python
import warnings
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_wine(return_X_y=True)        # 13 measurements, 3 wine types
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    raw = LogisticRegression().fit(X, y)
print([type(w.message).__name__ for w in caught], raw.n_iter_)
pipe = make_pipeline(StandardScaler(), LogisticRegression()).fit(X, y)
print(pipe[-1].n_iter_, pipe[-1].coef_.shape)
slow = LogisticRegression(max_iter=5000)
print(round(cross_val_score(slow, X, y, cv=5).mean(), 3),
      round(cross_val_score(pipe, X, y, cv=5).mean(), 3))
```

```text
['ConvergenceWarning'] [100]
[15] (3, 13)
0.961 0.983
```

- On the raw data the solver (`lbfgs`) hit its limit of 100 steps and raised
  a `ConvergenceWarning`: "I stopped before finding the best coefficients".
  The cause is scale: one column ranges over 0.13–0.66, `proline` over
  278–1680.
- Scaled, it finished in 15 steps. `max_iter=5000` silences the warning but
  does not fix the problem: accuracy 0.961 on raw data, 0.983 scaled.
- With three classes `coef_` is 3 × 13: each class has its own
  coefficients.
- `C` is the **inverse** of the penalty: a small `C` is a strong penalty. It
  works the opposite way to Ridge's `alpha`.

## The L1 penalty: l1_ratio

```python
Xs = StandardScaler().fit_transform(X)
for C in [1, 0.1]:
    model = LogisticRegression(l1_ratio=1, solver="saga", C=C, max_iter=5000)
    model.fit(Xs, y)
    print(C, (model.coef_ != 0).sum(axis=1).tolist())
```

```text
1 [3, 8, 4]
0.1 [4, 4, 4]
```

- `l1_ratio=1` is pure L1 (like Lasso), `0` pure L2 (the default), values in
  between a mix of the two (elastic net). Not every solver supports L1;
  `saga` does.
- At `C=1` the classes use 3, 8 and 4 columns; at `C=0.1`, 4 each. As the
  penalty grows, coefficients become zero.
- **The old way:** `penalty="l1"`, common online, raises a `FutureWarning` in
  this version ("deprecated in 1.8, removed in 1.10"). For an unpenalised
  model, write `C=np.inf` instead of `penalty=None` as well.

## A curved relationship: PolynomialFeatures

```python
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

rng = np.random.default_rng(1)
x = rng.uniform(-3, 3, 200)
y = 2 * np.sin(x) + rng.normal(0, 0.3, 200)
X = x.reshape(-1, 1)
cv = KFold(5, shuffle=True, random_state=0)
for degree in [1, 3, 5]:
    model = make_pipeline(PolynomialFeatures(degree), StandardScaler(),
                          Ridge(alpha=1e-3))
    print(degree, round(cross_val_score(model, X, y, cv=cv).mean(), 3))
names = PolynomialFeatures(2).fit(np.zeros((1, 3))).get_feature_names_out()
print(names.tolist())
print(PolynomialFeatures(3).fit(np.zeros((1, 20))).n_output_features_)
```

```text
1 0.641
3 0.963
5 0.966
['1', 'x0', 'x1', 'x2', 'x0^2', 'x0 x1', 'x0 x2', 'x1^2', 'x1 x2', 'x2^2']
1771
```

- The relationship is a sine; a straight line stays at R² 0.641.
  `PolynomialFeatures(3)` adds `x²` and `x³` columns beside `x`; the model is
  still **linear** (in the new columns) but draws a curve: 0.963.
- With several columns, products are added too (`x0 x1`). 3 columns at
  degree 2 give 10 columns, 20 columns at degree 3 give 1771: it explodes
  quickly. That is why a penalised model like Ridge is put behind it.

## Summary

- Scale to compare coefficients; use the raw model for per-unit
  interpretation.
- With many columns and few rows plain regression memorises; `RidgeCV` /
  `LassoCV` choose the penalty themselves.
- `LassoCV` is good for prediction, generous for selecting columns.
- A `ConvergenceWarning` is usually missing scaling; do not silence it with
  `max_iter`.
- For L1, `l1_ratio=1` and `solver="saga"`; `penalty=` is deprecated.
