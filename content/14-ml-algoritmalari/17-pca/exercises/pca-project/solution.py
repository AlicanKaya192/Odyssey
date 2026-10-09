import numpy as np


def pca_project(X, k):
    X = np.array(X, dtype=float)
    Xc = X - X.mean(axis=0)
    C = Xc.T @ Xc / (len(X) - 1)
    vals, vecs = np.linalg.eigh(C)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    for j in range(vecs.shape[1]):
        if vecs[np.argmax(np.abs(vecs[:, j])), j] < 0:
            vecs[:, j] = -vecs[:, j]
    return (Xc @ vecs[:, :k]).round(3).tolist()

X = [[1, 2], [2, 3], [3, 5], [4, 4], [5, 7]]
for row in pca_project(X, 1):
    print(row)
