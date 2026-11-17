import torch
from torch import nn


def ce(logits, targets):
    return 0.0

print(ce([[2.0, 1.0, 0.1], [0.5, 2.5, -1.0]], [0, 1]))
print(ce([[0.0, 0.0, 0.0]], [2]))
