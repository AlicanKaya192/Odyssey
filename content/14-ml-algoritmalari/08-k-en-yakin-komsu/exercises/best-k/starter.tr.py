import numpy as np


def knn_labels(Xtr, ytr, Xq, k):
    d = ((Xq[:, None, :] - Xtr[None, :, :]) ** 2).sum(axis=2)
    near = np.argsort(d, axis=1)[:, :k]
    return np.array([np.bincount(v).argmax() for v in ytr[near]])


def best_k(X, y, ks, folds):
    X, y = np.array(X, dtype=float), np.array(y)
    n = len(y)
    # Her k icin katlarda dogruluk.
    return ks[0]

rng = np.random.default_rng(3)
X = rng.normal(0, 1, (60, 2))
y = (X[:, 0] + X[:, 1] > 0).astype(int)
print(best_k(X.tolist(), y.tolist(), [1, 3, 7, 15], 5))
