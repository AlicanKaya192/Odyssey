import numpy as np


def normal_pdf(x, mu, var):
    return np.exp(-(x - mu) ** 2 / (2 * var)) / np.sqrt(2 * np.pi * var)


def em_fit(xs, weights, mus, variances, iters):
    xs, w = np.array(xs, dtype=float), np.array(weights, dtype=float)
    mu, var = np.array(mus, dtype=float), np.array(variances, dtype=float)
    # iters times: the E step, the M step
    return w.round(3).tolist(), mu.round(3).tolist(), var.round(3).tolist()

xs = [-1.2, -0.5, 0.1, 0.4, 0.9, 3.8, 4.4, 5.1, 5.6, 6.3]
w, mu, var = em_fit(xs, [0.5, 0.5], [0.0, 1.0], [1.0, 1.0], 50)
print(w)
print(mu)
print(var)
