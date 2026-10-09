import numpy as np


def normal_pdf(x, mu, var):
    return np.exp(-(x - mu) ** 2 / (2 * var)) / np.sqrt(2 * np.pi * var)


def responsibilities(xs, weights, mus, variances):
    xs, w = np.array(xs, dtype=float), np.array(weights, dtype=float)
    mu, var = np.array(mus, dtype=float), np.array(variances, dtype=float)
    # share * density, divide by the row sum
    return []

r = responsibilities([-1.0, 2.0, 6.0], [0.6, 0.4], [0.0, 4.0], [1.0, 2.25])
for row in r:
    print(row)
