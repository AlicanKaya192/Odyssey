import numpy as np


def r2(y, p):
    y, p = np.array(y, dtype=float), np.array(p, dtype=float)
    # Residual squares / squares around the mean.
    return 0.0

print(r2([3, 5, 7, 9], [2.8, 5.3, 6.9, 9.2]))
print(r2([3, 5, 7, 9], [6, 6, 6, 6]))
print(r2([3, 5, 7, 9], [9, 7, 5, 3]))
