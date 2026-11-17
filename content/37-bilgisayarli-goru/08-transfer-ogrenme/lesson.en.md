# Transfer Learning

Training big networks from scratch needs a lot of data and time. In practice
most image projects start from a network **pretrained** on another task with
a large dataset. For example, the last layer of a ResNet-50 trained on
ImageNet is replaced, and a "cat or dog?" classifier is built with a few
hundred cat and dog photos. This is called **transfer learning**: features
learned on one task are carried over to another.

We do not download pretrained weights; instead we build the same idea
ourselves on a small scale: first we train a network with plenty of data on a
**source task** (shape classification), then carry it to two **target tasks**
with little data. One target is close to the source, the other far.

## The source task: training with plenty of data

We split the network into two parts: a **body** (`features`) that turns a
picture into a feature vector, and a **head** that gives class scores from the
vector. The body, like ResNet, has BatchNorm and ends with global average
pooling: each picture comes down to a feature vector of 64 numbers.

```python
import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from dl_data import make_shapes


def make_features():
    return nn.Sequential(
        nn.Conv2d(1, 16, 3, padding=1), nn.BatchNorm2d(16), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(),
        nn.AdaptiveAvgPool2d(1), nn.Flatten(),
    )


def fit(model, x, y, epochs, lr, params=None, seed=0, batch_size=32):
    params = model.parameters() if params is None else params
    optimizer = torch.optim.Adam(params, lr=lr)
    loader = DataLoader(TensorDataset(x, y), batch_size=batch_size, shuffle=True,
                        generator=torch.Generator().manual_seed(seed))
    for epoch in range(epochs):
        model.train()
        for xb, yb in loader:
            optimizer.zero_grad()
            F.cross_entropy(model(xb), yb).backward()
            optimizer.step()


def accuracy(model, x, y):
    model.eval()
    with torch.no_grad():
        return (model(x).argmax(dim=1) == y).float().mean().item()


x_src, y_src = map(torch.from_numpy, make_shapes(600, seed=1))
x_chk, y_chk = map(torch.from_numpy, make_shapes(300, seed=2))
torch.manual_seed(0)
source = nn.Sequential(make_features(), nn.Linear(64, 3))
fit(source, x_src, y_src, epochs=5, lr=0.005)
print(accuracy(source, x_chk, y_chk) > 0.95)
torch.save(source[0].state_dict(), "source_features.pt")
print(len(source[0].state_dict()))
```

```text
True
21
```

- On the source task the network separates the shapes almost perfectly.
- We saved only the body's weights (`state_dict`) to a file: downloading a
  pretrained model means getting exactly such a file. The dictionary has 21
  entries: the weights and biases of three convolutions (6) and the scale,
  shift, two running statistics and a counter of three BatchNorms (15).

## Three paths

For a new task there are three options:

1. **From scratch:** train a randomly started network on the new data only.
2. **Feature extraction:** **freeze** the body from the source
   (`requires_grad = False`) and train only the new head.
3. **Fine-tuning:** train the body too, but with a small learning rate;
   shift what was learned towards the new task without breaking it.

```python
def make_model(mode, num_classes):
    features = make_features()
    if mode != "scratch":
        features.load_state_dict(torch.load("source_features.pt", weights_only=True))
    if mode == "frozen":
        for p in features.parameters():
            p.requires_grad = False
    return nn.Sequential(features, nn.Linear(64, num_classes))


def trainable(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


print(trainable(make_model("scratch", 2)), trainable(make_model("frozen", 2)))
```

```text
23650 130
```

In the frozen model only the head's parameters are trained: 64 × 2 + 2 = 130.
`weights_only=True` reads only tensors from the file; it prevents running code
from a file that came from someone else.

## A close target: round or angular?

The first target task is very similar to the source: the same kind of
pictures, but a different question ("a circle or not?") and only **24**
labelled pictures. Since the result of a single training run can swing with
the seed, we try each path with three seeds and look at the mean.

```python
def compare(x_train, y_train, x_test, y_test, num_classes, epochs):
    results = {}
    for mode in ("scratch", "frozen", "finetune"):
        scores = []
        for seed in (0, 1, 2):
            torch.manual_seed(seed)
            model = make_model(mode, num_classes)
            params = model[1].parameters() if mode == "frozen" else None
            lr = 0.002 if mode == "finetune" else 0.005
            fit(model, x_train, y_train, epochs, lr, params, seed, batch_size=8)
            scores.append(accuracy(model, x_test, y_test))
        results[mode] = round(sum(scores) / 3, 2)
    return results


x_a, y_a = map(torch.from_numpy, make_shapes(24, seed=5))
x_at, y_at = map(torch.from_numpy, make_shapes(300, seed=6))
y_a, y_at = (y_a != 0).long(), (y_at != 0).long()
print(compare(x_a, y_a, x_at, y_at, num_classes=2, epochs=20))
```

