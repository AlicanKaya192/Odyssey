`ablation(definitions, base, tickets)` should take out, one at a time,
every word that is in `definitions` but not in `base` (with its category)
and measure again with the given `accuracy(render(...), tickets)`. If the
change `round(new - full, 2)` is not zero, `[word, change]` goes into the
list (in dictionary and word order).

**Expected output:**

```
tracking -0.05
deliver -0.05
back 0.05
seam -0.05
card -0.05
```
