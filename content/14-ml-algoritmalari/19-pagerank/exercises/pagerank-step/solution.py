import numpy as np


def pagerank_step(M, r, d):
    M, r = np.array(M, dtype=float), np.array(r, dtype=float)
    new = d * M @ r + (1 - d) / len(r)
    return new.round(4).tolist()

M = [[0, 0, 1], [0.5, 0, 0], [0.5, 1, 0]]
r = [1 / 3, 1 / 3, 1 / 3]
r = pagerank_step(M, r, 0.85)
print(r)
print(pagerank_step(M, r, 0.85))
