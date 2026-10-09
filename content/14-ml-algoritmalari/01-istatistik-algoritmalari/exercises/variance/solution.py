import numpy as np


def variance(values):
    n = len(values)
    mean = sum(values) / n
    return round(sum((v - mean) ** 2 for v in values) / n, 4)

print(variance([2, 4, 4, 4, 5, 5, 7, 9]))
rng = np.random.default_rng(1)
x = (1e9 + rng.normal(0, 1, size=50_000)).tolist()
print(variance(x))
