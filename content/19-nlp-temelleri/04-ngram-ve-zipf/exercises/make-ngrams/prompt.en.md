`ngrams(tokens, n)` should produce the runs of `n` consecutive tokens from a
token list and return each run as a text joined with spaces: `["a b", "b c",
...]`. `n` can be 1, 2, 3 or larger; if it is larger than the number of
tokens, return an empty list.

**Expected output:**

```
it is | is not | not good
a b c | b c d
```
