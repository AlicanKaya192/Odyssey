import torch
from torch import nn


def untrained_loss(n_classes):
    scores = torch.zeros(4, n_classes)
    labels = torch.zeros(4, dtype=torch.long)
    loss = nn.CrossEntropyLoss()(scores, labels)
    return round(loss.item(), 3)

print(untrained_loss(10))
print(untrained_loss(3))
