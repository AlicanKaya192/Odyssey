This program runs PyTorch on the CPU. Real training is usually done on a
graphics card (GPU); on Macs the computer's own graphics unit (`mps`) can also be
used.
Writing the code **device-independent** from the start lets the same file
run everywhere.

```python
import torch
from torch import nn

if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")

model = nn.Linear(8, 2).to(device)
x = torch.randn(4, 8).to(device)
print(model(x).shape)
print(next(model.parameters()).device.type in ("cpu", "cuda", "mps"))
```

```text
torch.Size([4, 2])
True
```

- The model and the data must be **on the same device**; if one is on the CPU
  and the other on the GPU, PyTorch raises an error. `.to(device)` moves both.
- Which device is chosen depends on the machine; the output prints only the
  shape and that the device is one of the known kinds.

## Things to watch on a GPU

- **Transfer cost:** copying data between the CPU and the GPU is slow. Move
  data batch by batch instead of shuttling small pieces back and forth at
  every step; do not pull results back to the CPU with `.item()` at every
  step.
- **`DataLoader(pin_memory=True)`:** keeps data in memory ready for copying;
  together with `.to(device, non_blocking=True)` the copy overlaps with the
  computation.
- **The timing trap:** the GPU queues work and returns at once. If
  `torch.cuda.synchronize()` is not called when measuring time, what you
  measure is the queueing time, not the work itself.
- **Batch size:** a GPU is efficient with large batches; a batch as large as
  memory allows is often faster. If memory runs out, mixed precision
  (`autocast`) is the first thing to try.
