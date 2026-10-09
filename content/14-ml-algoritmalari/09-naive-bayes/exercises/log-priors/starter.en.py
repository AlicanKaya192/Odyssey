import numpy as np


def log_priors(y):
    y = np.array(y)
    # Classes with np.unique; the logs of the shares.
    return []

print(log_priors([0, 1, 1, 2, 1, 0]))
