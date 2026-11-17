Swapping the LSTM in the lesson's model for a GRU is a one-line job; the only
difference is that the GRU's second output is `h` itself, not a tuple. The
code below uses the lesson's data and its `train_model` and `accuracy`
functions.

```python
class GRUClassifier(nn.Module):
    def __init__(self, vocab=10, dim=8, hidden=16):
        super().__init__()
        self.emb = nn.Embedding(vocab, dim)
        self.gru = nn.GRU(dim, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 2)

    def forward(self, x):
        out, h = self.gru(self.emb(x))
        return self.head(h[-1])


torch.manual_seed(0)
gru_model = train_model(GRUClassifier())
gru_acc = accuracy(gru_model, x_test, y_test)
print(sum(p.numel() for p in gru_model.parameters()))
print(round(gru_acc, 2), gru_acc > 0.9)
```

```text
1362
1.0 True
```

With 1362 parameters (the LSTM had 1778) the GRU is
above 90% on this task too. On short sequences the two often give close
results; the choice is mostly about speed and memory.

## Which one to choose?

| Situation | Advice |
|---|---|
| First attempt | LSTM or GRU, try both; if the gap is small take the smaller one |
| Little data, small device | GRU: fewer parameters, less risk of overfitting |
| Very long dependencies | The LSTM's separate cell state is often a little better |
| Very long sequences, parallel computing needed | The Transformer (this module's attention section) |

When you compare, do not trust a verdict from a single seed: a small gap
between two models can flip with another seed.
