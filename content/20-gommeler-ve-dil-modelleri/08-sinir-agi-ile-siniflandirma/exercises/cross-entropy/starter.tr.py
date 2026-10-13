import math


def cross_entropy(probs, labels):
    return 0.0

probs = [[0.7, 0.2, 0.1], [0.1, 0.8, 0.1], [0.3, 0.3, 0.4]]
print(cross_entropy(probs, [0, 1, 2]))
print(cross_entropy(probs, [2, 0, 1]))
