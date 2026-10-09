import numpy as np


def pagerank_exact(M, d):
    M = np.array(M, dtype=float)
    n = len(M)
    A = np.eye(n) - d * M
    b = np.full(n, (1 - d) / n)
    return np.linalg.solve(A, b).round(3).tolist()

M = [[0, 0, 1], [0.5, 0, 0], [0.5, 1, 0]]
print(pagerank_exact(M, 0.85))
print(pagerank_exact(M, 0.5))
