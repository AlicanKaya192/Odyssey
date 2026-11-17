In the Embeddings and Language Models module we wrote the LSTM cell as
`c = f · c + i · g`: the forget gate `f` says how much of the old content
stays, the input gate `i` says how much of the new information (`g`) is
written; the output gate `o` chooses what passes from the cell to the hidden
state. PyTorch computes the four parts with one matrix product and then
splits them into four. For a single step there is `nn.LSTMCell`; let us
write the formula by hand and compare it with that.

```python
import torch
from torch import nn

torch.manual_seed(0)
cell = nn.LSTMCell(4, 3)
x = torch.randn(2, 4)
h, c = torch.zeros(2, 3), torch.zeros(2, 3)
z = x @ cell.weight_ih.T + cell.bias_ih + h @ cell.weight_hh.T + cell.bias_hh
i, f, g, o = z.chunk(4, dim=1)
c_new = torch.sigmoid(f) * c + torch.sigmoid(i) * torch.tanh(g)
h_new = torch.sigmoid(o) * torch.tanh(c_new)
h_ref, c_ref = cell(x, (h, c))
print(z.shape)
print(torch.allclose(h_new, h_ref), torch.allclose(c_new, c_ref))
```

```text
torch.Size([2, 12])
True True
```

- `z` is `(2, 12)`: the pre-activations of the four gates side by side.
  PyTorch's order is **input, forget, candidate, output** (`i, f, g, o`). If
  you touch part of the weights by hand (like the tip below), you need to
  know this order.
- The gates go through a sigmoid ("how much", between 0 and 1), the
  candidate `g` through tanh ("what", between −1 and 1).
- Two `True`s: the four-line hand computation matches the layer itself.

## When `LSTMCell`?

| Layer | What it does | When |
|---|---|---|
| `nn.LSTM` | Reads the whole sequence in one call, fast | Almost always |
| `nn.LSTMCell` | One step; you write the loop | When something has to happen between steps: feeding the previous output back in, deciding step by step |

A well-known initialisation tip: pulling the forget gate's bias to a positive
value such as 1 at the start keeps the network from erasing its memory early
in training. In the bias, the forget gate's slice is `[H:2H]`.
