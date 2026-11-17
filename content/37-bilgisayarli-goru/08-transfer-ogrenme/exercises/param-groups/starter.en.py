import torch
from torch import nn


def group_summary(body_lr, head_lr):
    body = nn.Sequential(nn.Conv2d(1, 8, 3), nn.ReLU(), nn.AdaptiveAvgPool2d(1), nn.Flatten())
    head = nn.Linear(8, 3)
    return []

print(group_summary(0.0001, 0.01))
