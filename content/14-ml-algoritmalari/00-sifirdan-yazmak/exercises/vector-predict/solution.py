import numpy as np


def predict(X, w, b):
    X = np.array(X, dtype=float)
    w = np.array(w, dtype=float)
    return (X @ w + b).round(3).tolist()

X = [[1, 2, 3], [0, 1, 0], [2, 0, 1]]
print(predict(X, [0.5, -2.0, 1.0], 0.25))
rng = np.random.default_rng(3)
big = rng.normal(size=(200_000, 4)).tolist()
print(sum(predict(big, [1, 2, 3, 4], 0.0)) / len(big))
