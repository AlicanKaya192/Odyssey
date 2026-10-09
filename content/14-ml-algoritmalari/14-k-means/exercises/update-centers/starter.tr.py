import numpy as np


def update_centers(X, labels, k):
    X, labels = np.array(X, dtype=float), np.array(labels)
    # Her kume icin X[labels == j].mean(axis=0)
    return []

X = [[0, 0], [2, 2], [9, 9], [11, 7]]
print(update_centers(X, [0, 0, 1, 1], 2))
