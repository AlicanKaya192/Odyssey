`pad_batch(seqs)` should pad id lists of different lengths with `0` using
`pad_sequence` into a tensor of shape `(B, T)`. Return a two-item list: the
padded tensor's `.tolist()` and the real length of each sequence.

**Expected output:**

```
[[4, 2, 3], [5, 0, 0], [7, 7, 0]]
[3, 1, 2]
```
