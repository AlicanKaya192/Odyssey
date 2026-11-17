# Capstone: A Sensor Fault Detector

The vibration sensors in a factory send windows of 64 measurements every
second. On a faulty machine a short, sharp jump and a jitter appear somewhere
in the window. Our task is an end-to-end detector: get to know the data, set a
baseline with a simple rule, train a 1D convolutional network, evaluate it
with the right measures, and make the model deliverable. Most of what we
learned in this module comes together here.

<figure class="fig">
<div class="flow">
<span class="node">data</span><span class="arrow">→</span>
<span class="node">baseline rule</span><span class="arrow">→</span>
<span class="node acc">1D convolution</span><span class="arrow">→</span>
<span class="node">evaluation</span><span class="arrow">→</span>
<span class="node ok">delivery package</span>
</div>
<figcaption>The project's steps. The deep network is only worth it if it beats the simple rule.</figcaption>
</figure>

## The data

`make_sensor` gives the windows and 0/1 fault labels. The gain of real
sensors differs from one to another: one measures the same vibration twice
as large. To imitate this, we multiply every window by a gain between 0.5
and 2 drawn with a fixed seed.

```python
import json
import numpy as np
import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_sensor

x_np, y_np = make_sensor(600, seed=7)
gain = np.random.default_rng(3).uniform(0.5, 2.0, (600, 1)).astype(np.float32)
x_np = x_np * gain
x, y = torch.tensor(x_np).unsqueeze(1), torch.tensor(y_np)
splits = {"train": slice(0, 400), "val": slice(400, 500), "test": slice(500, 600)}
print(tuple(x.shape), [int(y[s].sum()) for s in splits.values()])
```

```text
(600, 1, 64) [119, 19, 30]
```

- `unsqueeze(1)`: `Conv1d` wants its input as `(batch, channels, length)`; we
  added a single channel.
- 400 of the 600 windows are training, 100 validation, 100 test; the list is
  the number of faults in each part. Faults are a minority: about a third in
  training and test, fewer in validation. A model that always says "healthy"
  would be right about 70% of the time on the test set; accuracy alone will
  not be enough.

## Baseline: the peak rule

A fault is a jump; the simplest rule is "fault if the largest absolute value
in the window exceeds a threshold". We choose the threshold on the
**validation** data and measure on the test data:

```python
def rule(xs, threshold):
    return (xs.abs().amax(dim=(1, 2)) > threshold).long()


def accuracy(pred, ys):
    return (pred == ys).float().mean().item()


val, test = splits["val"], splits["test"]
candidates = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
best_t = max(candidates, key=lambda t: accuracy(rule(x[val], t), y[val]))
rule_acc = accuracy(rule(x[test], best_t), y[test])
print(best_t, round(rule_acc, 2))
```

```text
3.0 0.93
```

The rule is not bad, but the difference in gain spoils it: the normal wave of
a healthy sensor with a large gain can be bigger than the jump of a faulty
sensor with a small gain. A network's job is to get past this: to recognise
the jump not by the size of the values but by **the shape of the wave**.

## A 1D convolutional network

```python
def make_net():
    return nn.Sequential(
        nn.Conv1d(1, 16, 5, padding=2), nn.ReLU(), nn.MaxPool1d(2),
        nn.Conv1d(16, 32, 5, padding=2), nn.ReLU(), nn.AdaptiveMaxPool1d(1),
        nn.Flatten(), nn.Linear(32, 2))


def predict(model, xs):
    with torch.no_grad():
        return model(xs).argmax(dim=1)


torch.manual_seed(0)
model = make_net()
opt = torch.optim.Adam(model.parameters(), lr=0.003)
loader = torch.utils.data.DataLoader(
    torch.utils.data.TensorDataset(x[splits["train"]], y[splits["train"]]),
    batch_size=32, shuffle=True, generator=torch.Generator().manual_seed(1))
best_val, best_state = -1.0, None
for epoch in range(15):
    model.train()
    for xb, yb in loader:
        opt.zero_grad()
        F.cross_entropy(model(xb), yb).backward()
        opt.step()
    model.eval()
    val_acc = accuracy(predict(model, x[val]), y[val])
    if val_acc > best_val:
        best_val = val_acc
        best_state = {k: v.clone() for k, v in model.state_dict().items()}
model.load_state_dict(best_state)
print(sum(p.numel() for p in model.parameters()), best_val > 0.95)
```

```text
2754 True
```

- `AdaptiveMaxPool1d(1)`: takes each channel's largest response in the window.
  Wherever the jump is in the window it is caught, and the network also works
  on windows of a different length.
- We kept the weights of the epoch with the best validation accuracy (a copy
  of the `state_dict`) and loaded them at the end: a simple form of early
  stopping.

## Evaluation

Missing a fault is costly; so for the fault class **precision** ("how many of
the ones we called faults really are faults") and **recall** ("how many of
the real faults we caught") are measured separately.

```python
def precision_recall(pred, ys):
    tp = ((pred == 1) & (ys == 1)).sum().item()
    return tp / max(1, (pred == 1).sum().item()), tp / (ys == 1).sum().item()


pred = predict(model, x[test])
precision, recall = precision_recall(pred, y[test])
print(accuracy(pred, y[test]) > rule_acc, precision > 0.9, recall > 0.9)
print(precision_recall(rule(x[test], best_t), y[test])[1] < recall)
```

```text
True True True
True
```

- The network beats the rule on the test set; precision and recall are both
  above 0.9.
- The last line: the rule misses more of the faults (its recall is lower).
  The difference in accuracy looks small, but the real gain is here.

## The delivery package

As in the Exporting a Model section: the exported model, a description and a
golden output.

```python
batch = torch.export.Dim("batch")
ep = torch.export.export(model, (x[test][:4],), dynamic_shapes=({0: batch},))
torch.export.save(ep, "sensor.pt2")
meta = {"classes": ["healthy", "fault"], "length": 64, "test_recall": recall}
with open("sensor.json", "w") as f:
    json.dump(meta, f)
with torch.no_grad():
    golden = model(x[test][:8])
loaded = torch.export.load("sensor.pt2").module()
print(torch.allclose(loaded(x[test][:8]), golden, atol=1e-5), loaded(x[test]).shape)
```

```text
True torch.Size([100, 2])
```

The package is ready: `sensor.pt2` loads without the class code, is checked
against the golden output, and classifies 100 windows in a single call.

## Summary

- Get to know the data first: class balance, the right split (training /
  validation / test).
- A simple rule first: the threshold is chosen on validation and measured
  once on the test set.
- 1D convolution + `AdaptiveMaxPool1d`: recognises the jump independently of
  its position and the gain.
- Keep the best validation epoch; leave the test set for the very end.
- For a minority class, precision and recall rather than accuracy.
- Delivery: the exported model + a description + a golden output.
