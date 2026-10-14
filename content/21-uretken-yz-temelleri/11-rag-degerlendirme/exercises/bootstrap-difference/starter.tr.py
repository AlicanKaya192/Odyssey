import numpy as np


def bootstrap(a, b, n, seed):
    return [0, 0.0, 0.0]


a = [1, 1, 0, 1, 1, 0, 1, 1]
b = [1, 0, 0, 1, 1, 0, 1, 0]
print(bootstrap(a, b, 2000, 0))
