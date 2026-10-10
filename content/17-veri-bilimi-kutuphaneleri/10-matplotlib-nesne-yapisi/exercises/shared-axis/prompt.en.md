`compare(a, b)` should open two areas side by side (`plt.subplots(1, 2,
...)`), plot `a` on the left and `b` on the right, and make both areas use
**the same y axis** (`sharey=True`). Save it as `compare.png` and close the
figure. Return `[limits_equal, [low, high]]`; the limits are the left area's
`get_ylim()`, rounded to 1 place.

**Expected output:**

```
[True, [4.5, 125.5]]
```
