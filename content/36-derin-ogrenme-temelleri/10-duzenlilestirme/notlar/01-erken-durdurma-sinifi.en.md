To avoid rewriting early stopping in every project, a small class helps.
`min_delta` means "how much must it fall at least to count as an
improvement":

```python
class EarlyStopping:
    def __init__(self, patience=3, min_delta=0.0):
        self.patience, self.min_delta = patience, min_delta
        self.best, self.waited = float("inf"), 0

    def step(self, val_loss):
        if val_loss < self.best - self.min_delta:
            self.best, self.waited = val_loss, 0
            return False
        self.waited += 1
        return self.waited >= self.patience


stopper = EarlyStopping(patience=3)
losses = [0.9, 0.7, 0.6, 0.62, 0.61, 0.65, 0.5]
for epoch, loss in enumerate(losses, start=1):
    if stopper.step(loss):
        print("stop at", epoch, "best", stopper.best)
        break
```

```text
stop at 6 best 0.6
```

- After the 0.6 of epoch 3 there are three epochs without improvement; it
  stopped at epoch 6.
- At epoch 7 the loss would have dropped to 0.5, but we never saw that
  epoch. Patience is a trade-off: a small patience stops early (sometimes too
  early), a large one wastes epochs. Typical values are 5–20 epochs.
- `min_delta` keeps tiny drops at the noise level (0.6 → 0.5999) from
  resetting the counter.
