Write `evaluate(model, loader, loss_fn)`: put the model in `eval()` mode, walk
over all the batches inside `torch.no_grad()`, return `(mean loss, accuracy)`.
Both must be weighted by the number of examples (the last batch is small).

**Expected output:**

```
0.3858 0.8
```
