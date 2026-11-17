import torch
from torch import nn


class DeepNet(nn.Module):
    def __init__(self, sizes):
        super().__init__()
        self.layers = nn.ModuleList([nn.Linear(a, b) for a, b in zip(sizes, sizes[1:])])

    def forward(self, x):
        for layer in self.layers:
            x = torch.relu(layer(x))
        return x


def count(sizes):
    model = DeepNet(sizes)
    return sum(p.numel() for p in model.parameters())

print(count([6, 8, 3]))
print(count([4, 4, 4, 4]))
