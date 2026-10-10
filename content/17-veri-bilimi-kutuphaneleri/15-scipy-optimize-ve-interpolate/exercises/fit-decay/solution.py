import numpy as np
from scipy import optimize


def decay(t, a, k):
    return a * np.exp(-k * t)


def fit_decay(t, y):
    t = np.array(t, dtype=float)
    y = np.array(y, dtype=float)
    (a, k), _ = optimize.curve_fit(decay, t, y, p0=[y.max(), 0.1])
    return [round(float(a), 3), round(float(k), 3), round(float(np.log(2) / k), 2)]

T = [0, 1, 2, 3, 4, 5, 6, 7, 8]
Y = [80.4, 56.1, 40.2, 27.9, 20.0, 13.8, 10.1, 6.9, 5.1]
print(fit_decay(T, Y))
