`copy_effect(spread)` should add a noisy copy of area to the data
(`area_copy = area + np.random.default_rng(1).normal(0, spread, len(X))`),
retrain the forest and return `[area_importance, copy_importance]` on the test
data (`n_repeats=5`, `random_state=0`, 3 places; the copy is the last
column). The starter code does not add the copy.

**Expected output:**

```
[0.457, 0.282]
```
