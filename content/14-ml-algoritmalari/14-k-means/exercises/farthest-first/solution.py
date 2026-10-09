import numpy as np


def farthest_first(X, k):
    X = np.array(X, dtype=float)
    chosen = [0]
    while len(chosen) < k:
        C = X[chosen]
        d = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2).min(axis=1)
        chosen.append(int(d.argmax()))
    return chosen

X = [[0, 0], [1, 0], [10, 0], [5, 5], [0, 9], [9, 9]]
print(farthest_first(X, 3))
print(farthest_first(X, 4))
