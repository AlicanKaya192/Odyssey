# Exporting a Model

In the Deep Learning Fundamentals module we saved the model with a
`state_dict`. That file carries only the **numbers**: to load it you also need
the Python code that writes the model's class. When you want to send the model
to another program, a server or a phone, that is not enough. **Exporting**
writes the model's computation too (which operation in which order) into the
file; the program that opens the file does not need to know your class.

<figure class="fig">
<div class="flow">
<span class="node">nn.Module</span><span class="arrow">→</span>
<span class="node acc">torch.export</span><span class="arrow">→</span>
<span class="node">computation graph</span><span class="arrow">→</span>
<span class="node ok">model.pt2</span>
</div>
<figcaption>Exporting runs the model once with an example input, records the operations it performs and writes them, together with the weights, into a single file.</figcaption>
</figure>

In PyTorch the current way to do this is `torch.export`. We mention the old
way, TorchScript, and ONNX, the common format between programs, at the end
of the section.

## `torch.export`

```python
import torch
from torch import nn


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.body = nn.Sequential(nn.Linear(8, 16), nn.ReLU(), nn.Linear(16, 2))

    def forward(self, x):
        return self.body(x)


torch.manual_seed(0)
model = Net().eval()
x = torch.randn(4, 8)
ep = torch.export.export(model, (x,))
print(type(ep).__name__, torch.allclose(ep.module()(x), model(x)))
ops = [str(n.target) for n in ep.graph.nodes if n.op == "call_function"]
print([op.removeprefix("aten.") for op in ops])
```

```text
ExportedProgram True
['linear.default', 'relu.default', 'linear.default']
```

- `torch.export.export(model, (x,))` traces the model with the example input
  `x`. The result is an `ExportedProgram`: the weights and the graph of
  operations.
- `ep.module()` turns the graph back into a callable module; its output is the
  same as the original model's.
- The operations in the graph are PyTorch's basic operations (their names
  start with `aten.`; we dropped it to keep them short): two linear layers
  with a ReLU between them. Python structures such as `nn.Sequential` and
  `Net` are not in the graph; only the computation is left.

## Freeing the batch size

The example input's shape is also recorded during tracing. What happens when
we call it with another batch size?

```python
try:
    ep.module()(torch.randn(7, 8))
except Exception as e:
    print(type(e).__name__, "Guard failed" in str(e))

batch = torch.export.Dim("batch")
ep = torch.export.export(model, (x,), dynamic_shapes={"x": {0: batch}})
print(ep.module()(torch.randn(7, 8)).shape, ep.module()(torch.randn(1, 8)).shape)
```

```text
AssertionError True
torch.Size([7, 2]) torch.Size([1, 2])
```

- The first export **fixed** the batch size at 4; the 7-row input failed the
  "guard" check.
- With `torch.export.Dim("batch")` dimension 0 is free: the key of the
  `dynamic_shapes` dictionary is `forward`'s argument name (`x`), the value
  says which dimension is free. Now 7 and 1 both work.
- In a model that will be served the batch size is almost always freed.

## Saving and loading without the class

```python
torch.export.save(ep, "model.pt2")
del Net, model
loaded = torch.export.load("model.pt2").module()
print(type(loaded).__name__, loaded(x).shape)
```

```text
GraphModule torch.Size([4, 2])
```

- With `del Net` we even deleted the class; loading still worked. The program
  that opens the file needs only PyTorch.
- The `.pt2` file is a zip archive: the weights, the graph and the shape rules
  are inside.

## Old and common formats

**TorchScript** (`torch.jit.trace`, `torch.jit.script`) is PyTorch's old way
of exporting. In the version on this computer (PyTorch 2.15, Python 3.14) both
warn "not supported in Python 3.14+, switch to `torch.export`"
(`FutureWarning`). `torch.jit.script` also has to read the model's Python
source code; it does not work where there is no source (only compiled `.pyc`
files). New code uses `torch.export`; in the notes we will see a silent trap
of `trace`.

**ONNX** is a model format shared by different frameworks and runtimes: a
model trained in PyTorch can be exported to ONNX and used in another language
or on a device with a special runtime. PyTorch's ONNX exporter needs extra
packages (`onnx`, `onnxscript`); since they are not installed in this program,
we only show the code:

```
torch.onnx.export(model, (x,), "model.onnx", dynamo=True,
                  dynamic_shapes={"x": {0: torch.export.Dim("batch")}})
```

As you can see, the ONNX exporter also uses `torch.export` underneath: the
shape rules are the same.

## Summary

- A `state_dict` carries numbers and needs the class code; exporting also
  carries the computation.
- `torch.export.export(model, (example,))` → `ExportedProgram`; `.module()` is
  callable.
- Unless freed with `Dim`, the batch size is fixed to the example input's.
- `torch.export.save` / `load`: `.pt2`, loads without the class.
- TorchScript is outdated; ONNX needs extra packages and uses the same route
  underneath.
