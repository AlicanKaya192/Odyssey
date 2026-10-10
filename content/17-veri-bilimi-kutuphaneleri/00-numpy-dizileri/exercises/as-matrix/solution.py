import numpy as np


def as_matrix(values, cols):
    try:
        return np.array(values).reshape(-1, cols).tolist()
    except ValueError:
        return "error"

print(as_matrix([1, 2, 3, 4, 5, 6], 2))
print(as_matrix([1, 2, 3, 4, 5], 2))
