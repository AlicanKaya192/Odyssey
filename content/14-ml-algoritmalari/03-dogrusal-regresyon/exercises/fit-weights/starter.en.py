import numpy as np


def fit_weights(X, y):
    X, y = np.array(X, dtype=float), np.array(y, dtype=float)
    # A = [1, X]; the normal equation.
    return []

X = [[1, 2], [2, 1], [3, 4], [4, 3], [5, 5]]
y = [9, 6, 17, 14, 21]
print(fit_weights(X, y))
