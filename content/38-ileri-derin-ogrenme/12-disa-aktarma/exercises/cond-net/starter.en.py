import torch
from torch import nn


class CondNet(nn.Module):
    def forward(self, x):
        # x * 2 if the sum is positive, otherwise x * -1; write it with torch.cond
        if x.sum() > 0:
            return x * 2
        return x * -1


def cond_outputs(values):
    ep = torch.export.export(CondNet(), (torch.ones(3),))
    return ep.module()(torch.tensor(values)).tolist()

print(cond_outputs([1.0, 2.0, 3.0]))
print(cond_outputs([-1.0, -2.0, 0.5]))
