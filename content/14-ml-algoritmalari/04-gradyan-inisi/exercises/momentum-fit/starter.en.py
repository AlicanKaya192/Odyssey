import numpy as np


def momentum_fit(A, y, lr, beta, steps):
    A, y = np.array(A, dtype=float), np.array(y, dtype=float)
    w = np.zeros(A.shape[1])
    v = np.zeros(A.shape[1])
    # Accumulate v, update w.
    return w.round(3).tolist()

A = [[1, 0.0], [1, 1.0], [1, 2.0], [1, 3.0]]
y = [1.0, 3.0, 5.0, 7.0]
print(momentum_fit(A, y, 0.02, 0.0, 50))
print(momentum_fit(A, y, 0.02, 0.9, 50))
