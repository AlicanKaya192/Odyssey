import numpy as np


def principal_axes(X):
    X = np.array(X, dtype=float)
    Xc = X - X.mean(axis=0)
    C = Xc.T @ Xc / (len(X) - 1)
    # np.linalg.eigh, sorting, the sign
    return [], []

X = [[1, 2], [2, 3], [3, 5], [4, 4], [5, 7]]
vals, first = principal_axes(X)
print(vals)
print(first)
