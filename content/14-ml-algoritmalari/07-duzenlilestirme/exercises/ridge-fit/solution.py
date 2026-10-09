import numpy as np


def ridge_fit(X, y, alpha):
    X, y = np.array(X, dtype=float), np.array(y, dtype=float)
    xm, ym = X.mean(axis=0), y.mean()
    Xc, yc = X - xm, y - ym
    w = np.linalg.solve(Xc.T @ Xc + alpha * np.eye(X.shape[1]), Xc.T @ yc)
    return [round(float(ym - xm @ w), 4)] + [round(float(v), 4) for v in w]

X = [[1, 2], [2, 1], [3, 4], [4, 3], [5, 5]]
y = [9, 6, 17, 14, 21]
print(ridge_fit(X, y, 0.0))
print(ridge_fit(X, y, 10.0))
