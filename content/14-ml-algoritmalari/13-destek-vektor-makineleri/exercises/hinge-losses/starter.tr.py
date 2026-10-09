import numpy as np


def hinge_losses(y, scores):
    y, s = np.array(y, dtype=float), np.array(scores, dtype=float)
    # max(0, 1 - y * s)
    return []

print(hinge_losses([1, -1, 1, -1], [2.0, -0.5, 0.3, 1.2]))
