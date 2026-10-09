import numpy as np


def knn_predict(X, y, x, k):
    X, x = np.array(X, dtype=float), np.array(x, dtype=float)
    dist = np.sqrt(((X - x) ** 2).sum(axis=1))
    # The k nearest, then the vote
    return 0

X = [[0, 0], [1, 0], [0, 1], [5, 5], [6, 5], [5, 6]]
y = [0, 0, 0, 1, 1, 1]
print(knn_predict(X, y, [0.5, 0.5], 3))
print(knn_predict(X, y, [4, 4], 3))
print(knn_predict(X, y, [3, 3], 6))
