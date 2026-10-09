import numpy as np


def sq_distances(A, B):
    A, B = np.array(A, dtype=float), np.array(B, dtype=float)
    return ((A[:, None, :] - B[None, :, :]) ** 2).sum(axis=2).round(4).tolist()

print(sq_distances([[0, 0], [1, 1]], [[1, 0], [3, 4], [0, 0]]))
