With the same tables, `viterbi(words)` should return the most likely tag
sequence. Keep `(best probability, path reaching that tag)` for each tag; for
each new word pick the best previous tag for each tag. At the end return the
most likely path.

**Expected output:**

```
['PRON', 'VERB', 'DET', 'NOUN']
['DET', 'NOUN']
```
