import numpy as np


def as_matrix(values, cols):
    return np.array(values).reshape(cols, -1).tolist()

print(as_matrix([1, 2, 3, 4, 5, 6], 2))
print(as_matrix([1, 2, 3, 4, 5], 2))
