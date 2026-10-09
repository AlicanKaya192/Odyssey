import numpy as np


def fit_stump_reg(x, y):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    order = np.argsort(x)
    x, y = x[order], y[order]
    # The two sides' error for each cut.
    return None

x = [1, 2, 3, 4, 5, 6]
y = [1.0, 1.2, 0.9, 5.0, 5.2, 4.8]
print(fit_stump_reg(x, y))
