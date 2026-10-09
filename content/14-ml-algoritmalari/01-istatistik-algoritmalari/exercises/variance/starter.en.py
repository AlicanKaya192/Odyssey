import numpy as np


def variance(values):
    n = len(values)
    # Pass 1: the mean.  Pass 2: squared deviations.
    return 0.0

print(variance([2, 4, 4, 4, 5, 5, 7, 9]))
rng = np.random.default_rng(1)
x = (1e9 + rng.normal(0, 1, size=50_000)).tolist()
print(variance(x))
