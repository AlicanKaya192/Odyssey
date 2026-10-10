import numpy as np


def row_shares(matrix):
    X = np.array(matrix, dtype=float)
    return (X / X.sum(axis=1, keepdims=True)).round(3).tolist()

print(row_shares([[1, 3], [2, 2]]))
