The layers of the `TwoLayer` class are ready; `forward` returns the input as it
is. Fix `forward`: `first` → ReLU → `second`. `output` sets every weight to 0.5 and
gives the output.

**Expected output:**

```
[[4.5, 4.5]]
[[0.5, 0.5]]
```
