import torch


def f(t):
    return 3 * t ** 2 + t


def compare(value):
    x = torch.tensor(value, dtype=torch.float64, requires_grad=True)
    f(x).backward()
    h = 1e-4
    numeric = (f(value + h) - f(value - h)) / (2 * h)
    return [round(x.grad.item(), 4), round(numeric, 4)]

print(compare(1.5))
print(compare(-2.0))
