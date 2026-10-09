import numpy as np


def gini(y):
    if len(y) == 0:
        return 0.0
    p = np.bincount(y) / len(y)
    return 1 - (p ** 2).sum()


def best_threshold(x, y):
    x, y = np.array(x, dtype=float), np.array(y, dtype=int)
    values = np.unique(x)
    best_t, best_g = None, None
    for t in (values[:-1] + values[1:]) / 2:
        left = x <= t
        g = (left.sum() * gini(y[left]) + (~left).sum() * gini(y[~left])) / len(y)
        if best_g is None or g < best_g - 1e-12:
            best_t, best_g = t, g
    return round(float(best_t), 4), round(float(best_g), 4)

print(best_threshold([1, 2, 3, 4, 5, 6], [0, 0, 0, 1, 1, 1]))
print(best_threshold([3, 1, 2, 5, 4], [1, 0, 0, 1, 1]))
