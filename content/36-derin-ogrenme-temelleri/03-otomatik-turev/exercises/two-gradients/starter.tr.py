import torch


def gradients(w_value, x, b_value, target):
    return [0.0, 0.0]

print(gradients(2.0, 3.0, 1.0, 5.0))
print(gradients(1.0, -1.0, 0.0, 0.0))
