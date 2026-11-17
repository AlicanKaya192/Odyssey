import torch
from torch import nn


def export_shapes(batches):
    torch.manual_seed(0)
    model = nn.Sequential(nn.Linear(8, 16), nn.ReLU(), nn.Linear(16, 2)).eval()
    x = torch.randn(4, 8)
    # Grup boyunu (0. boyut) serbest birak
    ep = torch.export.export(model, (x,))
    return [list(ep.module()(torch.randn(b, 8)).shape) for b in batches]

print(export_shapes([3, 7]))
