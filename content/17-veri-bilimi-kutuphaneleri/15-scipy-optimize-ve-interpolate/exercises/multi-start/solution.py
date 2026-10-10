import numpy as np
from scipy import optimize


def bumpy(x):
    return np.sin(3 * x[0]) + 0.1 * x[0] ** 2


def multi_start(starts):
    results = [optimize.minimize(bumpy, x0=[s]) for s in starts]
    best = min(results, key=lambda r: r.fun)
    return [round(float(best.x[0]), 3), round(float(best.fun), 3)]

print(multi_start([-2.0, 0.0, 2.0]))
print(multi_start([2.0]))
