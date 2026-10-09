import numpy as np


def soft_threshold(values, t):
    z = np.array(values, dtype=float)
    # sign(z) * max(|z| - t, 0)
    return z.round(4).tolist()

print(soft_threshold([3.0, -0.5, 0.2, -2.0], 1.0))
