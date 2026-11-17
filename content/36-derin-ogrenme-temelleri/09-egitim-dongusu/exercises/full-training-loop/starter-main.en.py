import copy

import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader, random_split
from dl_data import make_table

x_np, y_np = make_table(1000)
data = TensorDataset(torch.from_numpy(x_np), torch.from_numpy(y_np))
train_set, val_set, test_set = random_split(
    data, [600, 200, 200], generator=torch.Generator().manual_seed(0))
train_loader = DataLoader(train_set, batch_size=32, shuffle=True,
                          generator=torch.Generator().manual_seed(0), num_workers=0)
val_loader = DataLoader(val_set, batch_size=100, num_workers=0)
test_loader = DataLoader(test_set, batch_size=100, num_workers=0)


def train_one_epoch(model, loader, optimizer, loss_fn):
    model.train()
    total, count = 0.0, 0
    for xb, yb in loader:
        optimizer.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        optimizer.step()
        total += loss.item() * len(yb)
        count += len(yb)
    return total / count


def evaluate(model, loader, loss_fn):
    model.eval()
    total, correct, count = 0.0, 0, 0
    with torch.no_grad():
        for xb, yb in loader:
            logits = model(xb)
            total += loss_fn(logits, yb).item() * len(yb)
            correct += (logits.argmax(dim=1) == yb).sum().item()
            count += len(yb)
    return total / count, correct / count


torch.manual_seed(3)
model = nn.Sequential(nn.Linear(6, 32), nn.ReLU(), nn.Linear(32, 3))
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.CrossEntropyLoss()
best_loss, best_state, best_epoch = float("inf"), None, 0
for epoch in range(1, 31):
    # Train one epoch, measure validation; if the validation loss is
    # lowest, update best_loss, best_epoch and best_state.
    pass

model.load_state_dict(best_state)
test_loss, test_acc = evaluate(model, test_loader, loss_fn)
print(best_epoch < 30)
print(test_acc > 0.8)
