import numpy as np


def knn_regress(X, y, Xq, k):
    X, y, Xq = np.array(X, dtype=float), np.array(y, dtype=float), np.array(Xq, dtype=float)
    d = ((Xq[:, None, :] - X[None, :, :]) ** 2).sum(axis=2)
    near = np.argsort(d, axis=1)[:, :k]
    return [round(float(v), 3) for v in y[near].mean(axis=1)]

X = [[1], [2], [3], [10], [11]]
y = [1.0, 2.0, 3.0, 10.0, 11.0]
print(knn_regress(X, y, [[2.2], [10.4]], 2))
