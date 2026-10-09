import numpy as np


def covariance_matrix(X):
    X = np.array(X, dtype=float)
    # Centre, then Xc.T @ Xc / (n - 1)
    return []

X = [[1, 2], [2, 3], [3, 5], [4, 4], [5, 7]]
C = covariance_matrix(X)
print(C[0])
print(C[1])
