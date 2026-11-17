# RNN, LSTM and GRU

The recurrent neural network (RNN) was built from scratch with NumPy in the
RNN section of the Embeddings and Language Models module. In short: the
network reads a sequence from left to right; at every step it combines the
current input with the previous **hidden state** to compute the new hidden
state, using the same weights at every step. In a plain RNN the derivative
vanishes over long sequences; the LSTM and the GRU solve this with
**gates**. There we wrote the forward pass, backpropagation through time and
the gates by hand.

In PyTorch all three are ready-made layers: `nn.RNN`, `nn.LSTM`, `nn.GRU`.
Autograd does the backpropagation. In this section we learn the layers'
**input and output formats**, where their parameters live and how to use
them on padded sequences; most bugs come from mixing these formats up.

## `nn.RNN`: two outputs

```python
import torch
from torch import nn

torch.manual_seed(0)
rnn = nn.RNN(input_size=4, hidden_size=3, batch_first=True)
x = torch.randn(2, 5, 4)
out, h = rnn(x)
print(out.shape, h.shape)
print(torch.allclose(out[:, -1], h[0]))
```

```text
torch.Size([2, 5, 3]) torch.Size([1, 2, 3])
True
```

- The input is `(B, T, D)`: 2 sequences, 5 steps, 4 numbers at each step.
  Without `batch_first=True` the layer expects `(T, B, D)` and reads along
  the wrong axis but **raises no error**; that makes it one of the sneakiest
  bugs.
- `out` is the hidden state of **every step**: `(B, T, H)`. Tasks that need
  an output for every word (tagging, a language model) use this.
- `h` is the hidden state of the **last** step only: `(number of layers, B,
  H)`. Tasks that summarise the whole sequence in one vector
  (classification) use this. Even with `batch_first=True`, the first
  dimension of `h` is the layer; the batch is second.
- The last line: the last step of `out` and `h` are the same thing.

## Inside the layer: the same formula

What `nn.RNN` computes is the same formula we wrote in NumPy. The weights
live under the names `weight_ih_l0` (input to hidden) and `weight_hh_l0`
(hidden to hidden); PyTorch keeps two separate biases.

```python
W_ih, W_hh = rnn.weight_ih_l0, rnn.weight_hh_l0
b = rnn.bias_ih_l0 + rnn.bias_hh_l0
h_t = torch.zeros(2, 3)
for t in range(5):
    h_t = torch.tanh(x[:, t] @ W_ih.T + h_t @ W_hh.T + b)
print(W_ih.shape, W_hh.shape)
print(torch.allclose(h_t, h[0], atol=1e-6))
```

```text
torch.Size([3, 4]) torch.Size([3, 3])
True
```

The weights are stored as `(output, input)`, so they are multiplied with
`.T`; the same layout as in `nn.Linear`. Our five-step loop gave the layer's
last hidden state.

## Three layers, three parameter counts

```python
def count(m):
    return sum(p.numel() for p in m.parameters())


for cls in (nn.RNN, nn.GRU, nn.LSTM):
    print(cls.__name__, count(cls(4, 3, batch_first=True)))
```

```text
RNN 27
GRU 81
LSTM 108
```

The plain RNN has one "gate": `3×4 + 3×3 + 3 + 3 = 27`. The GRU computes
three parts (reset gate, update gate, candidate state), the LSTM four
(forget, input and output gates and the candidate cell): the parameter count
is exactly 3 and 4 times as large. At the same hidden size the LSTM is
stronger but more expensive; the GRU sits in between.

## `nn.LSTM`: the cell state comes back too

Next to its hidden state the LSTM has a **cell state**: the long-term memory.
That is why the second output is a **tuple**.

```python
lstm = nn.LSTM(4, 3, batch_first=True)
out, (h, c) = lstm(x)
print(tuple(out.shape), tuple(h.shape), tuple(c.shape))
print(lstm.weight_ih_l0.shape)
```

```text
(2, 5, 3) (1, 2, 3) (1, 2, 3)
torch.Size([12, 4])
```

- If you write `out, h = lstm(x)`, `h` becomes a tuple and the next line
  gives a confusing error: unpack it as `(h, c)`.
- The weights of the four gates are stacked in one matrix: `(4 × 3, 4)` =
  `(12, 4)`.

## Deep and bidirectional

`num_layers=2` stacks two LSTMs: the second reads the first one's `out`.
`bidirectional=True` adds a second LSTM that reads the sequence from right to
left; the output of every step joins the two directions.

```python
deep = nn.LSTM(4, 3, num_layers=2, bidirectional=True, batch_first=True)
out, (h, c) = deep(x)
print(out.shape, h.shape)
```

```text
torch.Size([2, 5, 6]) torch.Size([4, 2, 3])
```

- `out` holds the two directions of the last layer side by side: `2 × 3 = 6`
  numbers.
- `h` has one final state per layer and per direction: `2 layers × 2
  directions = 4`. The order is `[layer 0 forward, layer 0 backward, layer 1
  forward, layer 1 backward]`; the two directions of the last layer are
  `h[-2]` and `h[-1]`.
- A bidirectional network needs to see the whole sequence in advance. That
  helps classification, where the whole text is at hand; in a language model
  that predicts the next word, seeing the future would be cheating.

## An LSTM on padded sequences

In the previous section we added padding to short sequences. The LSTM does
not know about padding: it reads the padding steps too and spoils the last
hidden state. Below, the real length of the second sequence is 2; the rest
is zero padding.

```python
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

torch.manual_seed(1)
x = torch.randn(2, 5, 4)
x[1, 2:] = 0
lengths = torch.tensor([5, 2])
out, (h, c) = lstm(x)
print(torch.allclose(h[0, 1], out[1, 1]))

packed = pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)
out_p, (h_p, c_p) = lstm(packed)
print(torch.allclose(h_p[0, 1], out[1, 1]))

padded, lens = pad_packed_sequence(out_p, batch_first=True)
print(padded.shape, lens.tolist(), padded[1, 2:].abs().sum().item())
```

```text
False
True
torch.Size([2, 5, 3]) [5, 2] 0.0
```

- The first line is `False`: in the run without packing, the second
  sequence's last hidden state is not the state at its real last step
  (`out[1, 1]`). Three zero steps changed the state. A zero input does not
  mean "nothing"; the network still computes with its weights and biases.
- **Packing** (`pack_padded_sequence`) tells the layer the length of every
  sequence; the layer stops each sequence at its own end. The second line is
  `True`: the last state of the packed run is the state of the real last
  step.
- `enforce_sorted=False` does not require the sequences to be sorted by
  length (the layer sorts and unsorts them itself).
- `pad_packed_sequence` turns the packed output back into a padded tensor;
  the padding positions are zero.

## Summary

- `nn.RNN`, `nn.GRU`, `nn.LSTM`: write `batch_first=True` for a `(B, T, D)`
  input; without it there is no error, only a wrong result.
- `out` is the state of every step `(B, T, H × directions)`; `h` is the last
  state `(layers × directions, B, H)`. The LSTM returns a tuple `(h, c)` as
  its second output.
- The parameter count is 3 (GRU) and 4 (LSTM) times that of the RNN.
- On padded sequences use `pack_padded_sequence(..., enforce_sorted=False)`
  for the last state, or pick the `out` of the last real step yourself (see
  the note).
