import numpy as np


def knn_labels(Xtr, ytr, Xq, k):
    d = ((Xq[:, None, :] - Xtr[None, :, :]) ** 2).sum(axis=2)
    near = np.argsort(d, axis=1)[:, :k]
    return np.array([np.bincount(v).argmax() for v in ytr[near]])


def best_k(X, y, ks, folds):
    X, y = np.array(X, dtype=float), np.array(y)
    n = len(y)
    best, best_acc = None, -1.0
    for k in sorted(ks):
        accs = []
        for test in np.array_split(np.arange(n), folds):
            train = np.setdiff1d(np.arange(n), test)
            accs.append((knn_labels(X[train], y[train], X[test], k) == y[test]).mean())
        if np.mean(accs) > best_acc:
            best, best_acc = k, np.mean(accs)
    return best

rng = np.random.default_rng(3)
X = rng.normal(0, 1, (60, 2))
y = (X[:, 0] + X[:, 1] > 0).astype(int)
print(best_k(X.tolist(), y.tolist(), [1, 3, 7, 15], 5))
