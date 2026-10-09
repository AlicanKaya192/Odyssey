import numpy as np


def fit_stump_reg(x, y):
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
    return best[1], best[2], best[3]


def gradient_boost_1d(x, y, rounds, lr):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    pred = np.full(len(y), y.mean())
    # rounds kez: artiklara kutuk, lr kadar ekle.
    return round(float(((y - pred) ** 2).mean()), 4)

x = [1, 2, 3, 4, 5, 6, 7, 8]
y = [1.0, 1.5, 1.2, 4.0, 4.5, 4.2, 8.0, 8.4]
for rounds in (0, 1, 5, 30):
    print(rounds, gradient_boost_1d(x, y, rounds, 0.5))
