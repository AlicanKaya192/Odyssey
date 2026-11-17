import torch


def slope(a, b, at):
    x = torch.tensor(at, requires_grad=True)
    y = a * x ** 2 + b * x
    y.backward()
    return round(x.grad.item(), 4)

print(slope(2.0, -1.0, 3.0))
