`channels_first(img)` should turn a nested list in `(height, width, channel)`
order into `(channel, height, width)` order and return it as a nested list
again. `torch.tensor`, `permute` and `tolist` are enough.

**Expected output:**

```
3 2 2
[[1, 4], [7, 10]]
```
