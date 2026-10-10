import numpy as np


def cap_above(values, limit):
    arr = np.array(values)
    arr[arr > limit][:] = limit
    return arr.tolist()

print(cap_above([5, 12, 7, 30], 10))
