`classifier_params(vocab, dim, hidden)` should build the three layers of the
lesson's model: `nn.Embedding(vocab, dim)`, `nn.LSTM(dim, hidden,
batch_first=True)` and `nn.Linear(hidden, 2)`. Return their total parameter
count.

**Expected output:**

```
1778
570
```
