import torch
from torch import nn


def hook_shape(index, size):
    torch.manual_seed(0)
    model = nn.Sequential(
        nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Flatten(),
    )
    captured = []
    return []

print(hook_shape(2, 16))
print(hook_shape(5, 24))
