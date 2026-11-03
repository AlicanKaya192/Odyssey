import numpy as np


def cuped_adjust(y, x):
    y, x = np.asarray(y, float), np.asarray(x, float)
    theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
    return [round(float(v), 3) for v in y - theta * x]


print(cuped_adjust([5, 7, 9, 12], [1, 2, 3, 4]))
