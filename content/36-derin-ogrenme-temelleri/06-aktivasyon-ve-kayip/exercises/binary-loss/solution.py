import torch
from torch import nn


def binary_loss(logits, labels):
    z = torch.tensor(logits)
    y = torch.tensor(labels).float()
    return round(nn.BCEWithLogitsLoss()(z, y).item(), 4)

print(binary_loss([1.5, -0.5, 3.0], [1, 0, 0]))
print(binary_loss([0.0], [1]))
