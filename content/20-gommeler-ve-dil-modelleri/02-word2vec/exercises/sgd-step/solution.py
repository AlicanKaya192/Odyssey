import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sgd_step(v, u_pos, u_negs, lr):
    v, u_pos, u_negs = np.array(v), np.array(u_pos), np.array(u_negs)
    g_pos = sigmoid(v @ u_pos) - 1
    g_neg = sigmoid(u_negs @ v)
    grad_v = g_pos * u_pos + (g_neg[:, None] * u_negs).sum(axis=0)
    new_u_pos = u_pos - lr * g_pos * v
    new_u_negs = u_negs - lr * g_neg[:, None] * v
    new_v = v - lr * grad_v
    return [new_v.round(3).tolist(), new_u_pos.round(3).tolist(), new_u_negs.round(3).tolist()]

v, u_pos, u_negs = sgd_step([0.5, -0.5], [1.0, -1.0], [[0.2, 0.1]], 0.1)
print(v)
print(u_pos)
print(u_negs)
