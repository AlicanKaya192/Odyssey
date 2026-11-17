Padding is not free: every padding position is computed in the network like
a real word and then thrown away with the mask. If we batch sequences of very
different lengths at random, a 3-word sentence in a batch is padded to the
length of a 29-word one. **Sorting the sequences by length** before batching
cuts this wasted work.

```python
import numpy as np

rng = np.random.default_rng(0)
lengths = rng.integers(3, 30, 64).tolist()


def padding(lengths, size):
    total = 0
    for i in range(0, len(lengths), size):
        group = lengths[i:i + size]
        total += max(group) * len(group) - sum(group)
    return total


print(sum(lengths))
print(padding(lengths, 8), padding(sorted(lengths), 8))
```

```text
1042
654 78
```

The 64 sequences hold 1042 real words in total. Batched in the
order they come, 654 padding positions are computed; in sorted
batches only 78. In training the order of the batches is still
shuffled every epoch; only the members of one batch are chosen with similar
lengths (bucketing by length).

## A way without padding: `nn.EmbeddingBag`

If all you want is the mean of a sequence's embeddings, there is no need for
padding at all. `nn.EmbeddingBag` takes all ids in one long list; `offsets`
says where each sequence starts.

```python
import torch
from torch import nn

torch.manual_seed(0)
bag = nn.EmbeddingBag(10, 4, mode="mean")
ids = torch.tensor([3, 5, 7, 2, 2])
offsets = torch.tensor([0, 3])
out = bag(ids, offsets)
print(out.shape)
print(torch.allclose(out[0], bag.weight[[3, 5, 7]].mean(dim=0)))
```

```text
torch.Size([2, 4])
True
```

There are two sequences: `[3, 5, 7]` and `[2, 2]`. The result is one vector
per sequence; the first is the same as the mean of the three rows. When word
order does not matter (bag-of-words models) this is the short, fast road to a
masked mean. Networks where order matters (LSTM, Transformer) need the padded
`(B, T, D)` tensor instead.
