`balanced_ids(per_label, seed)` should make a balanced choice from the pool
(`POOL`): create `rng = random.Random(seed)`; in the order of `LABELS`,
pick from each category's messages in the pool with
`rng.sample(..., per_label)` and add them to a list; at the end shuffle the
list with `rng.shuffle`. Return the ids of the chosen messages.

**Expected output:**

```
[27, 6, 33, 14, 15]
10
```