```text
{'scratch': 0.88, 'frozen': 1.0, 'finetune': 0.95}
```

- **Feature extraction** gets every test picture right: the features learned
  on the source are already enough for this question; learning 130 parameters
  from 24 pictures is easy.
- Training **from scratch** falls behind with 24 pictures; its result also
  swings a lot from seed to seed.
- Fine-tuning sits between the two: moving the whole body with little data
  carries some risk.

## A far target: digits

The second target is far from the source: handwritten digits (enlarged to
16 × 16), only **5** training pictures per digit.

```python
from sklearn.datasets import load_digits

digits = load_digits()
x_all = torch.tensor(digits.images, dtype=torch.float32).unsqueeze(1) / 16
x_all = F.interpolate(x_all, size=16, mode="bilinear")
y_all = torch.tensor(digits.target)
order = torch.randperm(len(y_all), generator=torch.Generator().manual_seed(0))
train_idx = torch.cat([order[y_all[order] == d][:5] for d in range(10)])
test_mask = torch.ones(len(y_all), dtype=torch.bool)
test_mask[train_idx] = False
x_b, y_b = x_all[train_idx], y_all[train_idx]
x_bt, y_bt = x_all[test_mask], y_all[test_mask]
print(len(y_b), len(y_bt))
print(compare(x_b, y_b, x_bt, y_bt, num_classes=10, epochs=30))
```

```text
50 1747
{'scratch': 0.72, 'frozen': 0.4, 'finetune': 0.8}
```

- This time **feature extraction** is very poor: the features learned to tell
  a circle from a square are not enough to tell digits apart.
- **Fine-tuning** is the best: the body knows general patterns such as edges
  and corners; a small shift fits them to digits. A network starting from
  scratch cannot get as far with 50 pictures.

The lesson: **the closer the source and target, the better freezing works;
the further apart, the more fine-tuning is needed.** Features learned on a
very varied source such as ImageNet carry well even to very different
targets; our small single-task source has a narrower reach.

## Freezing does not stop BatchNorm

`requires_grad = False` freezes the weights, but BatchNorm's running
statistics (`running_mean`, `running_var`) are buffers, not weights. While the
network is in training mode they are updated on every batch:

```python
torch.manual_seed(0)
frozen = make_model("frozen", 2)
weight_before = frozen[0][0].weight.clone()
stats_before = frozen[0][1].running_mean.clone()
fit(frozen, x_a, y_a, 5, 0.005, frozen[1].parameters(), batch_size=8)
print(torch.equal(frozen[0][0].weight, weight_before))
print(torch.equal(frozen[0][1].running_mean, stats_before))

torch.manual_seed(0)
frozen = make_model("frozen", 2)
stats_before = frozen[0][1].running_mean.clone()
optimizer = torch.optim.Adam(frozen[1].parameters(), lr=0.005)
frozen.train()
frozen[0].eval()
for xb, yb in DataLoader(TensorDataset(x_a, y_a), batch_size=8):
    optimizer.zero_grad()
    F.cross_entropy(frozen(xb), yb).backward()
    optimizer.step()
print(torch.equal(frozen[0][1].running_mean, stats_before))
```

```text
True
False
True
```

- The convolution weight did not change, but the BatchNorm statistic did: the
  body is not fully frozen.
- For a real freeze the body must stay in **evaluation mode** during training:
  `model[0].eval()` after `model.train()`.
- This matters: if the target data is small or different from the source,
  updating the statistics to it can damage what was learned on the source.

## Preprocessing must match the source

A pretrained network expects the preprocessing of the data it was trained on.
Our source was trained on grey pictures in [0, 1]; we gave the target pictures
in the same form (dividing the digits by 16 and enlarging them to 16 × 16).
Pretrained torchvision models carry their own preprocessing with them; we can
read it without downloading weights:

```python
from torchvision import models

info = models.ResNet18_Weights.IMAGENET1K_V1
prep = info.transforms()
print(prep.mean, prep.std)
print(prep.resize_size, prep.crop_size)
print(len(info.meta["categories"]))
```

```text
[0.485, 0.456, 0.406] [0.229, 0.224, 0.225]
[256] [224]
1000
```

With ImageNet weights, pictures are resized to 256, a 224 × 224 piece is cut
from the centre and normalised with this mean and deviation. If another
normalisation is given the network still runs, but its features break down.

## Summary

- Transfer learning: a body trained on a source task + a new head for the new
  task.
- Feature extraction: the body is frozen, only the head learns; strong when
  the source is close.
- Fine-tuning: the body learns too, with a small learning rate; needed when
  the source is far.
- `eval()` for BatchNorm in a frozen body; preprocessing the same as the
  source.
- A weight file is read with `torch.load(..., weights_only=True)`.
