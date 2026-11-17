In the lesson all sequences had the same length. Real text is not like that;
then the model must take the lengths too and give the LSTM packed input. A
good test for a good model: **adding extra padding to the same sequence must
not change the result.**

```python
import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence


class PackedClassifier(nn.Module):
    def __init__(self, vocab, dim=8, hidden=16):
        super().__init__()
        self.emb = nn.Embedding(vocab, dim, padding_idx=0)
        self.lstm = nn.LSTM(dim, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 2)

    def forward(self, x, lengths):
        packed = pack_padded_sequence(self.emb(x), lengths, batch_first=True,
                                      enforce_sorted=False)
        out, (h, c) = self.lstm(packed)
        return self.head(h[-1])


torch.manual_seed(0)
model = PackedClassifier(vocab=20)
seq = torch.tensor([[4, 7, 2]])
short = nn.functional.pad(seq, (0, 2))
long = nn.functional.pad(seq, (0, 9))
lengths = torch.tensor([3])
print(tuple(short.shape), tuple(long.shape))
with torch.no_grad():
    print(torch.allclose(model(short, lengths), model(long, lengths)))
    plain_short = model.lstm(model.emb(short))[1][0]
    plain_long = model.lstm(model.emb(long))[1][0]
    print(torch.allclose(plain_short, plain_long))
```

```text
(1, 5) (1, 12)
True
False
```

- `nn.functional.pad(seq, (0, 2))` adds two 0s to the end of the last
  dimension.
- In the packed model 2 or 9 pads give the same result (`True`).
- The unpacked LSTM's last state changes with the number of pads (`False`):
  the length chosen by whoever builds the batch changes the model's answer,
  which is a bug.

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| `lengths` on the GPU | `pack_padded_sequence` raises an error | Lengths stay on the CPU as `int64` |
| A sequence of length 0 | Packing raises an error | Remove empty examples from the data |
| Not packing in two directions | The backward direction reads padding first | Always pack |
| No `padding_idx` | The padding vector is learned | Harmless in a packed model, but a problem in a masked mean |
