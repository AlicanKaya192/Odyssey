import torch
from torch import nn


def build(sizes):
    layers = []
    for n_in, n_out in zip(sizes, sizes[1:]):
        layers += [nn.Linear(n_in, n_out), nn.ReLU()]
    return nn.Sequential(*layers[:-1])


def trace_shapes(sizes, batch):
    model = build(sizes)
    h = torch.zeros(batch, sizes[0])
    rows = []
    for layer in model:
        h = layer(h)
        rows.append([type(layer).__name__, list(h.shape)])
    return rows

for row in trace_shapes([6, 4, 2], 3):
    print(row)
