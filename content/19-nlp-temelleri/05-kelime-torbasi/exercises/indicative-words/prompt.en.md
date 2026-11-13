`indicative(label_a, label_b, k)` should compute, for every word, the log ratio
of its share in `label_a` reviews to its share in `label_b` reviews (+1
smoothing on both counts) and return the `k` words with the largest ratio,
largest first, as a list. The general form of the lesson's calculation.

Look at the first line of the output: the words pointing most to neutral
reviews are typos and numbers. Rare words seen once or twice in one class get
an artificially high ratio; that is what `min_df` from section 04 is for.

Words with equal scores should come in alphabetical order:
`np.argsort(-score, kind="stable")` sorts from largest to smallest and
keeps equal ones in place, so the order is the same on every computer.

**Expected output:**

```
deos, 30, 11, battrey, bluetotoh
but, be, to, all, at
```
