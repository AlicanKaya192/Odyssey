import torch
from torch import nn


def trainable_count(n_in, n_hidden, n_out):
    model = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Linear(n_hidden, n_out))
    for p in model[0].parameters():
        p.requires_grad = False
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return [trainable, total]

print(trainable_count(6, 16, 3))
print(trainable_count(10, 5, 2))
