import numpy as np


def fit_weights(X, y):
    X, y = np.array(X, dtype=float), np.array(y, dtype=float)
    A = np.column_stack([np.ones(len(X)), X])
    return np.linalg.solve(A.T @ A, A.T @ y).round(4).tolist()

X = [[1, 2], [2, 1], [3, 4], [4, 3], [5, 5]]
y = [9, 6, 17, 14, 21]
print(fit_weights(X, y))
