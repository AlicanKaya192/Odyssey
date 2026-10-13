`top_pmi(min_count, k)` should sort the word pairs that appear at least
`min_count` times by PMI, from largest to smallest, and return the first `k`
as `"a b"`. PMI is as in the lesson:

`log2((pair / n_bi) / ((left / n_uni) * (right / n_uni)))`

**Expected output:**

```
can't say
bluetooth connection
brewing time
step counter
```
