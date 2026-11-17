import torch
from torch import nn

torch.manual_seed(0)
model = nn.Sequential(nn.Linear(8, 16), nn.ReLU(), nn.Linear(16, 2)).eval()
x = torch.randn(4, 8)
ep = torch.export.export(model, (x,))
torch.export.save(ep, "model.pt2")
loaded = torch.export.load("model.pt2").module()
print(loaded(x).shape, torch.allclose(loaded(x), model(x)))
