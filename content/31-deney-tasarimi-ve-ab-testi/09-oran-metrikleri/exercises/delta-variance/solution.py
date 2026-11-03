import numpy as np


def delta_var(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    r = y.mean() / x.mean()
    var = y.var(ddof=1) - 2 * r * np.cov(x, y)[0, 1] + r ** 2 * x.var(ddof=1)
    return round(float(var / (len(x) * x.mean() ** 2)), 6)


print(delta_var([3, 5, 2, 8, 6], [1, 0, 0, 2, 1]))
