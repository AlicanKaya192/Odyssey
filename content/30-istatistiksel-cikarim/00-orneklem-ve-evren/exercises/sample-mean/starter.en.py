import numpy as np


def sample_mean(values, n, seed):
    return round(float(np.mean(values)), 2)


values = list(range(1, 21))
print(sample_mean(values, 5, 0))
print(sample_mean(values, 5, 1))
print(sample_mean(values, 20, 0))
