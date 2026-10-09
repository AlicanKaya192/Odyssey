import numpy as np


def cross_entropy(y, p):
    y = np.array(y, dtype=float)
    p = np.clip(np.array(p, dtype=float), 1e-12, 1 - 1e-12)
    # Log kaybi.
    return 0.0

print(cross_entropy([1, 0, 1], [0.9, 0.2, 0.6]))
print(cross_entropy([0], [0.99]))
print(cross_entropy([1], [1.0]))
