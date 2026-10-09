import numpy as np


def soft_threshold(values, t):
    z = np.array(values, dtype=float)
    return (np.sign(z) * np.maximum(np.abs(z) - t, 0)).round(4).tolist()

print(soft_threshold([3.0, -0.5, 0.2, -2.0], 1.0))
