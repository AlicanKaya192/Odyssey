import torch
from torch import nn


class CondNet(nn.Module):
    def forward(self, x):
        # Toplam pozitifse x * 2, degilse x * -1; torch.cond ile yaz
        if x.sum() > 0:
            return x * 2
        return x * -1


def cond_outputs(values):
    ep = torch.export.export(CondNet(), (torch.ones(3),))
    return ep.module()(torch.tensor(values)).tolist()

print(cond_outputs([1.0, 2.0, 3.0]))
print(cond_outputs([-1.0, -2.0, 0.5]))
