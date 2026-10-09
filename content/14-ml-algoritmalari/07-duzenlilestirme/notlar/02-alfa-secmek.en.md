`α` cannot be chosen by looking at the training data: the training error is
always lowest at `α = 0`. The right way is to measure the cross-validation
error for each candidate `α`.

```python
import numpy as np
from sklearn.linear_model import RidgeCV

rng = np.random.default_rng(7)
n = 60
X = rng.normal(0, 1, size=(n, 8))
true_w = np.array([3.0, -2.0, 1.5, 0, 0, 0, 0, 0])
y = 1.0 + X @ true_w + rng.normal(0, 1.0, n)


def ridge(X, y, alpha):
    xm, ym = X.mean(axis=0), y.mean()
    Xc, yc = X - xm, y - ym
    w = np.linalg.solve(Xc.T @ Xc + alpha * np.eye(X.shape[1]), Xc.T @ yc)
    return ym - xm @ w, w


def cv_error(alpha, k=5):
    errs = []
    for test in np.array_split(np.arange(n), k):
        train = np.setdiff1d(np.arange(n), test)
        b, w = ridge(X[train], y[train], alpha)
        errs.append(((b + X[test] @ w - y[test]) ** 2).mean())
    return np.mean(errs)


alphas = [0.01, 0.1, 1.0, 10.0, 100.0]
for a in alphas:
    print(a, round(cv_error(a), 4))
best = min(alphas, key=cv_error)
ref = RidgeCV(alphas=alphas, cv=5, scoring="neg_mean_squared_error")
ref.fit(X, y)
print(best, ref.alpha_)
```

```text
0.01 0.9687
0.1 0.9674
1.0 0.9676
10.0 1.6668
100.0 8.3057
0.1 0.1
```

On this data the signal is strong and there are seven times as many samples as
features; the best `α` is small (0.1), and 0.01–1 are almost the same. `α = 100`
multiplies the error by eight: too much shrinkage. scikit-learn's `RidgeCV`
chose the same `α` with the same folds. Listing the candidates on a logarithmic
scale (0.01, 0.1, 1, …) is the usual way; the order of magnitude matters more
than individual values.
