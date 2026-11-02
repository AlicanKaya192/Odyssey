The chance of getting past every layer is the same, `pass_prob`. How
many layers must be stacked so that the chance of getting past all of them
is equal to or less than `target`?

`layers_needed(pass_prob, target)` should return the smallest number of
layers (at least 1). If `pass_prob` is `1` or more, no number of layers
reaches the target: return `None`.

**Expected output:**

```
4
10
None
```
