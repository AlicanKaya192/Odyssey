When handing a model to someone else, the `.pt2` file alone is not enough.
The other side also needs to know: how many features the input has, which
class each output column is, and how to verify that the file in their hands
gives **the same result** as yours. A small delivery package is three files:
the model, a description, and an example input and output (the "golden"
output).

```python
import json
import torch
from torch import nn

torch.manual_seed(0)
model = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3)).eval()
example = torch.randn(5, 4, generator=torch.Generator().manual_seed(1))
batch = torch.export.Dim("batch")
ep = torch.export.export(model, (example,), dynamic_shapes=({0: batch},))
torch.export.save(ep, "model.pt2")
meta = {"classes": ["low", "mid", "high"], "features": 4}
with torch.no_grad():
    golden = {"input": example.tolist(), "output": model(example).tolist()}
with open("meta.json", "w") as f:
    json.dump(meta, f)
with open("golden.json", "w") as f:
    json.dump(golden, f)
print(sorted(meta), len(golden["output"]))
```

```text
['classes', 'features'] 5
```

- `dynamic_shapes=({0: batch},)`: it can also be given by position instead of
  the argument name; here dimension 0 of the single argument is free.
- `meta.json` carries the information outside the model; `golden.json` a
  fixed input and the output the model gave for it.

The other side's code loads the model without knowing its class, checks the
golden output first, then predicts:

```python
loaded = torch.export.load("model.pt2").module()
with open("meta.json") as f:
    meta = json.load(f)
with open("golden.json") as f:
    golden = json.load(f)
out = loaded(torch.tensor(golden["input"]))
print(torch.allclose(out, torch.tensor(golden["output"]), atol=1e-5))
labels = [meta["classes"][i] for i in out.argmax(dim=1).tolist()]
print(len(labels), set(labels) <= set(meta["classes"]))
```

```text
True
5 True
```

- The golden-output check tests three things at once: the right file, the
  right version, the right loading. If it fails, do not go on to predict.
- `atol=1e-5`: on another machine or another PyTorch version the last digits
  may change; exact equality is not expected.

In this module's reproducibility section we will put the package behind a
prediction function; the "Serving an ML Model" section of the Writing REST
APIs with FastAPI module puts the same kind of package behind a web
endpoint.
