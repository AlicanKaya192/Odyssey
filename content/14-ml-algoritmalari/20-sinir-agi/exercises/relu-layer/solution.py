import numpy as np


def relu_layer(X, W, b):
    X, W, b = (np.array(a, dtype=float) for a in (X, W, b))
    return np.maximum(0, X @ W + b).round(3).tolist()

X = [[1.0, -2.0], [0.5, 0.5]]
W = [[1.0, -1.0, 0.5], [2.0, 0.0, -1.0]]
for row in relu_layer(X, W, [0.0, 1.0, 0.0]):
    print(row)
