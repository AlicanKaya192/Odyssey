import numpy as np


def safe_sqrt(values):
    v = np.array(values, dtype=float)
    result = np.full(len(v), -1.0)
    np.sqrt(v, where=v >= 0, out=result)
    return result.tolist()

print(safe_sqrt([4, -1, 9, -16, 0]))
