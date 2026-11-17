import torch
from torch import nn


def describe(n_in, n_hidden, n_out, batch):
    model = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Linear(n_hidden, n_out))
    out = model(torch.zeros(batch, n_in))
    n_params = sum(p.numel() for p in model.parameters())
    return list(out.shape) + [n_params]

print(describe(64, 32, 10, 8))
print(describe(5, 16, 2, 3))
