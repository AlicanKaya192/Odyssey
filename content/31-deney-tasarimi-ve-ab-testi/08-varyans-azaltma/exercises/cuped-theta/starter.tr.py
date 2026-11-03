import numpy as np


def cuped_theta(x, y):
    return round(float(np.cov(x, y)[0, 1] / np.var(y, ddof=1)), 4)


print(cuped_theta([1, 2, 3, 4], [2, 4, 6, 9]))
