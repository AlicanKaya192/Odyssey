import numpy as np


def ppmi(counts):
    M = np.array(counts, dtype=float)
    total = M.sum()
    expected = np.outer(M.sum(axis=1), M.sum(axis=0)) / total ** 2
    with np.errstate(divide="ignore"):
        P = np.log((M / total) / expected)
    return np.maximum(P, 0).round(3).tolist()

counts = [[0, 4, 1],
          [4, 0, 2],
          [1, 2, 0]]
for row in ppmi(counts):
    print(row)
