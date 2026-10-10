import numpy as np


def distances(points):
    P = np.array(points, dtype=float)
    diff = P[:, None, :] - P[None, :, :]
    return np.sqrt((diff ** 2).sum(axis=-1)).round(2).tolist()

for row in distances([[0, 0], [3, 4], [6, 8]]):
    print(row)
