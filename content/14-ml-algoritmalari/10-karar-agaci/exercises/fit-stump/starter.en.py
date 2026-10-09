import numpy as np


def gini(y):
    if len(y) == 0:
        return 0.0
    p = np.bincount(y) / len(y)
    return 1 - (p ** 2).sum()


def fit_stump(X, y):
    X, y = np.array(X, dtype=float), np.array(y, dtype=int)
    # All features and thresholds.
    return []

X = [[1, 9], [2, 8], [3, 1], [6, 2], [7, 9], [8, 1]]
y = [0, 0, 0, 1, 1, 1]
print(fit_stump(X, y))
