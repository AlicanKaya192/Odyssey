import numpy as np


def logistic_grad(A, y, w):
    A, y, w = np.array(A, dtype=float), np.array(y, dtype=float), np.array(w, dtype=float)
    p = 1 / (1 + np.exp(-(A @ w)))
    return (A.T @ (p - y) / len(y)).round(4).tolist()

A = [[1, 0.5], [1, -1.0], [1, 2.0]]
y = [1, 0, 1]
print(logistic_grad(A, y, [0.0, 0.0]))
print(logistic_grad(A, y, [0.2, 1.5]))
