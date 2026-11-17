`channel_stats(batch)` should return, for each channel of a batch in
`(N, C, H, W)` order, the mean and the standard deviation (PyTorch's `std`,
default setting) rounded to 3 places, as two lists: `means, stds`.

**Expected output:**

```
[0.75, 0.5]
[0.5, 0.0]
```
