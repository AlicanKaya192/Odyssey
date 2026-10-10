import numpy as np


def column(matrix, j):
    return np.array(matrix)[:, j].tolist()

print(column([[1, 2, 3], [4, 5, 6]], 1))
