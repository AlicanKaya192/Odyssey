import torch
from torch import nn


def both_losses(logits, targets):
    z, t = torch.tensor(logits), torch.tensor(targets)
    loss_fn = nn.CrossEntropyLoss()
    return [0.0, 0.0]

print(both_losses([[4.0, 0.0, 0.0]], [0]))
print(both_losses([[0.0, 2.0, 0.0]], [0]))
