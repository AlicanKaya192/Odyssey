# Overfitting and Regularisation

In the Training Loop section we saw the validation loss rise after a point:
the model had started to **memorise** the training data. This is called
**overfitting**. Neural networks have many parameters, so they memorise
easily on little data. In this section we make overfitting big on purpose
and try four tools against it: **Dropout**, **weight decay**, **early
stopping** and a smaller model. These are the deep learning counterparts of
the regularisation idea from the machine learning track (the L2 penalty,
tree pruning).

## Making overfitting big

Let us keep only 80 examples for training and 320 for validation, and build
a network that is very large for 80 examples (two hidden layers of 128
neurons):

```python
import torch
from torch import nn
from dl_data import make_table

x_np, y_np = make_table(400, seed=11)
x, y = torch.from_numpy(x_np), torch.from_numpy(y_np)
x_tr, y_tr, x_val, y_val = x[:80], y[:80], x[80:], y[80:]
loss_fn = nn.CrossEntropyLoss()


def fit(model, epochs=200, weight_decay=0.0):
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.01, weight_decay=weight_decay)
    for _ in range(epochs):
        model.train()
        optimizer.zero_grad()
        loss_fn(model(x_tr), y_tr).backward()
        optimizer.step()
    model.eval()
    with torch.no_grad():
        train_acc = (model(x_tr).argmax(dim=1) == y_tr).float().mean().item()
        val_loss = loss_fn(model(x_val), y_val).item()
    return round(train_acc, 2), round(val_loss, 1)


def big_net(p=0.0):
    torch.manual_seed(0)
    return nn.Sequential(nn.Linear(6, 128), nn.ReLU(), nn.Dropout(p),
                         nn.Linear(128, 128), nn.ReLU(), nn.Dropout(p),
                         nn.Linear(128, 3))


print("big", fit(big_net()))
```

```text
big (1.0, 2.4)
```

The training accuracy is **100%**: the model memorised all 80 examples. But
the validation loss is 2.4: on examples it has not seen it is
very sure and often wrong. Memorising is not learning.

## Dropout

**Dropout** sets a random part of the neurons (e.g. half) to zero at every
step during training. The network cannot rely on a single neuron; it has to
spread the information over many paths. In evaluation (`model.eval()`)
Dropout switches off:

```python
drop = nn.Dropout(p=0.5)
ones = torch.ones(10)
torch.manual_seed(0)
print(drop(ones).tolist())
drop.eval()
print(drop(ones).tolist())
```

```text
[0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 2.0]
[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
```

- In training mode some elements are 0 and the rest are **2.0**: Dropout
  scales the remaining values by `1 / (1 − p)` so the mean of the output
  does not change.
- In `eval()` mode nothing changes. In the nn.Module section we said why
  `model.eval()` matters: forget it and the predictions change randomly on
  every run.

## Weight decay and a smaller model

**Weight decay** pulls the weights a little towards zero at every step:
large weights are penalised and the model stays "smoother". In `AdamW` it is
the `weight_decay` parameter. There is also the simplest remedy: a smaller
model.

```python
print("dropout", fit(big_net(p=0.5)))
print("decay", fit(big_net(), weight_decay=1.0))
torch.manual_seed(0)
print("small", fit(nn.Sequential(nn.Linear(6, 8), nn.ReLU(), nn.Linear(8, 3))))
```

```text
dropout (1.0, 1.6)
decay (1.0, 1.2)
small (0.95, 0.8)
```

With Dropout and weight decay the training accuracy is again 100% (80
examples are easy to memorise), with the small model 95%; in all three the
validation loss came down. None of them is magic; each makes memorising
harder and pushes the model towards general rules.

## Early stopping

The strongest and cheapest remedy is to watch the validation loss and **stop
the moment it stops improving**. If there is no improvement for a given
number of epochs (the patience), training is cut and we go back to the best
state:

```python
def early_stopping_fit(model, patience=10, max_epochs=200):
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.01)
    best, best_epoch, waited = float("inf"), 0, 0
    for epoch in range(1, max_epochs + 1):
        model.train()
        optimizer.zero_grad()
        loss_fn(model(x_tr), y_tr).backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            val_loss = loss_fn(model(x_val), y_val).item()
        if val_loss < best:
            best, best_epoch, waited = val_loss, epoch, 0
        else:
            waited += 1
            if waited == patience:
                break
    return best_epoch, epoch, round(best, 2)


print(early_stopping_fit(big_net()))
```

```text
(4, 14, 0.36)
```

The best validation loss came at epoch 4; after 10 epochs
without improvement, training stopped at epoch 14. The
validation loss (0.36) is lower than all the other remedies,
and the training is much shorter. (Here we did not save the best state; real
code saves it with `copy.deepcopy(model.state_dict())`, as in the Training
Loop section.)

## More data

The root of overfitting is too little data for the model's power. Let us
train the same large network for 200 epochs with 800 examples instead of 80:

```python
x2_np, y2_np = make_table(1120, seed=11)
x_tr = torch.from_numpy(x2_np[:800])
y_tr = torch.from_numpy(y2_np[:800])
x_val, y_val = torch.from_numpy(x2_np[800:]), torch.from_numpy(y2_np[800:])
print("big + 800", fit(big_net()))
```

```text
big + 800 (1.0, 1.6)
```

In 200 epochs this large network memorised all 800 examples too (the
training accuracy is again 100%), but the validation loss went down from
2.4 to 1.6: more data makes memorising harder.
Still, 800 examples are few for this network; early stopping is still the
most effective remedy here.

The remedies are used together, not instead of each other: all the data you
can get, a reasonably sized model, a little Dropout or weight decay, and
always early stopping.

## Summary

- Overfitting: perfect on training, bad on unseen data. Little data, many
  parameters.
- Dropout switches neurons off at random during training and switches off
  in `eval()`.
- Weight decay (`AdamW(weight_decay=...)`) keeps the weights small.
- Early stopping stops when the validation loss stops improving.
- More data makes memorising harder. The remedies are used together; early
  stopping always.
