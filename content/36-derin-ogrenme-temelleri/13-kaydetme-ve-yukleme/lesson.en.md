# Saving and Loading Models

You trained a model for hours; when the program closes, everything it learned
stays in memory and is gone. In this section we see how to write a trained
model to disk, load it back in another program and resume an interrupted
training run where it stopped. There is also a security topic: a model file
looks as if it only carries numbers, but loaded the wrong way it is a file in
which code can be run.

## state_dict

Everything the model learned is in its parameters. `model.state_dict()`
gives them as a name → tensor dictionary:

```python
import torch
from torch import nn

torch.manual_seed(0)
model = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3))
for name, tensor in model.state_dict().items():
    print(name, tuple(tensor.shape))
```

```text
0.weight (8, 4)
0.bias (8,)
2.weight (3, 8)
2.bias (3,)
```

- The names come from the layer's position in the `Sequential`: `0` is the
  first `Linear`, `2` the second. `ReLU` (1) has no parameters and is not in
  the dictionary.
- The dictionary holds no **code** of the model, only its numbers. When
  loading, we rebuild the same structure in code and put the numbers into it.

## Saving and loading

```python
torch.save(model.state_dict(), "model.pt")

torch.manual_seed(1)
restored = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3))
x = torch.randn(5, 4)
print(torch.equal(model(x), restored(x)))
result = restored.load_state_dict(torch.load("model.pt", weights_only=True))
print(torch.equal(model(x), restored(x)))
print(result)
```

```text
False
True
<All keys matched successfully>
```

- The new model was built with another seed; its predictions were different
  (`False`). After loading the numbers they were exactly the same (`True`).
- `load_state_dict` reports that every key matched. If a key does not match,
  it raises an error (the first note).
- On a model loaded for prediction, do not forget `model.eval()` (the modes of
  dropout and BatchNorm).

## Why weights_only=True matters

`torch.save` uses Python's `pickle` format. `pickle` does not only store
data: a file can also say **which Python function to call** while it is being
loaded. So blindly loading a model file from someone else can mean running
that person's code on your own computer.

`weights_only=True` puts the loader in a strict mode: it allows only tensors,
numbers, strings, lists and dictionaries, and builds no other object. Since
PyTorch 2.6 this is the default. Let us see what happens to a file that
carries an unusual object:

```python
class Note:
    def __init__(self, text):
        self.text = text


torch.save({"weights": model.state_dict(), "note": Note("hello")}, "odd.pt")
try:
    torch.load("odd.pt", weights_only=True)
except Exception as error:
    print(type(error).__name__)
    print(str(error).split(".")[0])
```

```text
UnpicklingError
Weights only load failed
```

- The file was refused; the `Note` object in it was not built.
- The error message says loading with `weights_only=False` is possible, but
  should be done **only if you trust the source of the file**. Even for a file
  you wrote yourself, try the state_dict way first.
- The rule: load a model file from someone else only with
  `weights_only=True`; where possible, prefer formats that store only tensors
  (such as `safetensors`).

<figure class="fig">
  <div class="versus">
    <div class="ok"><h5>state_dict + weights_only=True</h5>The file holds only numbers; the loader builds no other object. The model is rebuilt in code.</div>
    <div class="no"><h5>weights_only=False</h5>Python objects can be built while the file loads; for an untrusted file, that means running code.</div>
  </div>
  <figcaption>The left one is the default way to share and load models.</figcaption>
</figure>

## A checkpoint: resuming where you stopped

A long training run can be interrupted. To resume it **exactly** where it
stopped, we save not only the model but also the optimizer's state and the
epoch number. Adam keeps moving averages for every parameter (the
Optimisation section); if they are lost, training does not continue down the
same path:

```python
X = torch.randn(64, 4)
Y = torch.randint(0, 3, (64,))


def make():
    torch.manual_seed(0)
    net = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3))
    return net, torch.optim.Adam(net.parameters(), lr=0.01)


def train(net, optimizer, epochs):
    for _ in range(epochs):
        optimizer.zero_grad()
        nn.functional.cross_entropy(net(X), Y).backward()
        optimizer.step()


net, optimizer = make()
train(net, optimizer, 4)
straight = net[0].weight.clone()

net, optimizer = make()
train(net, optimizer, 2)
torch.save({"epoch": 2, "model": net.state_dict(),
            "optimizer": optimizer.state_dict()}, "checkpoint.pt")

checkpoint = torch.load("checkpoint.pt", weights_only=True)
net, optimizer = make()
net.load_state_dict(checkpoint["model"])
optimizer.load_state_dict(checkpoint["optimizer"])
train(net, optimizer, 2)
print(checkpoint["epoch"], torch.equal(straight, net[0].weight))

net, optimizer = make()
net.load_state_dict(checkpoint["model"])
train(net, optimizer, 2)
print(torch.equal(straight, net[0].weight))
print(list(checkpoint["optimizer"]["state"][0].keys()))
```

```text
2 True
False
['step', 'exp_avg', 'exp_avg_sq']
```

- With the model + optimizer loaded, 2 + 2 epochs gave exactly the same as 4
  epochs (`True`).
- With only the model loaded, Adam's averages started from zero and the
  weights came out different (`False`).
- For every parameter Adam stores the step count (`step`) and two moving
  averages (`exp_avg`, `exp_avg_sq`). If you use a learning rate scheduler,
  its `state_dict()` goes into the checkpoint too.
- A checkpoint is an ordinary dictionary as well; it can be loaded with
  `weights_only=True`.

## Summary

- `model.state_dict()` gives the parameters as a name → tensor dictionary;
  `torch.save` writes it to disk.
- Loading: build the same model in code, then `load_state_dict(torch.load(path,
  weights_only=True))`.
- A `pickle` file can run code while loading; do not use `weights_only=False`
  on a file from someone else.
- To resume training, save the model, the optimizer (and scheduler) state and
  the epoch number together.
