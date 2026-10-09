import numpy as np


def soft(z, t):
    return np.sign(z) * max(abs(z) - t, 0.0)


def lasso_fit(X, y, alpha, rounds):
    X, y = np.array(X, dtype=float), np.array(y, dtype=float)
    xm, ym = X.mean(axis=0), y.mean()
    Xc, yc = X - xm, y - ym
    n, d = Xc.shape
    w = np.zeros(d)
    # rounds rounds, each j in each round.
    return [round(float(ym - xm @ w), 3)] + [round(float(v), 3) for v in w]

X = [[1, 0, 2], [2, 1, 0], [3, 0, 1], [4, 1, 3], [5, 0, 0]]
y = [3, 5, 7, 9, 11]
print(lasso_fit(X, y, 0.1, 300))
print(lasso_fit(X, y, 2.0, 300))
