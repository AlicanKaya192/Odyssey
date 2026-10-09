import numpy as np


def log_priors(y):
    y = np.array(y)
    return [round(float(np.log((y == c).mean())), 4) for c in np.unique(y)]

print(log_priors([0, 1, 1, 2, 1, 0]))
