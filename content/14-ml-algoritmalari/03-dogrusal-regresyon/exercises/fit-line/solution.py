import numpy as np


def fit_line(x, y):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    dx, dy = x - x.mean(), y - y.mean()
    slope = (dx @ dy) / (dx @ dx)
    intercept = y.mean() - slope * x.mean()
    return round(float(intercept), 4), round(float(slope), 4)

print(fit_line([1, 2, 3, 4, 5], [2.1, 3.9, 6.2, 7.8, 10.1]))
print(fit_line([0, 1, 2], [5, 5, 5]))
