We can find the last real step of a padded sequence without packing too:
since `out` holds the state of every step, picking position `length − 1`
from each sequence is enough. This uses indexing with two indices: the first
says which sequence, the second which step.

```python
import torch
from torch import nn

torch.manual_seed(0)
lstm = nn.LSTM(4, 3, batch_first=True, bidirectional=True)
x = torch.randn(3, 6, 4)
lengths = torch.tensor([6, 4, 2])
out, (h, c) = lstm(x)
last = out[torch.arange(3), lengths - 1]
print(tuple(out.shape), tuple(last.shape))
print(torch.allclose(out[:, -1, :3], h[-2]))
print(torch.allclose(out[:, 0, 3:], h[-1]))
summary = torch.cat([h[-2], h[-1]], dim=1)
print(tuple(summary.shape))
```

```text
(3, 6, 6) (3, 6)
True
True
(3, 6)
```

- `out[torch.arange(3), lengths - 1]`: step 5 of sequence 0, step 3 of
  sequence 1, step 1 of sequence 2. The result is `(3, 6)`.
- In a bidirectional network the first 3 numbers of `out` are the forward
  direction and the last 3 the backward direction. The forward direction
  ends at the **last** step (`h[-2]`), the backward direction at the
  **first** step (`h[-1]`, because it reads from right to left). The two
  `True`s show this.
- Putting the two side by side is a common bidirectional summary: `(B, 2H)`.

## Careful: bidirectional networks and padding

The backward direction reads the sequence from end to start. On a padded
sequence the "end" is the end of the padding: the backward direction reads
the pads first and spoils the summary. The `x` above had no padding; on real
padded data **always** give a bidirectional network packed input. In the
forward direction, picking the last real step gives the same result as
packing.

| Situation | For the last state |
|---|---|
| One direction, padded | Pack, or `out[arange(B), lengths - 1]` |
| Two directions, padded | Pack (`pack_padded_sequence`) |
| No padding | `h[-1]` (bidirectional: `h[-2]`, `h[-1]`) |
