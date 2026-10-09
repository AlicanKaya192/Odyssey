import numpy as np


def gini(y):
    if len(y) == 0:
        return 0.0
    p = np.bincount(y) / len(y)
    return 1 - (p ** 2).sum()


def best_threshold(x, y):
    x, y = np.array(x, dtype=float), np.array(y, dtype=int)
    values = np.unique(x)
    # Orta noktalari dene.
    return None, None

print(best_threshold([1, 2, 3, 4, 5, 6], [0, 0, 0, 1, 1, 1]))
print(best_threshold([3, 1, 2, 5, 4], [1, 0, 0, 1, 1]))
