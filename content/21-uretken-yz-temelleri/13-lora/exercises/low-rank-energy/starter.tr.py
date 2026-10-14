import numpy as np


def energy(matrix, r):
    return 0.0


M = [[3, 0, 0], [0, 1, 0], [0, 0, 0.5]]
for r in [1, 2, 3]:
    print(r, energy(M, r))
