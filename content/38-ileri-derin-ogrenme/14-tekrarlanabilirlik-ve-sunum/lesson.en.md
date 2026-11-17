# Reproducibility and Serving a Model

An experiment's result is trustworthy only if it can be **reproduced**. If you
say "it was 91% yesterday, 87% today", you need to know what changed between
the two runs. The first half of this section makes the same code give the
same result; the second half puts the trained model behind a **prediction
function** that someone else can use.

## Seeds

Randomness in training comes from many places: the initial weights, the
shuffling of the data, dropout, data augmentation. Let us fix all their seeds
in a single function:

```python
import json
import random
import numpy as np
import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_table


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


x, y = map(torch.tensor, make_table(600, seed=7))


def train(seed, epochs=10):
    set_seed(seed)
    model = nn.Sequential(nn.Linear(6, 32), nn.ReLU(), nn.Dropout(0.2),
                          nn.Linear(32, 3))
    loader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(x[:500], y[:500]), batch_size=50, shuffle=True,
        generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.Adam(model.parameters(), lr=0.01)
    for _ in range(epochs):
        model.train()
        for xb, yb in loader:
            opt.zero_grad()
            F.cross_entropy(model(xb), yb).backward()
            opt.step()
    return model.eval()


def same(a, b):
    return all(torch.equal(p, q) for p, q in zip(a.parameters(), b.parameters()))


print(same(train(0), train(0)), same(train(0), train(1)))
```

```text
True False
```

- Two trainings with the same seed gave **bit-for-bit identical** weights; with
  a different seed, different ones.
- The `DataLoader`'s shuffling order comes from its own `generator`; we seeded
  that too. Dropout is affected by `torch.manual_seed`.
- `random` and `np.random` are not used in this code, but a data augmentation
  library might use them; fixing all three should be a habit.

The same result on the same machine does **not** mean the same result on
another machine. Different processors may do floating-point computations in a
different order; in long trainings the weights drift apart in the last digits.
This is why this program's contents print results far from a boundary, such
as accuracy, and not weight values.

## Deterministic algorithms

Some operations (mostly on graphics cards) have versions that are fast but
give **slightly different results on every run**.
`torch.use_deterministic_algorithms(True)` tells PyTorch to use only the
deterministic versions; an operation without such a version raises an error
instead of running silently.

```python
torch.use_deterministic_algorithms(True)
print(torch.are_deterministic_algorithms_enabled(), same(train(0), train(0)))
torch.use_deterministic_algorithms(False)
```

```text
True True
```

On the CPU almost every operation is deterministic already; the setting
matters mainly on a graphics card (where the `CUBLAS_WORKSPACE_CONFIG`
environment variable is also required). The price is some speed; it is
switched on while debugging and when reporting results.

## An experiment record

The other half of reproducibility is **writing down what you did**: which
settings, which seed, which data, which result. A dictionary and a JSON file
are enough:

```python
def accuracy(model):
    with torch.no_grad():
        return (model(x[500:]).argmax(1) == y[500:]).float().mean().item()


config = {"seed": 0, "epochs": 10, "lr": 0.01, "hidden": 32, "dropout": 0.2}
model = train(config["seed"], config["epochs"])
record = {"config": config, "torch": torch.__version__,
          "metrics": {"test_accuracy": accuracy(model)}}
with open("run-001.json", "w") as f:
    json.dump(record, f, indent=2)
with open("run-001.json") as f:
    loaded = json.load(f)
print(sorted(loaded), loaded["config"] == config)
print(loaded["metrics"]["test_accuracy"] > 0.8)
```

```text
['config', 'metrics', 'torch'] True
True
```

- The record also has PyTorch's version: when the version changes, the result
  may change.
- Real projects add a summary of the data (a hash), the git version of the
  code and the duration; in the notes we look at the data hash.

## Wrapping the model in a function

The person using the model should not have to know PyTorch, tensors or
`argmax`. We give them a plain **prediction function**: it takes a Python
list and returns a dictionary; it loads the model once and checks the input.

```python
CLASSES = ["low", "mid", "high"]


def predict(values):
    if len(values) != 6:
        raise ValueError(f"expected 6 values, got {len(values)}")
    with torch.inference_mode():
        logits = model(torch.tensor([values], dtype=torch.float32))
        probs = torch.softmax(logits, dim=1)[0]
    best = int(probs.argmax())
    return {"label": CLASSES[best], "probability": round(probs[best].item(), 2)}


answer = predict([1.5, 1.0, 0.0, 0.0, 1.0, 0.0])
print(answer["label"], 0.5 < answer["probability"] <= 1.0)
try:
    predict([1.0, 2.0])
except ValueError as e:
    print(e)
```

```text
mid True
expected 6 values, got 2
```

- The model is built **outside** the function, once; it is not reloaded on
  every request.
- The input's length is checked first; a wrong input is turned away with a
  clear message instead of PyTorch's cryptic shape error.
- The return value is a dictionary: the label's name and its probability. The
  calling code does not need to see a tensor.

This function is now ready to be put behind a web endpoint. The "Serving an
ML Model" section of the Writing REST APIs with FastAPI module does exactly
that; there it looks roughly like this (we do not start a server here):

```
@app.post("/predict")
def predict_endpoint(item: Features):
    return predict(item.values)
```

## Summary

- `set_seed`: `random`, `numpy`, `torch` all three; the `DataLoader` gets its
  own `generator`.
- The same seed gives the same result on the same machine; on another machine
  the last digits may change.
- `torch.use_deterministic_algorithms(True)`: a non-deterministic operation
  raises an error.
- Record every run: settings, seed, version, result.
- When serving, load the model once, check the input, return a plain
  dictionary.
