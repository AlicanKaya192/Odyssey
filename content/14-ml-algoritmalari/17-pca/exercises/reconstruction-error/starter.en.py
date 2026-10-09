import numpy as np


def reconstruction_error(X, k):
    X = np.array(X, dtype=float)
    Xc = X - X.mean(axis=0)
    C = Xc.T @ Xc / (len(X) - 1)
    vals, vecs = np.linalg.eigh(C)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    # Z = Xc @ V, rebuild, mean squared difference
    return 0.0

X = [[1, 2, 0], [2, 3, 1], [3, 5, 1], [4, 4, 2], [5, 7, 2]]
print(reconstruction_error(X, 1))
print(reconstruction_error(X, 2))
print(reconstruction_error(X, 3))
