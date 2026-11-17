import torch
from torch import nn


def layer_shapes(size):
    model = nn.Sequential(
        nn.Conv2d(1, 8, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(8, 16, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Flatten(),
    )
    x = torch.zeros(1, 1, size, size)
    shapes = []
    for layer in model:
        x = layer(x)
        shapes.append(list(x.shape[1:]))
    return shapes

for shape in layer_shapes(16):
    print(shape)
