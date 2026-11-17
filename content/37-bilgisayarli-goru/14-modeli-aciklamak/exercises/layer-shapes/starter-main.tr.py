import torch
from torch import nn

torch.manual_seed(0)
model = nn.Sequential(
    nn.Conv2d(1, 4, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(4, 8, 3), nn.ReLU(), nn.Flatten(),
)


def layer_shapes(size):
    return []

for shape in layer_shapes(8):
    print(shape)
print(layer_shapes(12)[-1])
print(len(layer_shapes(8)))
