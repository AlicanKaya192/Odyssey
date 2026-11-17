The strength of attention is that every position looks at every position;
so is its price. The weight matrix is `(T, T)`: when the sequence length
grows 10 times, the matrix grows 100 times. In an LSTM the work per step is
constant and the total work grows in proportion to the length.

```python
import torch
from torch import nn

for T in (100, 1000, 10000):
    print(T, T * T)

lstm = nn.LSTM(32, 32, batch_first=True)
block = nn.TransformerEncoderLayer(32, nhead=4, dim_feedforward=64, batch_first=True)
print(sum(p.numel() for p in lstm.parameters()))
print(sum(p.numel() for p in block.parameters()))
```

```text
100 10000
1000 1000000
10000 100000000
8448
8544
```

- In a sequence of 10,000 steps one head's weight matrix holds 100 million
  numbers: 400 MB in `float32`, and separately for every head and every
  example. That is why, for long audio and sensor recordings, shortening the
  sequence with a convolution first is common.
- The parameter counts are close; the difference is not in the parameters
  but in how the computation grows with length.

| | LSTM | Transformer |
|---|---|---|
| Work with length | Proportional (T) | Quadratic (T²) |
| Parallelism | Steps in order | All positions at once |
| Distant dependencies | Through the state, fading | In one step |
| Order information | By itself | Given with a positional embedding |
| With a lot of data | Improves more slowly | Usually scales better |

On short sequences and little data the two are close; large text models
became possible thanks to the Transformer's parallelism.
