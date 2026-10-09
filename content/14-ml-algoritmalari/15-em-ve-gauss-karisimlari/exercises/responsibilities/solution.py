import numpy as np


def normal_pdf(x, mu, var):
    return np.exp(-(x - mu) ** 2 / (2 * var)) / np.sqrt(2 * np.pi * var)


def responsibilities(xs, weights, mus, variances):
    xs, w = np.array(xs, dtype=float), np.array(weights, dtype=float)
    mu, var = np.array(mus, dtype=float), np.array(variances, dtype=float)
    dens = w * normal_pdf(xs[:, None], mu, var)
    r = dens / dens.sum(axis=1, keepdims=True)
    return r.round(3).tolist()

r = responsibilities([-1.0, 2.0, 6.0], [0.6, 0.4], [0.0, 4.0], [1.0, 2.25])
for row in r:
    print(row)
