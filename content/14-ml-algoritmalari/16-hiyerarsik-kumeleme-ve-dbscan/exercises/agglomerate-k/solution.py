import numpy as np


def agglomerate_k(X, k):
    X = np.array(X, dtype=float)
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(axis=2))
    clusters = [[i] for i in range(len(X))]
    while len(clusters) > k:
        best = None
        for a in range(len(clusters)):
            for b in range(a + 1, len(clusters)):
                d = D[np.ix_(clusters[a], clusters[b])].min()
                if best is None or d < best[0]:
                    best = (d, a, b)
        _, a, b = best
        clusters[a] = clusters[a] + clusters.pop(b)
    owner = {}
    for c, members in enumerate(clusters):
        for i in members:
            owner[i] = c
    names = {}
    return [names.setdefault(owner[i], len(names)) for i in range(len(X))]

X = [[0, 0], [0, 1], [5, 5], [5, 6], [10, 0], [10, 1]]
print(agglomerate_k(X, 3))
print(agglomerate_k(X, 2))
