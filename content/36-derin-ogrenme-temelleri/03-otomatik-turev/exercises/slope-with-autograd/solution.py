import torch


def slope(value):
    x = torch.tensor(value, requires_grad=True)
    y = x ** 3 - 2 * x
    y.backward()
    return round(x.grad.item(), 4)

print(slope(2.0))
print(slope(0.5))
