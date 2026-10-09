import numpy as np


def kernel_matrix(X, degree):
    X = np.array(X, dtype=float)
    return ((X @ X.T + 1) ** degree).round(3).tolist()

X = [[1, 0], [0, 1], [1, 1]]
K = kernel_matrix(X, 2)
print(K[0])
print(K[1])
print(K[2])
