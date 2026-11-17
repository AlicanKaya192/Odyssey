import torch
from torch import nn


class CondNet(nn.Module):
    def forward(self, x):
        return torch.cond(x.sum() > 0, lambda t: t * 2, lambda t: t * -1, (x,))


def cond_outputs(values):
    ep = torch.export.export(CondNet(), (torch.ones(3),))
    return ep.module()(torch.tensor(values)).tolist()

print(cond_outputs([1.0, 2.0, 3.0]))
print(cond_outputs([-1.0, -2.0, 0.5]))
