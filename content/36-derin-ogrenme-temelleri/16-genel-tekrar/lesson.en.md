# Overall Review

You have reached the end of the Deep Learning Fundamentals module. Starting
from a single number (a tensor), you arrived at a complete training setup
that takes derivatives automatically, uses layers you define yourself, feeds
the data in batches, guards against overfitting, ties the learning rate to a
schedule, can be saved and reloaded, and can be debugged. This section walks
the road once more; at the end there is a single example in which all the
pieces work together.

<figure class="fig">
  <div class="flow">
    <span class="node">Tensors<br><small>00–03</small></span><span class="arrow">→</span>
    <span class="node">Model<br><small>04–06</small></span><span class="arrow">→</span>
    <span class="node">Learning<br><small>07–09</small></span><span class="arrow">→</span>
    <span class="node">Robustness<br><small>10–12</small></span><span class="arrow">→</span>
    <span class="node acc">Use<br><small>13–15</small></span>
  </div>
  <figcaption>The module's road: compute with numbers, build a model, train it, make training robust, use the model.</figcaption>
</figure>

## 1. Tensors and derivatives (Sections 0–3)

| Task | Tool |
|---|---|
| Building tensors | `torch.tensor`, `zeros`, `randn`, `arange`; `dtype`, `shape` |
| Changing shape | `view`, `reshape`, `unsqueeze`, `squeeze`, `permute` |
| Computing | element-wise operations, `@` (matrix product), broadcasting, `sum(dim=...)` |
| Derivatives | `requires_grad=True`, `backward()`, `.grad`, `torch.no_grad()`, `detach()` |

Broadcasting aligns the shapes from the right and stretches dimensions of
size 1; if they do not fit, it raises an error. `backward()` **adds** the
gradient to `.grad`.

## 2. Building a model (Sections 4–6)

| Task | Tool |
|---|---|
| Gradient descent by hand | `w -= lr * w.grad` (inside `no_grad`), then `w.grad.zero_()` |
| Layers | `nn.Linear`, `nn.Sequential`, your own `nn.Module` class, `parameters()` |
| Activation | `ReLU` (in hidden layers), `Sigmoid`, `Softmax` (only when probabilities are needed) |
| Loss | `MSELoss` (regression), `CrossEntropyLoss` (classification, wants logits), `BCEWithLogitsLoss` |

No softmax at the output; `CrossEntropyLoss` applies it itself.

## 3. Learning (Sections 7–9)

| Task | Tool |
|---|---|
| Optimizer | `SGD` (+`momentum`), `Adam`; `zero_grad`, `backward`, `step` |
| Data | `Dataset` (`__len__`, `__getitem__`), `TensorDataset`, `DataLoader(batch_size, shuffle)` |
| The loop | epoch and batch loops, `model.train()` / `model.eval()`, the validation loss |
| Choosing | a `copy.deepcopy(state_dict())` copy of the best validation epoch |

## 4. Making it robust (Sections 10–12)

| Task | Tool |
|---|---|
| Against overfitting | `Dropout`, `weight_decay`, early stopping, more data |
| Initialisation and normalisation | `kaiming_normal_`, `BatchNorm1d`, `LayerNorm` |
| Learning rate | `StepLR`, `CosineAnnealingLR`, `LinearLR`, `ReduceLROnPlateau` |
| A large gradient | `nn.utils.clip_grad_norm_` (between `backward` and `step`) |

## 5. Using it (Sections 13–15)

| Task | Tool |
|---|---|
| Saving | `torch.save(model.state_dict(), path)`; the optimizer too in a checkpoint |
| Loading | build the same model, `load_state_dict(torch.load(path, weights_only=True))` |
| Debugging | a shape printout, starting loss `log(classes)`, memorising one batch, a `.grad` printout |
| Evaluating | accuracy, the confusion matrix, per-class accuracy |

## All together

All the pieces of the module in a single setup on the table data (3
classes): types, a starting loss check, a model with BatchNorm and dropout,
Adam + a cosine schedule, gradient clipping, early stopping, saving the best
weights and a safe load:

```python
import copy
import math

import torch
from dl_data import make_table
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

x_np, y_np = make_table(1200)
X, Y = torch.from_numpy(x_np).float(), torch.from_numpy(y_np).long()
train, val, test = slice(0, 800), slice(800, 1000), slice(1000, 1200)


def make_model():
    torch.manual_seed(0)
    return nn.Sequential(nn.Linear(6, 32), nn.BatchNorm1d(32), nn.ReLU(),
                         nn.Dropout(0.2), nn.Linear(32, 3))


model, loss_fn = make_model(), nn.CrossEntropyLoss()
model.eval()
with torch.no_grad():
    start = loss_fn(model(X[train]), Y[train]).item()
print("start", round(start, 1), round(math.log(3), 1))

loader = DataLoader(TensorDataset(X[train], Y[train]), batch_size=32,
                    shuffle=True, generator=torch.Generator().manual_seed(0))
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=40)
best_loss, best_epoch, waited = math.inf, 0, 0
for epoch in range(1, 41):
    model.train()
    for xb, yb in loader:
        optimizer.zero_grad()
        loss_fn(model(xb), yb).backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
    scheduler.step()
    model.eval()
    with torch.no_grad():
        val_loss = loss_fn(model(X[val]), Y[val]).item()
    if val_loss < best_loss:
        best_loss, best_epoch, waited = val_loss, epoch, 0
        torch.save(copy.deepcopy(model.state_dict()), "best.pt")
    else:
        waited += 1
        if waited == 5:
            break
print("stop", epoch, "best", best_epoch)

final = make_model()
final.load_state_dict(torch.load("best.pt", weights_only=True))
final.eval()
with torch.no_grad():
    hits = final(X[test]).argmax(dim=1) == Y[test]
print("test", round(100 * hits.float().mean().item(), 1))
```

```text
start 1.2 1.1
stop 8 best 3
test 87.0
```

- The starting loss (1.2) is close to `log 3 ≈ 1.1`: the types
  and the initialisation are healthy.
- Training stopped at epoch 8; the best validation loss was
  at epoch 3, and the next five epochs could not beat it. The
  weights of that epoch, not the last one, were loaded from disk in the safe
  mode.
- The test accuracy is 87.0%. The code is not short, but now you
  know why every line is there and what would break if it were removed.

## What comes next

In this module the models always took a flat list of numbers: 64 pixels or 6
features. The next module is **Computer Vision**: convolutional networks that
use the two-dimensional structure of an image, transfer learning with
pretrained models, and object detection. The training loop you built in this
module is used there unchanged; only the inside of the model changes.
