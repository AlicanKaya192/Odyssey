import numpy as np
from scipy import optimize


def decay(t, a, k):
    return a * np.exp(-k * t)


def fit_decay(t, y):
    return [0.0, 0.0, 0.0]

T = [0, 1, 2, 3, 4, 5, 6, 7, 8]
Y = [80.4, 56.1, 40.2, 27.9, 20.0, 13.8, 10.1, 6.9, 5.1]
print(fit_decay(T, Y))
