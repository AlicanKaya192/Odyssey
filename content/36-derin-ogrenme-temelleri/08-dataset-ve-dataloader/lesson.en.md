# Dataset and DataLoader

So far we gave the model **all** the training data at every step. With 1200
small digits that is fine; but hundreds of thousands of images do not fit in
memory, and even if they did, processing all of them for every small step
would be very slow. The fix is to split the data into small **batches**
(mini-batches): 32 or 64 examples per step. PyTorch gives two pieces for
this: a **Dataset**, which defines how to reach the examples one by one, and
a **DataLoader**, which walks over it in batches.

## TensorDataset

If the data is already in tensors, the easiest way is `TensorDataset`:

```python
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader, random_split
from sklearn.datasets import load_digits

digits = load_digits()
X = torch.tensor(digits.data, dtype=torch.float32) / 16
y = torch.tensor(digits.target)
data = TensorDataset(X, y)
image, label = data[0]
print(len(data), image.shape, label.item())
```

```text
1797 torch.Size([64]) 0
```

A Dataset has two jobs: to say how many examples there are (`len`) and to
give the `i`th example with `data[i]`. `TensorDataset` gives each example as
an `(input, label)` pair.

## Your own Dataset class

If the data is not in tensors (files, texts, examples you generate), you
write the Dataset yourself: a class that inherits from
`torch.utils.data.Dataset` and writes `__len__` and `__getitem__`. For the
`dl_data.make_shapes` images:

```python
from torch.utils.data import Dataset
from dl_data import make_shapes


class ShapesDataset(Dataset):
    def __init__(self, n, size=16):
        self.images, self.labels = make_shapes(n, size=size)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, i):
        image = torch.from_numpy(self.images[i])
        return image, int(self.labels[i])


shapes = ShapesDataset(100)
image, label = shapes[3]
print(len(shapes), image.shape, image.dtype, label)
```

```text
100 torch.Size([1, 16, 16]) torch.float32 2
```

`__getitem__` gives a **single** example on each call. In large data sets
this is where a file is read from disk; there is no need to load everything
into memory up front.

## DataLoader: in batches

`DataLoader` takes a Dataset and walks over it in batches every epoch. It
collects the examples and stacks them into tensors of shape `(batch, ...)`:

```python
loader = DataLoader(data, batch_size=64, shuffle=True,
                    generator=torch.Generator().manual_seed(0), num_workers=0)
xb, yb = next(iter(loader))
print(xb.shape, yb.shape, len(loader))
sizes = [len(yb) for _, yb in loader]
print(sizes[:3], sizes[-1], sum(sizes))
```

```text
torch.Size([64, 64]) torch.Size([64]) 29
[64, 64, 64] 5 1797
```

- `batch_size=64`: each batch has 64 examples. 1797 examples are split into
  29 batches; the last one is the leftovers, only 5
  examples. `drop_last=True` drops it if you like.
- `shuffle=True`: the examples are shuffled every epoch. If neighbouring
  examples are similar (all the 0s first, then all the 1s), training goes
  wrong without shuffling.
- `generator=...manual_seed(0)` fixes the shuffling order; the same seed
  gives the same order on every run.
- `num_workers=0` prepares the data in the main process. On large data a few
  worker processes speed things up; the small data in this track does not
  need them.

## Splitting training and test

`random_split` splits a Dataset at random into two (or more) parts:

```python
train_set, test_set = random_split(data, [1500, 297],
                                   generator=torch.Generator().manual_seed(0))
print(len(train_set), len(test_set), type(train_set).__name__)
```

```text
1500 297 Subset
```

The parts are `Subset`s: they do not copy the data, they only keep which
positions belong to them.

## A training loop with batches

The loop now has two levels: epochs outside, batches inside. The four steps
run for each **batch**:

```python
torch.manual_seed(0)
train_loader = DataLoader(train_set, batch_size=32, shuffle=True,
                          generator=torch.Generator().manual_seed(0), num_workers=0)
model = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 10))
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
loss_fn = nn.CrossEntropyLoss()
for epoch in range(5):
    total = 0.0
    for xb, yb in train_loader:
        optimizer.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        optimizer.step()
        total += loss.item() * len(yb)
    print(epoch, round(total / len(train_set), 2))

x_test, y_test = test_set[:]
with torch.no_grad():
    correct = (model(x_test).argmax(dim=1) == y_test).sum().item()
print(correct > 270, len(train_loader) * 5)
```

```text
0 1.77
1 0.61
2 0.31
3 0.23
4 0.18
True 235
```

- With batches of 32 an epoch has 47 batches; in 5 epochs
  the model was updated 235 times. The full-data training in the
  introduction made 200 updates in 200 epochs. Batches give many steps even
  in a single pass over the data.
- We computed an epoch's loss by weighting each batch's loss by its size and
  adding them up (the last batch is small).
- More than 270 of the 297 test images are right.
- `test_set[:]` takes all the test examples at once; that is fine when the
  evaluation does not need batches.

## Summary

- `Dataset`: `__len__` and `__getitem__`; gives one example.
- `DataLoader`: walks a Dataset in batches, shuffling if asked.
- For reproducibility, `generator=torch.Generator().manual_seed(...)` when
  shuffling.
- `random_split` separates training and test.
- The training loop has two levels; the four steps run for each batch.
