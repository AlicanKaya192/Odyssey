Exporting traces the model **with one example input**. If the model has an
`if` that depends on the input's value, tracing sees the branch that example
takes and never sees the other. The old `torch.jit.trace` silently accepts
this:

```python
import warnings
import torch
from torch import nn

warnings.simplefilter("ignore")


class Branchy(nn.Module):
    def forward(self, x):
        if x.sum() > 0:
            return x * 2
        return x * -1


model = Branchy()
pos, neg = torch.ones(3), -torch.ones(3)
traced = torch.jit.trace(model, pos)
print(model(neg).tolist(), traced(neg).tolist())
```

```text
[1.0, 1.0, 1.0] [-2.0, -2.0, -2.0]
```

- Tracing was done with a positive input; the recorded computation is
  "multiply by two". On the negative input the real model says `x * -1`
  (`1.0`), the traced model still multiplies by two (`-2.0`). No error, and
  with the warnings suppressed no trace at all: a wrong result.
- `warnings.simplefilter("ignore")` is here only to keep the output clean; in
  real code do not suppress `trace`'s warnings, they say exactly this.

`torch.export` does not accept the same model; it sees that the branch depends
on the data and raises an error. If both branches are needed, write it with
`torch.cond`:

```python
try:
    torch.export.export(model, (pos,))
except Exception as e:
    print(type(e).__name__)


class CondNet(nn.Module):
    def forward(self, x):
        return torch.cond(x.sum() > 0, lambda t: t * 2, lambda t: t * -1, (x,))


ep = torch.export.export(CondNet(), (pos,))
print(ep.module()(pos).tolist(), ep.module()(neg).tolist())
```

```text
GuardOnDataDependentSymNode
[2.0, 2.0, 2.0] [1.0, 1.0, 1.0]
```

- The error's name is long but its meaning is clear: "I cannot build a guard
  on a data-dependent expression".
- `torch.cond(condition, if_true, if_false, (inputs,))` puts both branches
  into the graph; the exported model is correct on both inputs.

After exporting, always compare the model with the original on **several
different inputs**. The same holds for branching on shapes (batch size,
sequence length): when choosing the example for export, think about which
shapes will be used.
