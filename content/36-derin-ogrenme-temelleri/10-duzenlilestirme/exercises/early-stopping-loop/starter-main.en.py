import torch
from torch import nn
from dl_data import make_table

x_np, y_np = make_table(400, seed=11)
x, y = torch.from_numpy(x_np), torch.from_numpy(y_np)
x_tr, y_tr, x_val, y_val = x[:80], y[:80], x[80:], y[80:]
loss_fn = nn.CrossEntropyLoss()
torch.manual_seed(0)
model = nn.Sequential(nn.Linear(6, 128), nn.ReLU(), nn.Linear(128, 128), nn.ReLU(),
                      nn.Linear(128, 3))
optimizer = torch.optim.AdamW(model.parameters(), lr=0.01)
best, best_epoch, waited, patience = float("inf"), 0, 0, 10
for epoch in range(1, 201):
    model.train()
    optimizer.zero_grad()
    loss_fn(model(x_tr), y_tr).backward()
    optimizer.step()
    model.eval()
    with torch.no_grad():
        val_loss = loss_fn(model(x_val), y_val).item()
    # If it improved, update best, best_epoch, waited; otherwise grow waited, stop at patience.

print(epoch < 200, best_epoch < epoch)
print(best < 0.5)
