Linear regression minimises the **squares** of the errors. A single record
that is 60 units off weighs as much as 3600 records that are 1 unit off; a
few bad records pull the line towards themselves. `HuberRegressor` uses the
square for small errors and the absolute value for large ones: a far point's
pull stays limited.

```python
import numpy as np
from sklearn.linear_model import HuberRegressor, LinearRegression

rng = np.random.default_rng(4)
x = rng.uniform(0, 10, 100)
y = 2 * x + 1 + rng.normal(0, 1, 100)    # truth: slope 2, constant 1
y[:5] += 60                              # 5 bad records
X = x.reshape(-1, 1)
for model in [LinearRegression(), HuberRegressor()]:
    model.fit(X, y)
    slope, const = float(model.coef_[0]), float(model.intercept_)
    print(type(model).__name__, round(slope, 2), round(const, 2))
```

```text
LinearRegression 2.38 2.11
HuberRegressor 2.03 1.11
```

## What we see

- 5 of the 100 records are corrupted. Linear regression found a slope of
  2.38 and a constant of 2.11: the whole line moved up.
- Huber found 2.03 and 1.11, very close to the truth.

## When

- When the target has occasional measurement/recording errors and cleaning
  them one by one is not possible.
- If the bad records can be found, fix them first; Huber is insurance, not a
  cleaning tool.
- As an error measure too, MAE is less affected by outliers than MSE; the
  same idea.
