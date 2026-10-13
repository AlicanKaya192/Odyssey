import numpy as np


def energy(matrix, k):
    return 0.0

M = [[3, 1, 0], [1, 3, 0], [0, 0, 1]]
for k in [1, 2, 3]:
    print(k, energy(M, k))
