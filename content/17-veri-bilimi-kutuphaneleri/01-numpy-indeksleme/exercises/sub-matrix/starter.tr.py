import numpy as np


def sub_matrix(matrix, rows, cols):
    return np.array(matrix)[rows, cols].tolist()

grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
print(sub_matrix(grid, [0, 2], [1, 3]))
