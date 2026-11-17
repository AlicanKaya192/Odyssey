In the lesson we chose **a single scale** for the whole tensor. For a weight
whose rows have very different sizes this is bad: the largest row sets the
scale, and all the rows with small values get squeezed into a few steps. The
remedy is to give every row (every output channel) **its own scale**.

```python
import torch

gen = torch.Generator().manual_seed(0)
w = torch.randn(4, 8, generator=gen) * torch.tensor([[0.1], [1.0], [5.0], [0.5]])


def quantize(w, scale):
    return torch.round(w / scale).clamp(-127, 127) * scale


per_tensor = quantize(w, w.abs().max() / 127)
per_row = quantize(w, w.abs().amax(dim=1, keepdim=True) / 127)
print(bool((w - per_row).abs()[0].max() < (w - per_tensor).abs()[0].max() / 10))
```

```text
True
```

- The rows of `w` are on different scales, between 0.1 and 5.
- With a single scale the error of the first row (smallest values) is more
  than ten times the error with a scale per row.
- A scale per row means one more number per row; in a 64-row layer that is 64
  numbers, negligible next to the weight. This is why **per-channel**
  quantisation is the default for convolution and linear layers.

## The zero point

After a ReLU the activations are always positive. Symmetric quantisation (-127
to 127) reserves half of the range for negative values that never come.
**Asymmetric** quantisation spreads `uint8`'s range 0–255 over the values'
real range, and records which integer the real 0 falls on with a **zero
point**: `real = scale · (q − zero_point)`.

```python
a = torch.rand(1000, generator=gen) * 6
symmetric = a.abs().max() / 127
asymmetric = (a.max() - a.min()) / 255
print(bool(asymmetric < symmetric))
```

```text
True
```

The asymmetric scale is smaller, so the steps are finer: less rounding error
with the same 8 bits. Since weights spread on both sides of zero, weights are
usually quantised symmetrically and activations asymmetrically.
