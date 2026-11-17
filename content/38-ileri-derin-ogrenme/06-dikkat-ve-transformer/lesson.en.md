# Attention and the Transformer

In the Embeddings and Language Models module we built attention and the
Transformer block from scratch with NumPy. In short: every position produces
a **query**, looks at its similarity with the **keys** of all positions,
turns those similarities into weights with a softmax, and takes the weighted
mean of the positions' **values**. All positions are computed at once; two
distant words see each other in one step. A Transformer block stacks
attention, a feed-forward network, residual connections and layer
normalisation.

In PyTorch these are ready-made: `nn.MultiheadAttention`,
`F.scaled_dot_product_attention`, `nn.TransformerEncoderLayer`. In this
section we see their formats, the two masks (padding and future) and why the
Transformer needs **position information**, and we train a small Transformer
on an order-dependent task.

## `nn.MultiheadAttention`

```python
import torch
from torch import nn
import torch.nn.functional as F

torch.manual_seed(0)
attn = nn.MultiheadAttention(embed_dim=8, num_heads=2, batch_first=True)
x = torch.randn(2, 5, 8)
out, weights = attn(x, x, x)
print(out.shape, weights.shape)
print(torch.allclose(weights.sum(dim=-1), torch.ones(2, 5)))
print(sum(p.numel() for p in attn.parameters()))
```

```text
torch.Size([2, 5, 8]) torch.Size([2, 5, 5])
True
288
```

- `attn(x, x, x)`: query, key and value come from the same sequence; this is
  called **self-attention**. In translation the query can come from one
  sequence and the key and value from the other.
- `batch_first=True` exists here too; without it the layer expects
  `(T, B, D)`.
- `weights` is `(B, T, T)`: the weight every query gives every key, averaged
  over the two heads. Every row sums to 1.
- Parameters: four `8 × 8` matrices for Q, K, V and the output, with their
  biases, `4 × (64 + 8) = 288`. The heads split these 8 dimensions in two;
  the number of heads does not change the parameter count.

## What is inside?

The core of attention is one function: `F.scaled_dot_product_attention`.
Let us compare it with the formula we wrote in NumPy.

```python
q, k, v = torch.randn(3, 1, 4, 6).unbind(0)
manual = torch.softmax(q @ k.transpose(-2, -1) / 6 ** 0.5, dim=-1) @ v
print(q.shape)
print(torch.allclose(F.scaled_dot_product_attention(q, k, v), manual, atol=1e-6))
```

```text
torch.Size([1, 4, 6])
True
```

Dividing by `√d` (here `√6`) shrinks the similarities; otherwise in high
dimensions the softmax sticks to a single position and the derivative
vanishes. The real benefit of the ready-made function is speed: it picks the
fastest road for the processor and hardware itself.

## Mask 1: not seeing the padding

In a padded sequence the queries must not give weight to padding positions.
`key_padding_mask` is a `(B, S)` boolean tensor; **`True` means "ignore this
key"** (the opposite of the `padded != 0` mask of the earlier sections).

```python
ids = torch.tensor([[4, 7, 2, 0, 0], [5, 1, 3, 8, 6]])
pad_mask = ids == 0
out, weights = attn(x, x, x, key_padding_mask=pad_mask)
print(weights[0, :, 3:].abs().sum().item())
print(torch.allclose(weights.sum(dim=-1), torch.ones(2, 5)))
```

```text
0.0
True
```

The last two positions of the first sequence are padding: no query gave them
any weight, the total is 0. The weights spread over the remaining three
positions; the row sums are still 1. PyTorch writes minus infinity at a
masked position before the softmax, and `exp(−∞) = 0`.

## Mask 2: not seeing the future

A language model that looks at the words on the right while predicting the
next word is cheating. A **causal mask** lets every position see only itself
and the positions on its left. In a boolean `attn_mask`, `True` means "do not
look".

```python
causal = torch.triu(torch.ones(5, 5, dtype=torch.bool), diagonal=1)
out, weights = attn(x, x, x, attn_mask=causal)
print(causal[1].tolist())
print(weights[0].triu(diagonal=1).abs().sum().item(), weights[0, 0, 0].item())
```

```text
[False, False, True, True, True]
0.0 1.0
```

- `torch.triu(..., diagonal=1)` sets everything above the diagonal to
  `True`: position 1 sees 0 and 1, not 2, 3, 4.
