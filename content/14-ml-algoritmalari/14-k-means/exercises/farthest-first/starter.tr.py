import numpy as np


def farthest_first(X, k):
    X = np.array(X, dtype=float)
    chosen = [0]
    # En yakin secilmise uzaklik, sonra argmax
    return chosen

X = [[0, 0], [1, 0], [10, 0], [5, 5], [0, 9], [9, 9]]
print(farthest_first(X, 3))
print(farthest_first(X, 4))
