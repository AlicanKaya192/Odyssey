import torch


def accumulated(value, times):
    x = torch.tensor(value, requires_grad=True)
    for _ in range(times):
        y = x ** 2
        y.backward()
    return x.grad.item()

print(accumulated(2.0, 3))
print(accumulated(-1.5, 2))
