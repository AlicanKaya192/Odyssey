In boosting, the number of trees is the knob of overfitting. The practical way
to find the right number is **early stopping**: set a part of the training data
aside for validation, look at the validation error after each tree, and stop if
there is no improvement for a certain number of rounds.

```python
import numpy as np
from sklearn.tree import DecisionTreeRegressor

rng = np.random.default_rng(22)
X = rng.uniform(0, 10, (300, 1))
y = np.sin(X[:, 0]) * 3 + rng.normal(0, 0.8, 300)
Xtr, ytr, Xval, yval = X[:200], y[:200], X[200:], y[200:]

pred_tr = np.full(200, ytr.mean())
pred_val = np.full(100, ytr.mean())
best, best_n, waited = np.inf, 0, 0
for n in range(1, 1001):
    tree = DecisionTreeRegressor(max_depth=3).fit(Xtr, ytr - pred_tr)
    pred_tr += 0.1 * tree.predict(Xtr)
    pred_val += 0.1 * tree.predict(Xval)
    val = ((yval - pred_val) ** 2).mean()
    if val < best - 1e-9:
        best, best_n, waited = val, n, 0
    else:
        waited += 1
    if waited == 30:                                  # 30 rounds without gain
        break
print(best_n, n, round(best, 3), round(val, 3))
```

```text
45 75 0.743 0.758
```

The validation error reached its lowest value at the number of trees in the
first column; after waiting patiently for 30 rounds, training stopped at the
round in the second column. The last error is slightly above the best: the
model is used with the number of trees from the best round. It stopped far
before building a thousand trees. In scikit-learn,
`GradientBoostingRegressor(n_iter_no_change=..., validation_fraction=...)` and
`HistGradientBoosting*` apply the same idea.
