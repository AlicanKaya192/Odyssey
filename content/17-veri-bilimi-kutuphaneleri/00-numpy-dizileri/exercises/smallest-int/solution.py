import numpy as np


def smallest_int(values):
    low, high = min(values), max(values)
    for kind in (np.int8, np.int16, np.int32, np.int64):
        info = np.iinfo(kind)
        if low >= info.min and high <= info.max:
            return np.dtype(kind).name
    return "int64"

print(smallest_int([0, 100]), smallest_int([-200, 5]), smallest_int([0, 40_000]))
