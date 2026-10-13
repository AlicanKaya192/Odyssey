`learn_bpe(counts, n_merges)` should learn at most `n_merges` merge rules from a
`{word: frequency}` dictionary and return them as a list of `[a, b]`. At each
step pick the most frequent pair; on ties, the largest `(count, pair)` key.
Stop when no pair is left.

**Expected output:**

```
['t', '</w>']
['s', 't</w>']
['e', 'st</w>']
['o', 'w']
['l', 'ow']
```
