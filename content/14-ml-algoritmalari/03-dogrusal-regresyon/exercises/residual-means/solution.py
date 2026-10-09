import numpy as np


def residual_means(x, y, parts):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    order = np.argsort(x)
    x, y = x[order], y[order]
    A = np.column_stack([np.ones(len(x)), x])
    w = np.linalg.lstsq(A, y, rcond=None)[0]
    resid = y - A @ w
    return [round(float(p.mean()), 2) for p in np.array_split(resid, parts)]

x = [0, 1, 2, 3, 4, 5, 6, 7, 8]
y = [v * v for v in x]
print(residual_means(x, y, 3))
