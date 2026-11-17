`shift_windows(ids, size)` should build window pairs for a language model:
for every `i` the input is `ids[i:i + size]` and the target its one-step shift
`ids[i + 1:i + size + 1]`. There are `len(ids) - size` pairs; return
`[inputs, targets]`.

**Expected output:**

```
[[1, 2, 3], [2, 3, 4]]
[[2, 3, 4], [3, 4, 5]]
```
