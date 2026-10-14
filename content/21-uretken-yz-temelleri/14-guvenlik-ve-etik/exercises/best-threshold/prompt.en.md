`best_threshold(scores, target, grid)` should take the model scores of the
suitable candidates in group B (`scores`), the target selection rate and a list
of candidate thresholds. For every threshold `t` find the share of scores not
below `t`, and return the threshold that brings this share closest to `target`
(the one earlier in the list on a tie).

**Expected output:**

```
0.4
```
