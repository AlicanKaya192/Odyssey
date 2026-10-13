`skipgram_pairs(tokens, window)` should take each token as the centre and
build a `[centre, context]` pair with every word in its window; return the
pairs in centre order, and for each centre from left to right.

**Expected output:**

```
a cat
cat a
cat sat
sat cat
```
