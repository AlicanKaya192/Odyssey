import torch
from torch import nn

torch.manual_seed(0)
model = nn.Sequential(nn.Linear(8, 16), nn.ReLU(), nn.Linear(16, 2)).eval()
x = torch.randn(4, 8)
ep = torch.export.export(model, (x,))
# 1) ep'yi "model.pt2" dosyasina kaydet
# 2) dosyayi yukle ve .module() ile cagrilabilir yap
loaded = None
print(loaded(x).shape, torch.allclose(loaded(x), model(x)))
