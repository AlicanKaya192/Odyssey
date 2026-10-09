A tree predicts numbers too. Instead of the Gini, the **sum of squared errors**
is minimised: a split is the threshold that lowers most the sum of the two
sides' squared errors around their own means. The prediction in a leaf is the
mean of the samples there.

```python
import numpy as np
from sklearn.tree import DecisionTreeRegressor

rng = np.random.default_rng(20)
x = rng.uniform(0, 10, 120)
y = np.where(x < 4, 2.0, np.where(x < 7, 5.0, 3.0)) + rng.normal(0, 0.3, 120)


def sse(v):
    return ((v - v.mean()) ** 2).sum()


def best_cut(x, y):
    best_t, best_err = None, sse(y)
    values = np.unique(x)
    for t in (values[:-1] + values[1:]) / 2:
        left = x <= t
        err = sse(y[left]) + sse(y[~left])
        if err < best_err - 1e-12:
            best_t, best_err = t, err
    return best_t


def grow(x, y, depth):
    t = best_cut(x, y) if depth > 0 else None
    if t is None:
        return float(y.mean())                      # a leaf: the mean
    left = x <= t
    return (t, grow(x[left], y[left], depth - 1), grow(x[~left], y[~left], depth - 1))


def ask(node, v):
    while isinstance(node, tuple):
        node = node[1] if v <= node[0] else node[2]
    return node


tree = grow(x, y, 2)
xq = np.array([1.0, 5.0, 9.0])
ours = np.array([ask(tree, v) for v in xq])
ref = DecisionTreeRegressor(max_depth=2).fit(x[:, None], y).predict(xq[:, None])
print(round(tree[0], 3), ours.round(2), np.allclose(ours, ref))
```

```text
4.008 [1.97 5.   2.95] True
```

The data was a staircase (2 up to 4, 5 up to 7, then 3). The first cut is at one
of the steps; the predictions for the three queries are close to the step
values and match scikit-learn's `DecisionTreeRegressor`. A regression tree's
prediction is **stepped**: it gives as many different values as there are
leaves and cannot see a slope in between.
