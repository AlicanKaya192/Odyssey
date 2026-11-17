The other schedulers follow a calendar; `ReduceLROnPlateau` follows the
**result**. If the validation loss does not improve for `patience` epochs, it
multiplies the rate by `factor`. That is why `step()` is given that epoch's
validation loss:

```python
w = nn.Parameter(torch.zeros(1))
optimizer = torch.optim.SGD([w], lr=0.1)
scheduler = lr_scheduler.ReduceLROnPlateau(optimizer, factor=0.5, patience=2)
val_losses = [1.0, 0.8, 0.7, 0.7, 0.71, 0.72, 0.69, 0.69, 0.7, 0.7]
rates = []
for val_loss in val_losses:
    optimizer.step()
    scheduler.step(val_loss)
    rates.append(optimizer.param_groups[0]["lr"])
print(rates)
```

```text
[0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.025]
```

- The best loss, 0.7, came in epoch 3; the next three epochs could not beat
  it, and at the end of epoch 6 the rate was halved.
- 0.69 became the new best and the counter was reset; after three more
  epochs without improvement the rate was halved once more.
- It goes well with early stopping (the Regularisation section): first lower
  the rate, and if that does not help either, stop.
