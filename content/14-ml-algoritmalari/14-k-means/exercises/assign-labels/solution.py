import numpy as np


def assign_labels(X, centers):
    X, C = np.array(X, dtype=float), np.array(centers, dtype=float)
    d = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)
    return d.argmin(axis=1).tolist()

X = [[0, 0], [1, 1], [9, 9], [10, 8], [4, 4]]
centers = [[0, 0], [10, 10]]
print(assign_labels(X, centers))
