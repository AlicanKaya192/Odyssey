import numpy as np


def bce_loss(y, p):
    y, p = np.array(y, dtype=float), np.array(p, dtype=float)
    p = np.clip(p, 1e-12, 1 - 1e-12)
    loss = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
    return round(abs(float(loss)), 4)

print(bce_loss([1, 0, 1], [0.9, 0.2, 0.6]))
print(bce_loss([0, 1], [0.0, 1.0]))
