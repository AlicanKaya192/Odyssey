import torch
from torch import nn


def group_summary(body_lr, head_lr):
    body = nn.Sequential(nn.Conv2d(1, 8, 3), nn.ReLU(), nn.AdaptiveAvgPool2d(1), nn.Flatten())
    head = nn.Linear(8, 3)
    optimizer = torch.optim.Adam([
        {"params": body.parameters(), "lr": body_lr},
        {"params": head.parameters(), "lr": head_lr},
    ])
    return [[group["lr"], sum(p.numel() for p in group["params"])] for group in optimizer.param_groups]

print(group_summary(0.0001, 0.01))
