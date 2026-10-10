import numpy as np


def replace_first(names, new):
    arr = np.array(names)
    arr[0] = new
    return arr.tolist()

print(replace_first(["ab", "cde"], "hello"))
