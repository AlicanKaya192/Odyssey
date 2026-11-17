# Sequence Classification

In the first two sections we saw how to prepare sequences and the formats of
the LSTM. Now we train a network: a **sequence classifier** that reads a
sequence and gives one label. Sentiment analysis, spam filtering, whether a
sensor recording is faulty: they all follow this pattern.

We choose the task on purpose so that it **depends on order**: in sequences
of 12 numbers from 0 to 9, "is a 3 immediately followed by a 5?" It is not
enough for a sequence to contain both 3 and 5; they must be next to each
other and in this order. A model that cannot see order should struggle
here.

## Data

```python
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
from dl_data import make_sequences

x, y = make_sequences(1200, length=12, seed=7)
x, y = torch.from_numpy(x), torch.from_numpy(y)
train = TensorDataset(x[:1000], y[:1000])
x_test, y_test = x[1000:], y[1000:]
print(x.shape, x.dtype)
print(x[0].tolist(), y[0].item())
print(round(y.float().mean().item(), 2))
```

```text
torch.Size([1200, 12]) torch.int64
[9, 6, 6, 8, 5, 7, 8, 2, 0, 3, 2, 8] 0
0.54
```

- Every number is a "word"; the vocabulary has 10 ids. This time there is no
  padding: all sequences have length 12, that is how `make_sequences` makes
  them.
- About half of the labels are 1: a model that always says 0 stays around
  50%. We read the score against that.
- The first 1000 sequences are for training, the last 200 for testing.

## The model: embedding → LSTM → linear

```python
class SeqClassifier(nn.Module):
    def __init__(self, vocab=10, dim=8, hidden=16):
        super().__init__()
        self.emb = nn.Embedding(vocab, dim)
        self.lstm = nn.LSTM(dim, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 2)

    def forward(self, x):
        out, (h, c) = self.lstm(self.emb(x))
        return self.head(h[-1])


torch.manual_seed(0)
model = SeqClassifier()
print(model(x[:4]).shape)
print(sum(p.numel() for p in model.parameters()))
```

```text
torch.Size([4, 2])
1778
```

- `h[-1]` is the last hidden state of the last layer, `(B, 16)`: a
  one-vector summary of the sequence. The linear layer turns it into the
  **logits** of the two classes (the raw scores before softmax).
- The output is `(4, 2)`: 4 sequences, 2 classes. The loss
  `nn.CrossEntropyLoss` applies softmax itself, so the model ends without
  one (the activation and loss section of the Deep Learning Fundamentals
  module).

## Training

The training loop is the same as for table data; being a sequence changes
nothing. We write two small functions to reuse.

```python
def train_model(model, epochs=8, lr=0.01):
    loader = DataLoader(train, batch_size=32, shuffle=True,
                        generator=torch.Generator().manual_seed(0))
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    for epoch in range(epochs):
        model.train()
        for xb, yb in loader:
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
    return model


def accuracy(model, x, y):
    model.eval()
    with torch.no_grad():
        return (model(x).argmax(dim=1) == y).float().mean().item()


torch.manual_seed(0)
lstm_model = train_model(SeqClassifier())
acc = accuracy(lstm_model, x_test, y_test)
print(round(acc, 2), acc > 0.9)
```

```text
1.0 True
```

The LSTM reached 100% accuracy on the test set: it learned the
pattern. On this computer training took a few seconds.

## A rival that cannot see order

A model that takes the mean of the embeddings (bag of words) knows which
numbers are present but not their order.

```python
class BagClassifier(nn.Module):
    def __init__(self, vocab=10, dim=8):
        super().__init__()
        self.emb = nn.Embedding(vocab, dim)
        self.head = nn.Linear(dim, 2)

    def forward(self, x):
        return self.head(self.emb(x).mean(dim=1))


torch.manual_seed(0)
bag_model = train_model(BagClassifier())
bag_acc = accuracy(bag_model, x_test, y_test)
print(round(bag_acc, 1), bag_acc < acc)
```

```text
0.8 True
```

The bag of words stayed around 80%. It can learn "are 3 and 5
present" (that is why it beats 50%), but not "a 5 right after a 3".

## Reversing the order

Let us see the evidence directly: reverse the test sequences. In a reversed
sequence "3, 5" becomes "5, 3"; the right label may change. For the bag of
words, though, the reversed sequence is the same sequence.

```python
x_rev = x_test.flip(dims=[1])
with torch.no_grad():
    bag_same = torch.equal(bag_model(x_test).argmax(1), bag_model(x_rev).argmax(1))
    lstm_same = torch.equal(lstm_model(x_test).argmax(1), lstm_model(x_rev).argmax(1))
print(bag_same, lstm_same)
```

```text
True False
```

- `True`: all 200 predictions of the bag of words are the same on the
  reversed sequences. Since a mean does not depend on order, it cannot be
  otherwise.
- `False`: the LSTM reads the reversed sequence as a different sequence.

## Summary

- A sequence classifier: `nn.Embedding` → `nn.LSTM` → last state `h[-1]` →
  `nn.Linear` → logits. The softmax lives inside the loss function.
- The training loop is the same as for table data; only the inside of the
  model changes.
- A mean of embeddings cannot see order; on an order-dependent task the
  LSTM is far ahead.
- Compare the score with a baseline (always saying one class, a bag of
  words); a percentage on its own says little.
