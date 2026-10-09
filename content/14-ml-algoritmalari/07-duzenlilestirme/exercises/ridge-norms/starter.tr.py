import numpy as np


def ridge(X, y, alpha):
    xm, ym = X.mean(axis=0), y.mean()
    Xc, yc = X - xm, y - ym
    w = np.linalg.solve(Xc.T @ Xc + alpha * np.eye(X.shape[1]), Xc.T @ yc)
    return ym - xm @ w, w


def ridge_norms(X, y, alphas):
    X, y = np.array(X, dtype=float), np.array(y, dtype=float)
    # Her alfa icin |w| toplami.
    return []

X = [[1, 2], [2, 1], [3, 4], [4, 3], [5, 5]]
y = [9, 6, 17, 14, 21]
print(ridge_norms(X, y, [0.0, 1.0, 10.0, 100.0]))
