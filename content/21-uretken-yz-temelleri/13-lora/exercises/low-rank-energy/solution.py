import numpy as np


def energy(matrix, r):
    S = np.linalg.svd(np.array(matrix, dtype=float), compute_uv=False)
    return round(float((S[:r] ** 2).sum() / (S ** 2).sum()), 3)


M = [[3, 0, 0], [0, 1, 0], [0, 0, 0.5]]
for r in [1, 2, 3]:
    print(r, energy(M, r))
