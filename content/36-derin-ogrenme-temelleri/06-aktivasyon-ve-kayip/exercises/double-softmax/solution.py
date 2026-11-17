import torch
from torch import nn


def both_losses(logits, targets):
    z, t = torch.tensor(logits), torch.tensor(targets)
    loss_fn = nn.CrossEntropyLoss()
    right = loss_fn(z, t).item()
    double = loss_fn(torch.softmax(z, dim=1), t).item()
    return [round(right, 3), round(double, 3)]

print(both_losses([[4.0, 0.0, 0.0]], [0]))
print(both_losses([[0.0, 2.0, 0.0]], [0]))
