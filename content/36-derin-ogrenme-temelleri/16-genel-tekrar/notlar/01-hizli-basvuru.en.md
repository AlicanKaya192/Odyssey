## The training loop pattern

Every training run in the module is a form of this skeleton. You can start
from here in your own project:

```python
import copy

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


def fit(model, loader, val_x, val_y, epochs, lr=0.01, patience=5):
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, epochs)
    best_loss, best_state, waited = float("inf"), None, 0
    for epoch in range(epochs):
        model.train()
        for xb, yb in loader:
            optimizer.zero_grad()
            loss_fn(model(xb), yb).backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
        scheduler.step()
        model.eval()
        with torch.no_grad():
            val_loss = loss_fn(model(val_x), val_y).item()
        if val_loss < best_loss:
            best_loss, waited = val_loss, 0
            best_state = copy.deepcopy(model.state_dict())
        else:
            waited += 1
            if waited == patience:
                break
    model.load_state_dict(best_state)
    return best_loss


torch.manual_seed(0)
x = torch.randn(64, 4)
y = (x[:, 0] > 0).long()
loader = DataLoader(TensorDataset(x, y), batch_size=16)
net = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 2))
print(fit(net, loader, x, y, epochs=30) < 0.3)
```

```text
True
```

## Common bugs and their messages

| Symptom | Cause | Fix |
|---|---|---|
| `mat1 and mat2 shapes cannot be multiplied` | the layer's input size does not fit | print the shape layer by layer |
| `expected target dtype to be Long` | the labels are floats | `y.long()` |
| `must have the same dtype ... Double and Float` | `float64` from NumPy | `x.float()` |
| `multi-target not supported` | the target is `(n, 1)` | `y.view(-1)` |
| `Expected more than 1 value per channel` | BatchNorm in training mode on one example | `model.eval()` |
| `Weights only load failed` | a non-tensor object in the file | save a state_dict |
| `Missing key(s) in state_dict` | the model differs from the file | match the structure or `strict=False` |
| the loss is `nan` | `log 0`, a large rate, unscaled input | `cross_entropy`, a smaller rate, scaling, clipping |
| the loss does not fall, no message | softmax + `CrossEntropyLoss`, a forgotten `step` | memorise one batch |

## The mode rule

| When | Mode |
|---|---|
| training batches | `model.train()` |
| validation, test, prediction | `model.eval()` + `torch.no_grad()` |
