import torch
from torch import nn


def build(sizes):
    layers = []
    for n_in, n_out in zip(sizes, sizes[1:]):
        layers += [nn.Linear(n_in, n_out), nn.ReLU()]
    return nn.Sequential(*layers[:-1])


def state_summary(sizes):
    model = build(sizes)
    return [[name, tensor.numel()] for name, tensor in model.state_dict().items()]

for row in state_summary([4, 8, 3]):
    print(row)
