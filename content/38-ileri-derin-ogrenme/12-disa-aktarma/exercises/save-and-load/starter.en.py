import torch
from torch import nn

torch.manual_seed(0)
model = nn.Sequential(nn.Linear(8, 16), nn.ReLU(), nn.Linear(16, 2)).eval()
x = torch.randn(4, 8)
ep = torch.export.export(model, (x,))
# 1) Save ep to the file "model.pt2"
# 2) Load the file and make it callable with .module()
loaded = None
print(loaded(x).shape, torch.allclose(loaded(x), model(x)))
