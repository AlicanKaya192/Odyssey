import torch
from torch import nn


def cnn_params(channels, kernel):
    layers = [nn.Conv2d(a, b, kernel) for a, b in zip(channels, channels[1:])]
    return sum(p.numel() for layer in layers for p in layer.parameters())

print(cnn_params([1, 8, 16], 3))
print(cnn_params([3, 16], 5))
