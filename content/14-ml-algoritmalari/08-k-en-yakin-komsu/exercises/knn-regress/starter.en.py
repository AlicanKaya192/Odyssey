import numpy as np


def knn_regress(X, y, Xq, k):
    X, y, Xq = np.array(X, dtype=float), np.array(y, dtype=float), np.array(Xq, dtype=float)
    # The mean of the nearest k targets.
    return []

X = [[1], [2], [3], [10], [11]]
y = [1.0, 2.0, 3.0, 10.0, 11.0]
print(knn_regress(X, y, [[2.2], [10.4]], 2))
