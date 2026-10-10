`discounts(qtys)` should return the discount rate for each quantity: 25 and
above `0.2`, 10 and above `0.1`, the rest `0.0`. Use `np.select`. The starter
code also uses `np.select` but gives `0.1` for 30 items: the order of the
conditions is wrong. **Do not write a loop.**

**Expected output:**

```
[0.0, 0.1, 0.0, 0.2, 0.2]
```
