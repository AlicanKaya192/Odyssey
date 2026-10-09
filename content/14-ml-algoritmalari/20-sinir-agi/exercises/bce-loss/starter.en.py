import numpy as np


def bce_loss(y, p):
    y, p = np.array(y, dtype=float), np.array(p, dtype=float)
    # Clip, then the formula
    return 0.0

print(bce_loss([1, 0, 1], [0.9, 0.2, 0.6]))
print(bce_loss([0, 1], [0.0, 1.0]))
