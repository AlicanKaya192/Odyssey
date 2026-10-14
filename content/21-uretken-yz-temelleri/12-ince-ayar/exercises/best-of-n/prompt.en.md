`best_of_n(candidates, weights)` should take, for every question, the
candidate answers' feature lists (`candidates[i]`) and the reward weights. For
every question pick the index of the candidate with the highest reward
(`features · weights`) (the smaller index on a tie). Return the list of
indices.

**Expected output:**

```
[0, 1]
```
