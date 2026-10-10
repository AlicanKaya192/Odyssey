import numpy as np


def safe_sqrt(values):
    v = np.array(values, dtype=float)
    return np.sqrt(np.abs(v)).tolist()

print(safe_sqrt([4, -1, 9, -16, 0]))
