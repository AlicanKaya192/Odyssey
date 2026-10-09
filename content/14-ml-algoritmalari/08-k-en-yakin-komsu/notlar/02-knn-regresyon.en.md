KNN is used not only for classification but also for predicting numbers: the
**mean** of the targets of the nearest `k` samples is the prediction. There is
one more option: **weighting by distance**; a near neighbour's vote counts as
`1 / distance`.

```python
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

rng = np.random.default_rng(18)
x = np.sort(rng.uniform(0, 10, 80))
y = np.sin(x) + rng.normal(0, 0.2, 80)
xq = np.array([2.5, 5.0, 7.5])


def knn_reg(x, y, xq, k, weighted=False):
    out = []
    for q in xq:
        d = np.abs(x - q)
        near = np.argsort(d)[:k]
        if weighted:
            w = 1 / d[near]                       # the near count more
            out.append((w * y[near]).sum() / w.sum())
        else:
            out.append(y[near].mean())                     # a plain mean
    return np.array(out)


for weighted, mode in ((False, "uniform"), (True, "distance")):
    ours = knn_reg(x, y, xq, 7, weighted)
    model = KNeighborsRegressor(n_neighbors=7, weights=mode)
    ref = model.fit(x[:, None], y).predict(xq[:, None])
    print(mode, ours.round(3), np.allclose(ours, ref))
print(np.sin(xq).round(3))
```

```text
uniform [ 0.563 -0.779  0.873] True
distance [ 0.491 -0.878  0.956] True
[ 0.598 -0.959  0.938]
```

Both methods match scikit-learn's `KNeighborsRegressor`. The last line is the
true value (`sin x`). The distance weighting is closer to the truth at two of
the three points (5 and 7.5) but not at one (2.5): at peaks and dips the near
neighbours carry more accurate information, but weighting is also more
sensitive to noise. Which one is better is again seen with cross-validation.
