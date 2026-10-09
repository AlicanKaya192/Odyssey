import numpy as np


def gauss_loglik(x, mean, var):
    x, mean, var = np.array(x, dtype=float), np.array(mean, dtype=float), np.array(var, dtype=float)
    return round(float((-0.5 * np.log(2 * np.pi * var) - (x - mean) ** 2 / (2 * var)).sum()), 4)

print(gauss_loglik([1.0, 2.0], [0.0, 2.0], [1.0, 4.0]))
