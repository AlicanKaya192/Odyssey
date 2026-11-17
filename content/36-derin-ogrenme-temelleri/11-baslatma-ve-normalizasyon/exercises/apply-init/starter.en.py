import torch
from torch import nn

visited = []


def init_weights(module):
    pass


def init_report(sizes):
    visited.clear()
    layers = []
    for n_in, n_out in zip(sizes, sizes[1:]):
        layers += [nn.Linear(n_in, n_out), nn.ReLU()]
    model = nn.Sequential(*layers)
    model.apply(init_weights)
    bias_total = sum(m.bias.abs().sum().item() for m in model if isinstance(m, nn.Linear))
    return [len(visited), bias_total]

print(init_report([8, 16, 16, 4]))
