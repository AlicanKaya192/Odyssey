import numpy as np


def assign_labels(X, centers):
    X, C = np.array(X, dtype=float), np.array(centers, dtype=float)
    # (n, k) kare uzakliklar, sonra argmin
    return []

X = [[0, 0], [1, 1], [9, 9], [10, 8], [4, 4]]
centers = [[0, 0], [10, 10]]
print(assign_labels(X, centers))
