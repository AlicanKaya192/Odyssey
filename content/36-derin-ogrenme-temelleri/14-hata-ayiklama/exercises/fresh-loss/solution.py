import math


def loss_looks_fresh(num_classes, loss):
    return abs(loss - math.log(num_classes)) < 0.5

print(loss_looks_fresh(10, 2.31))
print(loss_looks_fresh(10, 92.6))
