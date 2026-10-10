A pipeline's steps transform only `X`. But sometimes what needs transforming
is **the target itself**: right-skewed, multiplicatively growing targets like
price, income or waiting time. `TransformedTargetRegressor` transforms the
target before training and turns the prediction back.

```python
import numpy as np
from sklearn.compose import TransformedTargetRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(7)
X = rng.uniform(0, 3, size=(300, 1))
y = np.exp(1.0 + 1.2 * X[:, 0] + rng.normal(0, 0.3, 300))
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=7)
plain = LinearRegression().fit(X_train, y_train)
logged = TransformedTargetRegressor(regressor=LinearRegression(),
                                    func=np.log, inverse_func=np.exp)
logged.fit(X_train, y_train)
print(round(plain.score(X_test, y_test), 3), round(logged.score(X_test, y_test), 3))
at_zero = [round(float(m.predict([[0.0]])[0]), 2) for m in (plain, logged)]
print(*at_zero)
print(round(float(logged.regressor_.coef_[0]), 2))
```

```text
0.645 0.807
-11.92 2.66
1.19
```

## What happened?

- The target grows exponentially. The plain linear model got a test R² of
  0.645 and predicted a **negative** price at x = 0 (−11.92): a value that can
  never happen.
- `TransformedTargetRegressor` trained the model on `log(y)` and turned the
  prediction back with `exp`: R² 0.807, 2.66 at x = 0 (the true value is
  e¹ ≈ 2.72).
- The inner model learned the slope of `log(y)`: 1.19 (we used 1.2 when
  generating the data).
- Training on `np.log(y)` by hand and turning predictions back with `np.exp`
  works too, but it is easy to forget; scores and cross-validation are then
  computed on the wrong scale too. This class does both correctly and can be
  placed at the end of a pipeline.

## When?

- If the target is always positive and right-skewed (price, income, duration),
  `np.log` / `np.exp`; if it can be zero, `np.log1p` / `np.expm1`.
- To learn the transformation from the data, give
  `transformer=QuantileTransformer()` or `PowerTransformer()`.
