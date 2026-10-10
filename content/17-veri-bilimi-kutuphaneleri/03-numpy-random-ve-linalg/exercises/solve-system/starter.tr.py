import numpy as np


def solve(A, b):
    return (np.array(b) / np.array(A).sum(axis=1)).round(3).tolist()

print(solve([[2, 1], [1, 3]], [3, 5]))
print(solve([[1, 2], [2, 4]], [1, 2]))
