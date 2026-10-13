import numpy as np


def energy(matrix, k):
    S = np.linalg.svd(np.array(matrix, dtype=float), compute_uv=False)
    return round(float((S[:k] ** 2).sum() / (S ** 2).sum()), 3)

M = [[3, 1, 0], [1, 3, 0], [0, 0, 1]]
for k in [1, 2, 3]:
    print(k, energy(M, k))
