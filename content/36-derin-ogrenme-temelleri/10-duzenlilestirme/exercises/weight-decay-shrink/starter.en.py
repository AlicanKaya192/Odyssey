import torch


def after_decay(start, lr, decay, steps):
    w = torch.tensor([start], requires_grad=True)
    return start

print(after_decay(1.0, 0.1, 0.1, 3))
print(after_decay(2.0, 0.5, 0.2, 2))
