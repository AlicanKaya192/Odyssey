import torch
from torch import nn


def trainable_count(n_in, n_hidden, n_out):
    model = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Linear(n_hidden, n_out))
    total = sum(p.numel() for p in model.parameters())
    return [total, total]

print(trainable_count(6, 16, 3))
print(trainable_count(10, 5, 2))
