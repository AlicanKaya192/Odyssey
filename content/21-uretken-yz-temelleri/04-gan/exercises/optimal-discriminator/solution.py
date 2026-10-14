import numpy as np


def density(x, m, s):
    return np.exp(-(x - m) ** 2 / (2 * s ** 2)) / (s * np.sqrt(2 * np.pi))


def optimal_d(xs, mu_g, sd_g):
    xs = np.array(xs)
    p_data = density(xs, 0.0, 1.0)
    p_g = density(xs, mu_g, sd_g)
    return [round(float(v), 3) for v in p_data / (p_data + p_g)]


print(optimal_d([0.0, 1.0, 2.0], 0.0, 1.0))
print(optimal_d([0.0, 1.0, 2.0], 2.0, 1.0))
