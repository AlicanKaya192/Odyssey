`score(samples, patterns)` should join the patterns with `"|"` into a
case-insensitive regular expression and return the counts `[tp, fp, fn,
tn]` on samples of `[text, is attack]` pairs: tp a caught attack, fp a
false alarm, fn a missed attack, tn an innocent message correctly let
through.

**Expected output:**

```
[2, 1, 1, 1]
```
