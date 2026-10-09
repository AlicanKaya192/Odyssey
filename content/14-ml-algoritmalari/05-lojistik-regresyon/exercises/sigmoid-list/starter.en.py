import numpy as np


def sigmoid_list(z):
    z = np.array(z, dtype=float)
    # 1 / (1 + e^-z)
    return z.round(4).tolist()

print(sigmoid_list([-2, 0, 2]))
print(sigmoid_list([-50, 50]))
