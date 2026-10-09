import numpy as np


def gini(y):
    if len(y) == 0:
        return 0.0
    p = np.bincount(y) / len(y)
    return 1 - (p ** 2).sum()


def fit_stump(X, y):
    X, y = np.array(X, dtype=float), np.array(y, dtype=int)
    best = None
    for j in range(X.shape[1]):
        values = np.unique(X[:, j])
        for t in (values[:-1] + values[1:]) / 2:
            left = X[:, j] <= t
            g = (left.sum() * gini(y[left]) + (~left).sum() * gini(y[~left])) / len(y)
            if best is None or g < best[0] - 1e-12:
                best = (g, j, t, left)
    g, j, t, left = best
    left_label = int(np.bincount(y[left]).argmax())
    right_label = int(np.bincount(y[~left]).argmax())
    return [j, round(float(t), 4), left_label, right_label]

X = [[1, 9], [2, 8], [3, 1], [6, 2], [7, 9], [8, 1]]
y = [0, 0, 0, 1, 1, 1]
print(fit_stump(X, y))
