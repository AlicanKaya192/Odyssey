import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sgd_step(v, u_pos, u_negs, lr):
    return [v, u_pos, u_negs]

v, u_pos, u_negs = sgd_step([0.5, -0.5], [1.0, -1.0], [[0.2, 0.1]], 0.1)
print(v)
print(u_pos)
print(u_negs)
