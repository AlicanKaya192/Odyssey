# The Training Loop

Our loops so far were a single block of code, and at the end we looked at
the test data once. In real projects the training loop is a little more
organised: two functions, one that trains for an epoch and one that
evaluates the model; a look at the **validation** data every epoch; the
losses kept in a history; and the best model saved. In this section we build
this skeleton; we use it for the rest of the module.

## Three parts of data

We split the data into three: **training** (the model learns from it),
**validation** (we watch the model across epochs and make decisions) and
**test** (once, at the very end, to measure the real performance).

```python
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
print(len(train_loader), len(val_loader), len(test_loader))
```

```text
19 2 2
```

The training loader shuffles; the validation and test loaders do not (the
rule from the Dataset and DataLoader section).

## Two functions: train and evaluate

```python
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
```

<figure class="fig">
  <div class="versus">
    <div><h5><code>train_one_epoch</code></h5><code>model.train()</code>, the four steps on every batch, the mean training loss.</div>
    <div><h5><code>evaluate</code></h5><code>model.eval()</code> and <code>torch.no_grad()</code>; no updates; the mean loss and accuracy.</div>
  </div>
  <figcaption>Training and evaluation in separate functions: one changes the model, the other only measures it.</figcaption>
</figure>

- The loss and accuracy are weighted by the number of examples: the mean of
  the batch means is wrong when the last batch is small.
- `evaluate` puts the model in `eval()` mode; `train_one_epoch` puts it back
  into `train()` on every call. Forgetting the mode switch is a silent bug in
  models with Dropout and BatchNorm.

## The loop, the history and the best model

```python
torch.manual_seed(3)
model = nn.Sequential(nn.Linear(6, 32), nn.ReLU(), nn.Linear(32, 3))
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.CrossEntropyLoss()
history, best_loss, best_state, best_epoch = [], float("inf"), None, 0

for epoch in range(1, 31):
    train_loss = train_one_epoch(model, train_loader, optimizer, loss_fn)
    val_loss, val_acc = evaluate(model, val_loader, loss_fn)
    history.append((train_loss, val_loss))
    if val_loss < best_loss:
        best_loss, best_epoch = val_loss, epoch
        best_state = copy.deepcopy(model.state_dict())
    if epoch % 10 == 0:
        print(epoch, round(train_loss, 2), round(val_loss, 2), round(100 * val_acc, 1))

model.load_state_dict(best_state)
test_loss, test_acc = evaluate(model, test_loader, loss_fn)
print("best", best_epoch, "test", round(100 * test_acc, 1))
```

```text
10 0.21 0.36 87.5
20 0.21 0.41 86.5
30 0.18 0.43 85.5
best 5 test 84.0
```

- Every epoch writes the training loss and the validation loss to the
  history; seeing the two side by side tells how the model is doing (the
  second note).
- At the moment the validation loss is lowest, we copy the model's **state**
  (`state_dict`, a dictionary of all the parameters). `copy.deepcopy` is a
  must: without copying, the dictionary keeps changing with the model.
- When training ends we go back to the best state and look at the test data
  **once**. The best epoch is 5, the test accuracy
  84%.
- Note: while the training loss falls through all 30 epochs, the validation
  loss **rises** after the early epochs. The model started to memorise the
  training data (overfitting). Saving the best state protected us from it;
  the next section deals with overfitting itself.

<figure class="fig">
  <div class="flow">
    <span class="node">Training<br><small>learn</small></span><span class="arrow">→</span>
    <span class="node">Validation<br><small>watch, choose</small></span><span class="arrow">→</span>
    <span class="node">Best state<br><small>state_dict</small></span><span class="arrow">→</span>
    <span class="node acc">Test<br><small>once</small></span>
  </div>
  <figcaption>Decisions (which epoch, which setting) are made with validation; the test stays untouched until the end.</figcaption>
</figure>

## Why a separate validation set?

If we picked the best epoch by looking at the **test** loss, the test data
would also have been used to choose the model. Then the test result comes
out optimistic: the model has been tuned to the test data. The rule is the
same as in the machine learning track: decisions with validation data, the
final measurement with untouched test data.

## Summary

- The data is split into three: training, validation, test.
- `train_one_epoch` (`model.train()`, four steps) and `evaluate`
  (`model.eval()`, `torch.no_grad()`) are separate functions.
- Means are weighted by the number of examples.
- Validation is measured every epoch; the best `state_dict` is kept with
  `copy.deepcopy`, loaded at the end, and the test is measured once.
