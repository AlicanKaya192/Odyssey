import numpy as np


def covariance_matrix(X):
    X = np.array(X, dtype=float)
    Xc = X - X.mean(axis=0)
    C = Xc.T @ Xc / (len(X) - 1)
    return C.round(3).tolist()

X = [[1, 2], [2, 3], [3, 5], [4, 4], [5, 7]]
C = covariance_matrix(X)
print(C[0])
print(C[1])
