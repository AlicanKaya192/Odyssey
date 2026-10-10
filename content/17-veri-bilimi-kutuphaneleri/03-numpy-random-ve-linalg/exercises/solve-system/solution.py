import numpy as np


def solve(A, b):
    try:
        x = np.linalg.solve(np.array(A, dtype=float), np.array(b, dtype=float))
    except np.linalg.LinAlgError:
        return "singular"
    return x.round(3).tolist()

print(solve([[2, 1], [1, 3]], [3, 5]))
print(solve([[1, 2], [2, 4]], [1, 2]))
