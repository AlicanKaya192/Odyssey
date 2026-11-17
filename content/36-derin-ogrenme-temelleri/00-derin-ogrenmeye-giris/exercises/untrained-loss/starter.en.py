import torch
from torch import nn


def untrained_loss(n_classes):
    return 0.0

print(untrained_loss(10))
print(untrained_loss(3))
