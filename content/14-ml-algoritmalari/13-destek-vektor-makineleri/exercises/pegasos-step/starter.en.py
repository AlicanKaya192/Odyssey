import numpy as np


def pegasos_step(x, yi, w, b, lam, t):
    x, w = np.array(x, dtype=float), np.array(w, dtype=float)
    lr = 1 / (lam * t)
    # Inside the margin?
    return w.round(4).tolist(), round(b, 4)

w, b = [0.0, 0.0], 0.0
w, b = pegasos_step([1.0, 2.0], 1, w, b, 0.1, 1)
print(w, b)
w, b = pegasos_step([2.0, 2.0], 1, w, b, 0.1, 2)
print(w, b)
