`uint8` pixels behave silently or unexpectedly in three places:

```python
import torch

x = torch.tensor([10, 250], dtype=torch.uint8)
print((x - 20).tolist())
try:
    x.mean()
except RuntimeError as error:
    print(type(error).__name__)
print(x.float().mean().item())
print((x.to(torch.int16) - 20).tolist())
```

```text
[246, 230]
NotImplementedError
130.0
[-10, 230]
```

- **Subtraction wraps around:** `10 − 20` cannot be negative, so it becomes
  246. No error. Change the type before computing brightness differences,
  edges and the like.
- **The mean raises an error:** `mean` does not work on an integer type
  (`NotImplementedError`; it is a kind of `RuntimeError`, so
  `except RuntimeError` catches it too). Use `float()` first.
- **A wider type:** `int16` holds negative values too; but the network still
  needs `float32`.

Rule: convert a picture read from a file to `float32` first and scale it to
[0, 1]; do all the remaining arithmetic there. When saving, limit the values
with `clamp(0, 1)` before going back to `uint8`, otherwise values above 1 wrap
around too.
