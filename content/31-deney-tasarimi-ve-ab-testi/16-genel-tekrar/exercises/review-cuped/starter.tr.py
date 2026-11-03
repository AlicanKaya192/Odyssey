import numpy as np


def variance_left(x, y):
    rho = np.corrcoef(x, y)[0, 1]
    return round(float(1 - rho), 3)


print(variance_left([1, 2, 3, 4, 5], [2, 4, 5, 4, 6]))
