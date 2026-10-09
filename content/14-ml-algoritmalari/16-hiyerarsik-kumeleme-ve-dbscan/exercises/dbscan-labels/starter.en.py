import numpy as np


def dbscan_labels(X, eps, min_samples):
    X = np.array(X, dtype=float)
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(axis=2))
    near = D <= eps
    core = near.sum(axis=1) >= min_samples
    labels = [-1] * len(X)
    # A new cluster from an unlabelled core point, grow with a stack
    return labels

X = [[0, 0], [0, 1], [1, 0], [1, 1], [2.5, 0.5],
     [6, 6], [6, 7], [7, 6], [7, 7], [12, 0]]
print(dbscan_labels(X, 1.6, 4))
