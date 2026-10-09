import numpy as np


def pagerank(links, d=0.85, tol=1e-10):
    n = len(links)
    M = np.zeros((n, n))
    for j in range(n):
        outs = links[j]
        if outs:
            for i in outs:
                M[i, j] = 1 / len(outs)
        else:
            M[:, j] = 1 / n
    r = np.full(n, 1 / n)
    steps = 0
    while True:
        steps += 1
        new = d * M @ r + (1 - d) / n
        if np.abs(new - r).sum() < tol:
            return new.round(3).tolist(), steps
        r = new

links = [[1, 2], [2], [0], [2]]
ranks, steps = pagerank(links)
print(ranks)
print(steps)
