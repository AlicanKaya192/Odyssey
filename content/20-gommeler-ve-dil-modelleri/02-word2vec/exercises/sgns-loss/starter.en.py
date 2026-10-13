import math


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def sgns_loss(v, u_pos, u_negs):
    return 0.0

v = [0.5, -0.5]
print(sgns_loss(v, [1.0, -1.0], [[0.2, 0.1], [-0.3, 0.4]]))
print(sgns_loss([0.0, 0.0], [1.0, 1.0], [[1.0, 1.0]]))
