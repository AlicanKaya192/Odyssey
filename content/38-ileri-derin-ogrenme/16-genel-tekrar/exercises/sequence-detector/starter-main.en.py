import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_sequences


class Detector(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(10, 8)
        self.conv = nn.Conv1d(8, 16, kernel_size=2)
        self.head = nn.Linear(16, 2)

    def forward(self, ids):
        h = self.embed(ids).transpose(1, 2)
        return self.head(torch.relu(self.conv(h)).amax(dim=2))


x_np, y_np = make_sequences(600, seed=7)
x, y = torch.tensor(x_np), torch.tensor(y_np)
torch.manual_seed(0)
model = Detector()
opt = torch.optim.Adam(model.parameters(), lr=0.01)
gen = torch.Generator().manual_seed(1)
# 1) 20 epochs: every epoch torch.randperm(500, generator=gen), batches of 50
# 2) model.eval(); export with a free batch size (Dim) and save to "detector.pt2"

with torch.no_grad():
    acc = (model(x[500:]).argmax(1) == y[500:]).float().mean().item()
    golden = model(x[500:])
loaded = torch.export.load("detector.pt2").module()
print(acc > 0.95)
print(torch.allclose(loaded(x[500:]), golden, atol=1e-5), loaded(x[:3]).shape)
