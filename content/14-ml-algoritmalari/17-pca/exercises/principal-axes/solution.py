import numpy as np


def principal_axes(X):
    X = np.array(X, dtype=float)
    Xc = X - X.mean(axis=0)
    C = Xc.T @ Xc / (len(X) - 1)
    vals, vecs = np.linalg.eigh(C)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    v = vecs[:, 0]
    if v[np.argmax(np.abs(v))] < 0:
        v = -v
    return vals.round(3).tolist(), v.round(3).tolist()

X = [[1, 2], [2, 3], [3, 5], [4, 4], [5, 7]]
vals, first = principal_axes(X)
print(vals)
print(first)
