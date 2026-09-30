Transform the passenger series step by step and see what the two tests
say at each step.

**What to do:**

1. Prepare four series and collect them in a dictionary (keys in this order):
   - `"level"`: `p`
   - `"diff"`: `p.diff()`
   - `"diff12"`: `p.diff(12)`
   - `"log diff12"`: `np.log(p).diff(12)`
2. For each (after `dropna()`) compute the ADF and KPSS p-values and print
   them as `name adf_p kpss_p`, p-values with three decimals, one per line.
3. Print how many rows the last series (`"log diff12"`) lost and its standard
   deviation (three decimals) on one line.
4. Go one step further and take an unnecessary difference:
   `np.log(p).diff(12).diff()`. Print its standard deviation rounded to three
   decimals.

**Expected output:**

```
level 1.0 0.01
diff 0.537 0.1
diff12 0.982 0.01
log diff12 0.0 0.1
12 0.023
0.033
```

For the level and for `diff12` both tests say "not stationary". For the plain
difference the tests disagree: the season and the growing variance are still
there. With logarithm + `diff(12)` both say "stationary". One more difference
on top **raises** the standard deviation: stop at the fewest differences
needed.
