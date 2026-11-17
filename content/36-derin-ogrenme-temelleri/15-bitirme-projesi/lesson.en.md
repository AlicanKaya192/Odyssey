# Capstone: An End-to-End Classifier

In this module we saw the pieces one by one: tensors, automatic
differentiation, `nn.Module`, the loss, the optimizer, `DataLoader`, the
training loop, regularisation, normalisation, learning rate schedules, saving
and debugging. In this section we put them all into a single job: we build a
classifier that recognises handwritten digits (8 × 8 pixels) from start to
finish. Every step rests on one of the earlier sections; there is nothing new,
only everything together.

The plan:

<figure class="fig">
  <div class="flow">
    <span class="node">Data and split</span><span class="arrow">→</span>
    <span class="node">Model and check</span><span class="arrow">→</span>
    <span class="node">Training</span><span class="arrow">→</span>
    <span class="node">Test</span><span class="arrow">→</span>
    <span class="node acc">Save</span>
  </div>
  <figcaption>Every box is the topic of one of the earlier sections.</figcaption>
</figure>

## 1. Data and split

The data are the digits from the introduction: 1797 images of 64 pixels each,
with pixel values from 0 to 16. Dividing the pixels by 16 brings them between
0 and 1 (scale, the Linear Model section). Then we shuffle the data once,
with a fixed seed, and split it in three: training (60%), validation (20%,
for early stopping and choices) and test (20%, only once at the very end):

```python
import copy
import math

import torch
from sklearn.datasets import load_digits
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

digits = load_digits()
X = torch.tensor(digits.data, dtype=torch.float32) / 16
Y = torch.tensor(digits.target)
order = torch.randperm(len(X), generator=torch.Generator().manual_seed(0))
train_idx, val_idx, test_idx = order[:1078], order[1078:1437], order[1437:]
print(len(train_idx), len(val_idx), len(test_idx))
print(torch.bincount(Y[train_idx]).tolist())
```

```text
1078 359 360
[116, 110, 113, 110, 100, 108, 104, 110, 105, 102]
```

- The three sets are disjoint: no image is in two sets at once.
- The training set has 100–116 examples of each digit; the classes are
  roughly balanced, so accuracy is a meaningful measure.
- The `float32` and `long` types are right from the start (the Debugging
  section).

## 2. The model and a first check

```python
class DigitNet(nn.Module):
    def __init__(self, hidden=64, p=0.2):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(64, hidden), nn.BatchNorm1d(hidden), nn.ReLU(),
            nn.Dropout(p), nn.Linear(hidden, 10),
        )

    def forward(self, x):
        return self.layers(x)


torch.manual_seed(0)
model = DigitNet()
loss_fn = nn.CrossEntropyLoss()
print(sum(p.numel() for p in model.parameters()))
model.eval()
with torch.no_grad():
    start = loss_fn(model(X[train_idx]), Y[train_idx]).item()
print(round(start, 1), round(math.log(10), 1))
```

```text
4938
2.3 2.3
```

- The model has 4938 parameters: 64 → 64 → 10, with BatchNorm and
  dropout in between.
- There is no softmax at the output; `CrossEntropyLoss` wants logits.
- The starting loss equals `log 10`: the initialisation and the loss are
  healthy.

## 3. Training

Adam, a cosine schedule, the validation loss at the end of every epoch; if
the validation loss does not improve for 5 epochs, stop and go back to the
weights of the **best epoch**:

```python
loader = DataLoader(TensorDataset(X[train_idx], Y[train_idx]), batch_size=32,
                    shuffle=True, generator=torch.Generator().manual_seed(0))
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=30)
best_loss, best_state, best_epoch, waited = math.inf, None, 0, 0
for epoch in range(1, 31):
    model.train()
    for xb, yb in loader:
        optimizer.zero_grad()
        loss_fn(model(xb), yb).backward()
        optimizer.step()
    scheduler.step()
    model.eval()
    with torch.no_grad():
        val_loss = loss_fn(model(X[val_idx]), Y[val_idx]).item()
    if val_loss < best_loss:
        best_loss, best_epoch, waited = val_loss, epoch, 0
        best_state = copy.deepcopy(model.state_dict())
    else:
        waited += 1
        if waited == 5:
            break
print(epoch, best_epoch, round(best_loss, 3))
model.load_state_dict(best_state)
```

```text
16 11 0.056
```

- Training stopped at epoch 16; the best validation loss was
  at epoch 11 (0.056).
- `copy.deepcopy` is a must: `state_dict()` points at the weights themselves,
  and without a copy the "best" record keeps changing as training goes on
  (the note of the Training Loop section).
- Switching between `model.train()` and `model.eval()` every epoch: dropout
  and BatchNorm behave differently in the two modes.

## 4. Test

Only now, and only once, do we look at the test set:

```python
model.eval()
with torch.no_grad():
    pred = model(X[test_idx]).argmax(dim=1)
truth = Y[test_idx]
accuracy = (pred == truth).float().mean().item()
print(round(100 * accuracy, 1), (pred != truth).sum().item())

matrix = torch.zeros(10, 10, dtype=torch.long)
for t, p in zip(truth.tolist(), pred.tolist()):
    matrix[t, p] += 1
off = matrix.clone()
off.fill_diagonal_(0)
t, p = divmod(off.argmax().item(), 10)
print(f"{t} -> {p}: {off[t, p].item()}")
```

```text
96.7 12
3 -> 8: 4
```

- 12 of the 360 test images are wrong: an accuracy of
  96.7%.
- A **confusion matrix** counts `matrix[true, predicted]`; the diagonal holds
  the correct answers, the rest are errors. The most common error is taking
  a 3 for an 8 (4 times).
- Accuracy is a single number; the matrix shows **where** the model
  struggles.

## 5. Save and reload

```python
torch.save(model.state_dict(), "digits.pt")
fresh = DigitNet()
fresh.load_state_dict(torch.load("digits.pt", weights_only=True))
fresh.eval()
with torch.no_grad():
    same = torch.equal(fresh(X[test_idx]).argmax(dim=1), pred)
print(same)
```

```text
True
```

Only the state_dict is saved; the loading program builds the `DigitNet` class
in code and reads the numbers in the safe mode. The loaded model gave the same
predictions on the test set.

## Summary

- The data are split in three once, with a fixed seed; the test set is looked
  at once, at the end.
- Two checks before training: the types and the starting loss.
- The training loop: `train()`/`eval()` switching, a schedule, early stopping,
  a copy of the best weights.
- A confusion matrix next to accuracy.
- Saving: state_dict + `weights_only=True`.
