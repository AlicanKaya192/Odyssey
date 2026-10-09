import numpy as np


def gini(y):
    if len(y) == 0:
        return 0.0
    p = np.bincount(y) / len(y)
    return 1 - (p ** 2).sum()


def split_gini(x, y, t):
    x, y = np.array(x, dtype=float), np.array(y, dtype=int)
    left = x <= t
    # The weighted average.
    return 0.0

x = [1, 2, 3, 4, 5, 6]
y = [0, 0, 0, 1, 1, 0]
for t in (1.5, 3.5, 5.5):
    print(t, split_gini(x, y, t))
