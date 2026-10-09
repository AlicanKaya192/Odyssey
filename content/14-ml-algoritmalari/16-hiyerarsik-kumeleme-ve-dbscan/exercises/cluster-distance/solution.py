import numpy as np


def cluster_distance(A, B, method):
    A, B = np.array(A, dtype=float), np.array(B, dtype=float)
    D = np.sqrt(((A[:, None] - B[None]) ** 2).sum(axis=2))
    if method == "single":
        d = D.min()
    elif method == "complete":
        d = D.max()
    else:
        d = D.mean()
    return round(float(d), 3)

A = [[0, 0], [0, 1]]
B = [[3, 0], [4, 1]]
for method in ("single", "complete", "average"):
    print(method, cluster_distance(A, B, method))
