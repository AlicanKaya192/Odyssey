import numpy as np


def ridge_fit(X, y, alpha):
    X, y = np.array(X, dtype=float), np.array(y, dtype=float)
    # Merkezle, coz, kesisimi bul.
    return []

X = [[1, 2], [2, 1], [3, 4], [4, 3], [5, 5]]
y = [9, 6, 17, 14, 21]
print(ridge_fit(X, y, 0.0))
print(ridge_fit(X, y, 10.0))
