import numpy as np


def ridge(X, y, alpha):
    xm, ym = X.mean(axis=0), y.mean()
    Xc, yc = X - xm, y - ym
    w = np.linalg.solve(Xc.T @ Xc + alpha * np.eye(X.shape[1]), Xc.T @ yc)
    return ym - xm @ w, w


def best_alpha(X, y, alphas, k):
    X, y = np.array(X, dtype=float), np.array(y, dtype=float)
    n = len(y)

    def cv_error(alpha):
        errs = []
        for test in np.array_split(np.arange(n), k):
            train = np.setdiff1d(np.arange(n), test)
            b, w = ridge(X[train], y[train], alpha)
            errs.append(((b + X[test] @ w - y[test]) ** 2).mean())
        return np.mean(errs)

    return min(alphas, key=cv_error)

rng = np.random.default_rng(1)
X = rng.normal(0, 1, size=(40, 5))
y = X @ np.array([2.0, -1.0, 0.0, 0.0, 0.5]) + rng.normal(0, 1, 40)
print(best_alpha(X.tolist(), y.tolist(), [0.01, 1.0, 100.0], 4))
