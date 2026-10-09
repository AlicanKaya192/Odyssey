import numpy as np


def backprop_w1(X, y, W1, b1, W2, b2):
    X, W1, W2 = (np.array(a, dtype=float) for a in (X, W1, W2))
    b1, b2 = np.array(b1, dtype=float), np.array(b2, dtype=float)
    y = np.array(y, dtype=float)
    H = np.tanh(X @ W1 + b1)
    p = (1 / (1 + np.exp(-(H @ W2 + b2)))).ravel()
    dz2 = (p - y)[:, None] / len(y)
    dz1 = (dz2 @ W2.T) * (1 - H ** 2)
    return (X.T @ dz1).round(4).tolist()

X = [[0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
y = [1, 1, 0]
W1 = [[0.5, -0.5], [0.3, 0.8]]
W2 = [[1.0], [-1.0]]
for row in backprop_w1(X, y, W1, [0.0, 0.0], W2, [0.0]):
    print(row)
