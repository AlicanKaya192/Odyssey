import numpy as np


def sigmoid_list(z):
    z = np.array(z, dtype=float)
    return (1 / (1 + np.exp(-z))).round(4).tolist()

print(sigmoid_list([-2, 0, 2]))
print(sigmoid_list([-50, 50]))
