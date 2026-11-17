# A Character-Level Language Model

A language model predicts the **next item** of a sequence. In the Embeddings
and Language Models module we built a word-level n-gram model and an RNN
language model with NumPy, and saw text generation and decoding methods
(greedy choice, temperature, beam search). This section builds the same idea
in PyTorch **at the character level**: the vocabulary is letters, not words,
so it is tiny; the model has to learn by itself to write words letter by
letter.

This section has two PyTorch-specific lessons: a language model uses the
output of **every step** (classification used only the last state), and the
loss function does not take a `(B, T, V)` output directly.

## Characters and targets

```python
import math

import torch
from torch import nn
from dl_data import TEXT

chars = sorted(set(TEXT))
index = {c: i for i, c in enumerate(chars)}
data = torch.tensor([index[c] for c in TEXT])
T = 32
x = torch.stack([data[i:i + T] for i in range(len(data) - T)])
y = torch.stack([data[i + 1:i + T + 1] for i in range(len(data) - T)])
print(len(TEXT), len(chars), repr("".join(chars[:6])))
print(x.shape, y.shape)
print(torch.equal(x[0, 1:], y[0, :-1]))
```

```text
289 21 ' .abcd'
torch.Size([257, 32]) torch.Size([257, 32])
True
```

- The text has 289 characters; with the space and the full stop
  the vocabulary has 21 characters.
- The target is the input **shifted by one**: `y[t] = x[t + 1]`. The last
  line confirms it. Every window holds 32 predictions; nobody wrote the
  labels by hand, they come from the text itself (self-supervised learning).

## The model: one prediction per step

```python
class CharLM(nn.Module):
    def __init__(self, vocab, dim=16, hidden=64):
        super().__init__()
        self.emb = nn.Embedding(vocab, dim)
        self.lstm = nn.LSTM(dim, hidden, batch_first=True)
        self.head = nn.Linear(hidden, vocab)

    def forward(self, x, state=None):
        out, state = self.lstm(self.emb(x), state)
        return self.head(out), state


torch.manual_seed(0)
model = CharLM(len(chars))
logits, _ = model(x[:4])
print(logits.shape)
loss = nn.functional.cross_entropy(logits.reshape(-1, len(chars)), y[:4].reshape(-1))
print(abs(loss.item() - math.log(len(chars))) < 0.1)
```

```text
torch.Size([4, 32, 21])
True
```

- `self.head(out)`: the linear layer applies to the last dimension of
  `(B, T, 64)`, and the output is `(B, T, V)`: a logit for every character
  of the vocabulary at every step.
- `cross_entropy` expects the class dimension in **second** place (`(N, V)`
  or `(B, V, T)`). The clearest road is flattening both tensors: `(B·T, V)`
  and `(B·T,)`. Give it `(B, T, V)` as it is and it takes T for the classes
  and raises an error (or, if the shapes happen to fit, computes the wrong
  thing).
- The untrained model's loss is close to `log V`: roughly equal chances for
  every character.
- `forward` also returns the state; generation will need it.

## Training

```python
opt = torch.optim.Adam(model.parameters(), lr=0.01)
for step in range(150):
    gen = torch.Generator().manual_seed(step)
    batch = torch.randint(0, len(x), (32,), generator=gen)
    logits, _ = model(x[batch])
    flat = logits.reshape(-1, len(chars))
    loss = nn.functional.cross_entropy(flat, y[batch].reshape(-1))
    opt.zero_grad()
    loss.backward()
    opt.step()
print(loss.item() < 1.0)
```

```text
True
```

At every step we pick 32 random windows (the choice is seeded, the same on
every run). After 150 steps the loss is below 1. The text is very small; the
model largely **memorises** it. In a real language model the same loop runs
over millions of characters and a separate validation text measures
memorisation.

## Generating text

For generation the network gets a start, the most likely character is chosen
(greedy choice) and **fed back in** as input. Instead of having it read the
whole text from the beginning every time, we carry the LSTM's state: the
network reads only the last character.

```python
def generate(model, start, n):
    model.eval()
    text = start
    with torch.no_grad():
        ids = torch.tensor([[index[c] for c in start]])
        logits, state = model(ids)
        for _ in range(n):
            next_id = logits[0, -1].argmax().item()
            text += chars[next_id]
            logits, state = model(torch.tensor([[next_id]]), state)
    return text


print(generate(model, "the c", 20))
print(generate(model, "a bird", 20))
```

```text
the cat saw the dog. the 
a bird sat on the tree. th
```

- The model learned to write words letter by letter; every word it produces
  is in the text. The sentences are pieces of the text's sentences: that is
  what to expect from such a small text.
- Carrying `state` gives the same result as re-reading the whole text at
  every step, but does one character of work per step (see the note).

## Summary

- In a language model the target is the input shifted by one: `y[t] = x[t +
  1]`; the label comes from the text itself.
- The output is `(B, T, V)`; flatten to `(B·T, V)` and `(B·T,)` for the
  loss.
- The untrained model's loss is around `log V`; that is a good first check.
- For generation, carry the LSTM's state and feed only the last character.
