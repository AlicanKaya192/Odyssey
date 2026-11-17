import torch


def slope(value):
    x = torch.tensor(value, requires_grad=True)
    y = x ** 3 - 2 * x
    return 0.0

print(slope(2.0))
print(slope(0.5))
