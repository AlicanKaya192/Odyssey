`table[i]` holds the logits of the ids that follow id `i` (a tiny bigram
model). `generate_greedy(table, start, n)` should start at `start` and
generate `n` ids, at every step appending the position of the largest logit
in the last id's row. Return the whole list, the start included.

**Expected output:**

```
[0, 1, 2, 0, 1, 2]
[2, 0, 1, 2]
```
