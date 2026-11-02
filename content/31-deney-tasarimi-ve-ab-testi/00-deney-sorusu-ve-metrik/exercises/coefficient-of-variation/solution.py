import numpy as np


def variation(values):
    values = np.array(values, dtype=float)
    return round(float(values.std(ddof=1) / values.mean()), 3)


print(variation([0, 0, 0, 100]))
print(variation([10, 12, 11, 9]))
