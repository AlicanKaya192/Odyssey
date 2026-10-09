import numpy as np


def pagerank(links, d=0.85, tol=1e-10):
    n = len(links)
    M = np.zeros((n, n))
    # Build the matrix, then iterate
    return [], 0

links = [[1, 2], [2], [0], [2]]
ranks, steps = pagerank(links)
print(ranks)
print(steps)
