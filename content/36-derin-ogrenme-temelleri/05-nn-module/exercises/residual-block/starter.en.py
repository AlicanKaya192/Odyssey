import torch
from torch import nn


class Residual(nn.Module):
    def __init__(self, size):
        super().__init__()
        self.layer = nn.Linear(size, size)

    def forward(self, x):
        return self.layer(x)


def apply_block(values):
    block = Residual(len(values))
    nn.init.constant_(block.layer.weight, 0.25)
    nn.init.zeros_(block.layer.bias)
    with torch.no_grad():
        return block(torch.tensor(values)).tolist()

print(apply_block([1.0, -3.0]))
print(apply_block([2.0, 2.0]))
