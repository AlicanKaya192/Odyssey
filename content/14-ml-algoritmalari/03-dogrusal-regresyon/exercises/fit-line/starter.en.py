import numpy as np


def fit_line(x, y):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    # Deviations, slope, intercept.
    return 0.0, 0.0

print(fit_line([1, 2, 3, 4, 5], [2.1, 3.9, 6.2, 7.8, 10.1]))
print(fit_line([0, 1, 2], [5, 5, 5]))
