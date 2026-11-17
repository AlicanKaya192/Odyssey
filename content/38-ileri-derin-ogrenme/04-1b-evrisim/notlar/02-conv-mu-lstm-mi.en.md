The two layer families want the same data in different layouts; switching
between them is a single `transpose`.

```python
import torch
from torch import nn

torch.manual_seed(0)
x = torch.randn(4, 64, 3)
lstm = nn.LSTM(3, 8, batch_first=True)
conv = nn.Conv1d(3, 8, kernel_size=5, padding=2)
out_lstm, _ = lstm(x)
out_conv = conv(x.transpose(1, 2))
print(tuple(out_lstm.shape), tuple(out_conv.shape))
print(tuple(out_conv.transpose(1, 2).shape))
n_lstm = sum(p.numel() for p in lstm.parameters())
print(n_lstm, sum(p.numel() for p in conv.parameters()))
```

```text
(4, 64, 8) (4, 8, 64)
(4, 64, 8)
416 128
```

- `x` is in LSTM layout `(B, T, D)`: 4 recordings, 64 steps, 3 axes.
  `transpose(1, 2)` makes it `(B, D, T)`; the convolution's output can be
  turned back the same way.
- Without `transpose`, `Conv1d` takes 64 for the channel count and raises an
  error saying it expected 3 channels; that error is the good case. The bad
  case is when the channel count happens to equal the time length: no error,
  a wrong result.

## Which one to choose?

| | 1D convolution | LSTM / GRU |
|---|---|---|
| Computation | All positions in parallel, fast | Step by step, sequential |
| What it sees | A local window as wide as the receptive field | In principle the whole past |
| Good at | Local patterns: a jump, vibration, a sound event | Order and long dependencies |
| Position | Recognises a pattern anywhere | Carries position in its state |

They are also used together: a few convolution layers first pull out local
patterns and shorten the sequence (`stride` or pooling), then an LSTM reads
this short summary sequence.
