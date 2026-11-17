import torch
from torch import nn


def missing_after_load(extra):
    small = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3))
    torch.save(small.state_dict(), "small.pt")
    layers = [nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3)]
    for _ in range(extra):
        layers += [nn.ReLU(), nn.Linear(3, 3)]
    bigger = nn.Sequential(*layers)
    result = bigger.load_state_dict(torch.load("small.pt", weights_only=True), strict=False)
    return result.missing_keys

print(missing_after_load(1))
