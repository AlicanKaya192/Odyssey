import numpy as np


def missing_and_mean(values):
    arr = np.array(values)
    return [0, float(arr.mean())]

print(missing_and_mean([3, None, 5]))
print(missing_and_mean([1, 2, 3]))
