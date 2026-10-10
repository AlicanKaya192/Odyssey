import numpy as np


def fit_line(xs, ys):
    x = np.array(xs, dtype=float)
    X = np.column_stack([np.ones_like(x), x])
    coef, *_ = np.linalg.lstsq(X, np.array(ys, dtype=float), rcond=None)
    return coef.round(3).tolist()

print(fit_line([1, 2, 3, 4], [2.1, 3.9, 6.2, 7.8]))
