import numpy as np


def alpha_bars(T, start, end, ts):
    betas = np.linspace(start, end, T)
    alpha_bar = np.cumprod(1 - betas)
    return [round(float(alpha_bar[t]), 4) for t in ts]


print(alpha_bars(100, 0.0001, 0.1, [0, 9, 29, 99]))
print(alpha_bars(1000, 0.0001, 0.02, [0, 499, 999]))
