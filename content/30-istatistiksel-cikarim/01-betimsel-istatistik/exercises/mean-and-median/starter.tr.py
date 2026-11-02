import numpy as np


def center(values):
    mean = round(float(np.mean(values)), 2)
    return [mean, mean]


print(center([4, 1, 3, 2, 100]))
print(center([2, 4, 6, 8]))
