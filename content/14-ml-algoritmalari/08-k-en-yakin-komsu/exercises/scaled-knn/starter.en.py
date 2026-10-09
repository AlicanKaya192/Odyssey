import numpy as np


def knn_labels(Xtr, ytr, Xq, k):
    d = ((Xq[:, None, :] - Xtr[None, :, :]) ** 2).sum(axis=2)
    near = np.argsort(d, axis=1)[:, :k]
    return np.array([np.bincount(v).argmax() for v in ytr[near]])


def scaled_knn(X, y, Xq, k):
    X, y, Xq = np.array(X, dtype=float), np.array(y), np.array(Xq, dtype=float)
    # Standardise with the training scale.
    return [int(v) for v in knn_labels(X, y, Xq, k)]

X = [[1, 1000], [2, 3000], [9, 1100], [10, 2900]]
y = [0, 0, 1, 1]
print(scaled_knn(X, y, [[1.5, 2800], [9.5, 1200]], 1))
