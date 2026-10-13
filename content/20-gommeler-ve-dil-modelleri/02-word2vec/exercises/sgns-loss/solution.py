import math


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def sgns_loss(v, u_pos, u_negs):
    loss = -math.log(sigmoid(dot(v, u_pos)))
    for u in u_negs:
        loss -= math.log(sigmoid(-dot(v, u)))
    return round(loss, 3)

v = [0.5, -0.5]
print(sgns_loss(v, [1.0, -1.0], [[0.2, 0.1], [-0.3, 0.4]]))
print(sgns_loss([0.0, 0.0], [1.0, 1.0], [[1.0, 1.0]]))
