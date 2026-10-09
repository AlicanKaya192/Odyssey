import numpy as np


def agglomerate_k(X, k):
    X = np.array(X, dtype=float)
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(axis=2))
    clusters = [[i] for i in range(len(X))]
    # Merge the two closest clusters (single: min of the D block)
    return []

X = [[0, 0], [0, 1], [5, 5], [5, 6], [10, 0], [10, 1]]
print(agglomerate_k(X, 3))
print(agglomerate_k(X, 2))
