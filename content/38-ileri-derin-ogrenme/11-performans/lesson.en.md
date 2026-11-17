# Performance and Profiling

The model works correctly but slowly. The first rule: **do not guess,
measure.** Where the slowness is usually is not where you think; often it is
not the model itself but the Python code around it. In this section we look
at measuring time, profiling, and a few tools PyTorch offers for speed and
memory.

Times change from machine to machine; so in the outputs below we print no
times, only **comparisons**. The comparisons have wide margins: on this
computer the differences are tens of times.

## A batch, not a loop

```python
import time
import torch
from torch import nn


def timeit(fn, repeat=5):
    best = float("inf")
    for _ in range(repeat):
        start = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - start)
    return best


torch.manual_seed(0)
model = nn.Sequential(nn.Linear(64, 128), nn.ReLU(), nn.Linear(128, 10)).eval()
x = torch.randn(512, 64)
with torch.no_grad():
    loop = timeit(lambda: [model(row) for row in x])
    batch = timeit(lambda: model(x))
print(batch < loop / 10)
```

```text
True
```

- `time.perf_counter()` is the most precise wall-clock timer; use it, not
  `time.time()`, to measure durations.
- `timeit` does the same job several times and takes **the shortest**: so
  that the set-up of the first call and other work in the background do not
  inflate the measurement.
- Giving the 512 rows to the model one by one is more than ten times slower
  than giving them all as a single `(512, 64)` tensor (tens of times on this
  computer). Every call has a fixed cost in Python and PyTorch; a batch pays
  it once and leaves the computation to an optimised matrix product.

## `no_grad` and `inference_mode`

```python
y = model(x)
print(y.requires_grad, y.grad_fn is not None)
with torch.inference_mode():
    z = model(x)
print(z.requires_grad, z.grad_fn is None, z.is_inference())
```

```text
True True
False True True
```

- In a normal call PyTorch builds the computation graph for backpropagation
  and keeps intermediate results in memory (`grad_fn`).
- When predicting there is no need for this. `torch.no_grad()` does not build
  the graph; `torch.inference_mode()` goes one step further and marks the
  resulting tensors as "prediction only", so PyTorch skips some internal
  bookkeeping as well.
- The gain is above all **memory**. In a small model the speed difference may
  be too small to measure; it becomes clear with a large model and a large
  batch.

## Memory: parameters and the number type

```python
params = sum(p.numel() for p in model.parameters())
print(params, params * 4, params * 2)
with torch.autocast("cpu", dtype=torch.bfloat16):
    print(model(x).dtype)
```

```text
9610 38440 19220
torch.bfloat16
```

- The model has 9610 parameters. A `float32` number is 4 bytes; a `bfloat16`
  2 bytes. The parameters' memory halves directly with the type.
- `torch.autocast` is a mixed-precision mode: inside it operations such as
  matrix products run in the smaller type, while precision-sensitive ones
  (sums, losses) stay in `float32`. The output is `bfloat16`. On a graphics
  card the same is done with `torch.autocast("cuda", dtype=torch.float16)`,
  and the speed gain is much larger than on the CPU.

## Profiling: where does the time go?

`torch.profiler` records every PyTorch operation and the labelled sections
you give it. Below we measure a (slow) preparation step that normalises the
data row by row and the model under separate labels.

```python
from torch.profiler import profile, ProfilerActivity, record_function

with profile(activities=[ProfilerActivity.CPU]) as prof:
    with record_function("prepare"):
        rows = torch.stack([(r - r.mean()) / r.std() for r in x])
    with record_function("model"):
        with torch.no_grad():
            model(rows)
events = {e.key: e for e in prof.key_averages()}
print(sorted(k for k in events if k in ("prepare", "model", "aten::linear")))
print(events["prepare"].cpu_time_total > events["model"].cpu_time_total)
```

```text
['aten::linear', 'model', 'prepare']
True
```

- `record_function("name")` names a section; it shows up in the profile under
  that name. `aten::linear` is the internal operation PyTorch calls for a
  linear layer.
- The result is the opposite of the guess: **running the model is faster than
  preparing the data**. Instead of normalising row by row,
  `(x - x.mean(1, keepdim=True)) / x.std(1, keepdim=True)` does it in one
  line, as a batch.
- To see the whole table, print
  `prof.key_averages().table(sort_by="cpu_time_total", row_limit=10)`; we do
  not show it here because it contains times.

## `torch.compile`

`torch.compile(model)` traces the model and passes it through a compiler that
merges operations and generates faster code. The default back end (inductor)
needs a C++ compiler on the machine; on Windows, if Visual Studio's compiler
is not installed, it fails on the first call (`cl is not found` on this
computer). `backend="eager"` needs no compiler: it runs only the tracing
part, gives no speed-up, but checks that the code is fit for compiling.

```python
compiled = torch.compile(model, backend="eager")
with torch.no_grad():
    print(torch.equal(compiled(x), model(x)))
```

```text
True
```

Compiling takes time on the first call, and the gain depends on the model,
the hardware and the batch size: do not say "it got faster" without
measuring.

## Summary

- Measure first: `time.perf_counter`, the shortest of several repeats;
  compare ratios, not times.
- A batch, not row by row: the fixed cost is paid once.
- For prediction `torch.inference_mode()` (or `no_grad`): no graph, less
  memory.
- `bfloat16` / `autocast`: memory halves.
- `torch.profiler` + `record_function`: see where the time goes.
- `torch.compile` needs a compiler; measure its gain.
