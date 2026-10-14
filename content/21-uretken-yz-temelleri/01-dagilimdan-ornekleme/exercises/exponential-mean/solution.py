import numpy as np


def exponential_mean(rate, n, seed):
    u = np.random.default_rng(seed).random(n)
    waits = -np.log(1 - u) / rate
    return round(float(waits.mean()), 3)


print(exponential_mean(0.5, 10000, 1))
print(exponential_mean(2.0, 10000, 3))
