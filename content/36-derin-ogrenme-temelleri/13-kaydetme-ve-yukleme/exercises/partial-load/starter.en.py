import torch
from torch import nn


def missing_after_load(extra):
    small = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3))
    torch.save(small.state_dict(), "small.pt")
    layers = [nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3)]
    for _ in range(extra):
        layers += [nn.ReLU(), nn.Linear(3, 3)]
    bigger = nn.Sequential(*layers)
    return []

print(missing_after_load(1))
