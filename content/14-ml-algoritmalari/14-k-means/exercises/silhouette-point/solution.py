import numpy as np


def silhouette_point(X, labels, i):
    X, labels = np.array(X, dtype=float), np.array(labels)
    dist = np.sqrt(((X - X[i]) ** 2).sum(axis=1))
    own = labels == labels[i]
    a = dist[own].sum() / (own.sum() - 1)
    others = set(labels.tolist()) - {int(labels[i])}
    b = min(dist[labels == c].mean() for c in others)
    return round(float((b - a) / max(a, b)), 3)

X = [[0, 0], [0, 1], [1, 0], [5, 5], [5, 6], [6, 5]]
labels = [0, 0, 0, 1, 1, 1]
print(silhouette_point(X, labels, 0))
print(silhouette_point(X, labels, 3))
