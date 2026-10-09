import numpy as np


def train_logistic(X, y, lr, epochs):
    X, y = np.array(X, dtype=float), np.array(y, dtype=float)
    w, b = np.zeros(X.shape[1]), 0.0
    for _ in range(epochs):
        p = 1 / (1 + np.exp(-(X @ w + b)))
        w = w - lr * X.T @ (p - y) / len(y)
        b = b - lr * float(np.mean(p - y))
    return w.round(3).tolist(), round(b, 3)

X = [[0.0, 1.0], [1.0, 0.0], [1.0, 1.0], [0.0, 0.0]]
y = [1, 0, 1, 0]
w, b = train_logistic(X, y, 0.5, 200)
print(w)
print(b)
