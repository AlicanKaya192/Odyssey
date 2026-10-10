import numpy as np


def center_columns(matrix):
    X = np.array(matrix, dtype=float)
    return (X - X.mean()).round(2).tolist()

print(center_columns([[1, 10], [3, 20], [5, 60]]))
