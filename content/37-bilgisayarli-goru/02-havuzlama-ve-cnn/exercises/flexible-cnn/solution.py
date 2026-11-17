import torch
from torch import nn


def build_cnn(num_classes):
    return nn.Sequential(
        nn.Conv2d(1, 16, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(16, 32, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.AdaptiveAvgPool2d(1),
        nn.Flatten(),
        nn.Linear(32, num_classes),
    )


def param_count(num_classes):
    return sum(p.numel() for p in build_cnn(num_classes).parameters())

model = build_cnn(5)
for size in (16, 40):
    print(size, tuple(model(torch.zeros(2, 1, size, size)).shape))
print(param_count(5))
