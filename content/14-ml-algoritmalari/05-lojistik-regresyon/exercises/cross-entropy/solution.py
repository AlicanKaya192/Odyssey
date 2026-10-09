import numpy as np


def cross_entropy(y, p):
    y = np.array(y, dtype=float)
    p = np.clip(np.array(p, dtype=float), 1e-12, 1 - 1e-12)
    return round(float(-(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()), 4)

print(cross_entropy([1, 0, 1], [0.9, 0.2, 0.6]))
print(cross_entropy([0], [0.99]))
print(cross_entropy([1], [1.0]))
