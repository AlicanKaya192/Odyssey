import torch
from torch import nn
from dl_data import make_table


class TableNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.Linear(6, 16)
        self.out = nn.Linear(16, 3)

    def forward(self, x):
        # hidden → ReLU → out
        pass


torch.manual_seed(0)
model = TableNet()
x_np, y_np = make_table(600)
x, y = torch.from_numpy(x_np), torch.from_numpy(y_np)
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
loss_fn = nn.CrossEntropyLoss()
for epoch in range(200):
    optimizer.zero_grad()
    loss = loss_fn(model(x[:480]), y[:480])
    loss.backward()
    optimizer.step()
model.eval()
with torch.no_grad():
    accuracy = (model(x[480:]).argmax(dim=1) == y[480:]).float().mean().item()
print(model(x).shape)
print(accuracy > 0.8)
