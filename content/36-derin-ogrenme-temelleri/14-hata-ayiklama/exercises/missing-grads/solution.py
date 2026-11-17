import torch
from torch import nn


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.first = nn.Linear(4, 4)
        self.second = nn.Linear(4, 1)

    def forward(self, x):
        h = torch.relu(self.first(x))
        return self.second(h)


def missing_grads():
    torch.manual_seed(0)
    net = Net()
    net(torch.randn(3, 4)).sum().backward()
    return [name for name, p in net.named_parameters() if p.grad is None]

print(missing_grads())
