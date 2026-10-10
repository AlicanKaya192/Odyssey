import numpy as np


def distances(points):
    P = np.array(points, dtype=float)
    # P[:, None, :] - P[None, :, :]
    return []

print(*distances([[0, 0], [3, 4], [6, 8]]), sep="\n")
