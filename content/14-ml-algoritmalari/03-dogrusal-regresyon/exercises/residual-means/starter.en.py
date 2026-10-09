import numpy as np


def residual_means(x, y, parts):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    order = np.argsort(x)
    x, y = x[order], y[order]
    # Line, residuals, the parts' means.
    return []

x = [0, 1, 2, 3, 4, 5, 6, 7, 8]
y = [v * v for v in x]
print(residual_means(x, y, 3))
