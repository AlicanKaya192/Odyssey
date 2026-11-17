import torch


def accumulated(value, times):
    x = torch.tensor(value, requires_grad=True)
    return 0.0

print(accumulated(2.0, 3))
print(accumulated(-1.5, 2))
