import numpy as np


def region_query(X, i, eps):
    X = np.array(X, dtype=float)
    dist = np.sqrt(((X - X[i]) ** 2).sum(axis=1))
    return np.where(dist <= eps)[0].tolist()

X = [[0, 0], [0.5, 0], [1.2, 0], [3, 3]]
print(region_query(X, 0, 1.0))
print(region_query(X, 1, 1.0))
print(region_query(X, 3, 1.0))
