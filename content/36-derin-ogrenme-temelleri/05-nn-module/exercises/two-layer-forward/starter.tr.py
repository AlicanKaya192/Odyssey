import torch
from torch import nn


class TwoLayer(nn.Module):
    def __init__(self, n_in, n_hidden, n_out):
        super().__init__()
        self.first = nn.Linear(n_in, n_hidden)
        self.second = nn.Linear(n_hidden, n_out)

    def forward(self, x):
        return x


def output(values):
    model = TwoLayer(len(values), 4, 2)
    for p in model.parameters():
        nn.init.constant_(p, 0.5)
    with torch.no_grad():
        return model(torch.tensor([values])).tolist()

print(output([1.0, 2.0]))
print(output([-1.0, -2.0]))
