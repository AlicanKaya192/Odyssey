import numpy as np
from scipy import optimize


def bumpy(x):
    return np.sin(3 * x[0]) + 0.1 * x[0] ** 2


def multi_start(starts):
    res = optimize.minimize(bumpy, x0=[starts[0]])
    return [round(float(res.x[0]), 3), round(float(res.fun), 3)]

print(multi_start([-2.0, 0.0, 2.0]))
print(multi_start([2.0]))
