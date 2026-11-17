`order_blind(seqs)` builds two untrained models (the seed is set): a bag of
words and an LSTM. Reverse the sequences with `flip(dims=[1])` and return,
for each model, whether its outputs on the plain and reversed sequences are
the same by `torch.allclose`, as `[bag_same, lstm_same]`. Compute the outputs
inside `torch.no_grad()`.

**Expected output:**

```
[True, False]
```
