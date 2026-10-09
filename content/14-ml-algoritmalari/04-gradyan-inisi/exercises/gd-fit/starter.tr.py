import numpy as np


def gd_fit(A, y, lr, steps):
    A, y = np.array(A, dtype=float), np.array(y, dtype=float)
    w = np.zeros(A.shape[1])
    # steps kez adim.
    return w.round(3).tolist()

A = [[1, 0.0], [1, 1.0], [1, 2.0], [1, 3.0]]
y = [1.0, 3.0, 5.0, 7.0]
print(gd_fit(A, y, 0.1, 500))
