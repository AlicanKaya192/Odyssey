`pick_version(results)` should choose, from rows `[name, development,
test]`, the one with the highest development success (the first on a tie;
do **not** choose by the test result). Return `[name, test, gap,
overfitting suspected]`: gap is `round(development - test, 2)`, suspected
is `True` if the gap is larger than 0.1.

**Expected output:**

```
['v3', 0.75, 0.25, True]
['a', 0.8, 0.0, False]
```
