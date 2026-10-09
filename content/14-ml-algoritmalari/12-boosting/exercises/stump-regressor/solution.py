import numpy as np


def fit_stump_reg(x, y):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    order = np.argsort(x)
    x, y = x[order], y[order]
    best = None
    for i in range(1, len(x)):
        if x[i] == x[i - 1]:
            continue
        left, right = y[:i], y[i:]
        err = ((left - left.mean()) ** 2).sum() + ((right - right.mean()) ** 2).sum()
        if best is None or err < best[0] - 1e-12:
            best = (err, (x[i - 1] + x[i]) / 2, left.mean(), right.mean())
    return round(float(best[1]), 3), round(float(best[2]), 3), round(float(best[3]), 3)

x = [1, 2, 3, 4, 5, 6]
y = [1.0, 1.2, 0.9, 5.0, 5.2, 4.8]
print(fit_stump_reg(x, y))
