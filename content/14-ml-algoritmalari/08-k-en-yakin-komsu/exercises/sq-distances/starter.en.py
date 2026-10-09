import numpy as np


def sq_distances(A, B):
    A, B = np.array(A, dtype=float), np.array(B, dtype=float)
    # Differences by broadcasting, sum of squares on the last axis.
    return []

print(sq_distances([[0, 0], [1, 1]], [[1, 0], [3, 4], [0, 0]]))
