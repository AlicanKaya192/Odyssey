import numpy as np


def knn_classify(X, y, Xq, k):
    X, y, Xq = np.array(X, dtype=float), np.array(y), np.array(Xq, dtype=float)
    d = ((Xq[:, None, :] - X[None, :, :]) ** 2).sum(axis=2)
    near = np.argsort(d, axis=1)[:, :k]
    return [int(np.bincount(v).argmax()) for v in y[near]]

X = [[0, 0], [0, 1], [1, 0], [5, 5], [5, 6], [6, 5]]
y = [0, 0, 0, 1, 1, 1]
print(knn_classify(X, y, [[0.5, 0.5], [5.5, 5.2], [3, 3]], 3))