- All weights above the diagonal are 0. The first position sees only
  itself, with a weight of exactly 1.

## The Transformer encoder and position information

`nn.TransformerEncoderLayer` is a whole block: self-attention, a
feed-forward network, residual connections, normalisation.
`nn.TransformerEncoder` stacks blocks. Below we shuffle the positions of the
sequence (a permutation) and look at what happens.

```python
torch.manual_seed(0)
layer = nn.TransformerEncoderLayer(d_model=8, nhead=2, dim_feedforward=16,
                                   dropout=0.0, batch_first=True)
encoder = nn.TransformerEncoder(layer, num_layers=2)
encoder.eval()
perm = torch.tensor([4, 2, 0, 1, 3])
with torch.no_grad():
    out = encoder(x)
    out_perm = encoder(x[:, perm])
print(out.shape, sum(p.numel() for p in encoder.parameters()))
print(torch.allclose(out[:, perm], out_perm, atol=1e-5))
```

```text
torch.Size([2, 5, 8]) 1200
True
```

`True`: shuffling the positions shuffled the output **in the same way**, and
nothing else changed. Attention looks the way you look at a set; it does not
know which item is in which place. The LSTM learned order by reading; for the
Transformer **we must supply** the order: a **positional embedding** is added
to every position. The NumPy section used a sinusoidal positional encoding;
here we use a learned `nn.Embedding`.

## A small Transformer on an order-dependent task

The task from the sequence classification section: "is a 3 immediately
followed by a 5?"

```python
from torch.utils.data import TensorDataset, DataLoader
from dl_data import make_sequences


class TinyTransformer(nn.Module):
    def __init__(self, vocab=10, length=12, d=32):
        super().__init__()
        self.tok = nn.Embedding(vocab, d)
        self.pos = nn.Embedding(length, d)
        layer = nn.TransformerEncoderLayer(d, nhead=2, dim_feedforward=32,
                                           dropout=0.0, batch_first=True)
        self.encoder = nn.TransformerEncoder(layer, num_layers=1)
        self.head = nn.Linear(d, 2)

    def forward(self, x):
        positions = torch.arange(x.shape[1])
        h = self.encoder(self.tok(x) + self.pos(positions))
        return self.head(h.max(dim=1).values)


xs, ys = make_sequences(1200, length=12, seed=7)
xs, ys = torch.from_numpy(xs), torch.from_numpy(ys)
loader = DataLoader(TensorDataset(xs[:1000], ys[:1000]), batch_size=32, shuffle=True,
                    generator=torch.Generator().manual_seed(0))
torch.manual_seed(0)
model = TinyTransformer()
opt = torch.optim.Adam(model.parameters(), lr=0.005)
for epoch in range(15):
    model.train()
    for xb, yb in loader:
        opt.zero_grad()
        F.cross_entropy(model(xb), yb).backward()
        opt.step()
model.eval()
with torch.no_grad():
    acc = (model(xs[1000:]).argmax(dim=1) == ys[1000:]).float().mean().item()
print(acc > 0.9)
```

```text
True
```

- `self.tok(x) + self.pos(positions)`: the word embedding and the position
  embedding are added; the `(12, 32)` position tensor broadcasts over the
  batch.
- After the attention layer every position's vector also carries
  information from its neighbours: "there is a 3 here and a 5 right to my
  right" can come together in one position. `h.max(dim=1).values` takes the
  largest value of each feature over all positions: like the pooling in 1D
  convolution, the question "is it anywhere?". With the same settings the
  version that takes the mean (`h.mean(dim=1)`) stayed below 85%.
- The Transformer passed 90% on this task too.

## Summary

- `nn.MultiheadAttention(..., batch_first=True)`; for self-attention
  `attn(x, x, x)`. The weights are `(B, T, S)`, the rows sum to 1.
- In the boolean masks `key_padding_mask` `(B, S)` and `attn_mask` `(T, S)`,
  **`True` means ignore**. The first for padding, `torch.triu(...,
  diagonal=1)` for the future.
- Attention is blind to order: shuffling the positions only shuffles the
  output. Order is given with a positional embedding.
- `nn.TransformerEncoderLayer` + `nn.TransformerEncoder` is a ready block;
  on small data, `dropout=0.0` and `eval()` make checking easier.
