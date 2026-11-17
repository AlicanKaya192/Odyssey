import torch
from torch import nn


def dropout_values(p):
    drop = nn.Dropout(p)
    ones = torch.ones(1000)
    torch.manual_seed(0)
    return [[], []]

print(dropout_values(0.5))
print(dropout_values(0.2))
