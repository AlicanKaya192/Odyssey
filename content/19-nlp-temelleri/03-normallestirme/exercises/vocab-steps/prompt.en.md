`vocab_steps(n)` should measure the vocabulary of the first `n` reviews in
three steps and return `[raw, after_stop, after_stem]`:

1. raw: the set of all words
2. after stop: those not in `STOP`
3. after stem: the stems of the remaining ones with `stem` (a set)

**Expected output:**

```
[332, 303, 297]
```
