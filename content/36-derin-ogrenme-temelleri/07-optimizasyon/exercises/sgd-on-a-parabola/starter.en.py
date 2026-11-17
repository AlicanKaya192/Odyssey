import torch


def descend(start, lr, steps):
    w = torch.tensor(start, requires_grad=True)
    optimizer = torch.optim.SGD([w], lr=lr)
    return w.item()

print(descend(0.0, 0.1, 10))
print(descend(10.0, 0.5, 1))
