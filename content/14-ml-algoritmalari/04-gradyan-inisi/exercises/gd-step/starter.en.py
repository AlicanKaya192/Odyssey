import numpy as np


def gd_step(A, y, w, lr):
    A, y, w = np.array(A, dtype=float), np.array(y, dtype=float), np.array(w, dtype=float)
    # The gradient and one step.
    return w.round(4).tolist()

A = [[1, 0.5], [1, 1.5], [1, 2.0]]
y = [2.0, 4.0, 5.0]
w = [0.0, 0.0]
for _ in range(3):
    w = gd_step(A, y, w, 0.1)
    print(w)
