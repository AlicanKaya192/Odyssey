import torch
from torch import nn


def export_shapes(batches):
    torch.manual_seed(0)
    model = nn.Sequential(nn.Linear(8, 16), nn.ReLU(), nn.Linear(16, 2)).eval()
    x = torch.randn(4, 8)
    batch = torch.export.Dim("batch")
    ep = torch.export.export(model, (x,), dynamic_shapes=({0: batch},))
    return [list(ep.module()(torch.randn(b, 8)).shape) for b in batches]

print(export_shapes([3, 7]))
