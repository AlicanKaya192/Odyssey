import numpy as np


def point_types(X, eps, min_samples):
    X = np.array(X, dtype=float)
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(axis=2))
    near = D <= eps
    # First the core points, then the borders
    return []

X = [[0, 0], [0, 1], [1, 0], [1, 1], [2.5, 0.5], [6, 6]]
for i, kind in enumerate(point_types(X, 1.6, 4)):
    print(i, kind)
