`param_bytes(sizes, bytes_per_value)` should compute the parameter memory, in
bytes, of a network made of consecutive linear layers. `sizes = [64, 128, 10]`
means two layers: `Linear(64, 128)` and `Linear(128, 10)`; every layer has a
weight and a bias.

**Expected output:**

```
38440
19220
```
