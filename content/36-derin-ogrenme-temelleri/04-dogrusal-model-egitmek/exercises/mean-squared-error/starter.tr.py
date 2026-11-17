import torch


def mse(pred, target):
    return 0.0

print(mse([1.0, 2.0, 3.0], [1.0, 2.0, 5.0]))
print(mse([0.0, 0.0], [3.0, -1.0]))
