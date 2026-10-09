import numpy as np


def knn_predict(X, y, x, k):
    X, x = np.array(X, dtype=float), np.array(x, dtype=float)
    dist = np.sqrt(((X - x) ** 2).sum(axis=1))
    nearest = np.argsort(dist, kind="stable")[:k]
    votes = {}
    for i in nearest:
        votes[y[i]] = votes.get(y[i], 0) + 1
    return min(votes, key=lambda c: (-votes[c], c))

X = [[0, 0], [1, 0], [0, 1], [5, 5], [6, 5], [5, 6]]
y = [0, 0, 0, 1, 1, 1]
print(knn_predict(X, y, [0.5, 0.5], 3))
print(knn_predict(X, y, [4, 4], 3))
print(knn_predict(X, y, [3, 3], 6))
