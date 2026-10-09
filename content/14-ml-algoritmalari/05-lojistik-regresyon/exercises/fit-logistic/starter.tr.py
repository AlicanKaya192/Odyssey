import numpy as np


def fit_logistic(A, y, lr, steps):
    A, y = np.array(A, dtype=float), np.array(y, dtype=float)
    w = np.zeros(A.shape[1])
    # steps kez gradyan adimi.
    return w.round(3).tolist()

A = [[1, -2.0], [1, -1.0], [1, -0.5], [1, 0.5], [1, 1.0], [1, 2.0]]
y = [0, 0, 1, 0, 1, 1]
print(fit_logistic(A, y, 0.5, 2000))
