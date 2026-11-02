import numpy as np


def variation(values):
    return round(float(np.std(values, ddof=1)), 3)


print(variation([0, 0, 0, 100]))
print(variation([10, 12, 11, 9]))
