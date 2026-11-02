This time only 20 loads were measured after the server change
(`make_speed_test(n=20, seed=81)`). Print how far the mean is from the old
mean (`gap`, 1 place). Then find the p-value by simulation: draw 10000
samples of 20 from the old load times (`old`)
(`rng.choice(old, size=(10000, 20))`), take their means and print, with 3
places, the share **at least** `gap` away from `old.mean()`.

**Expected output:**

```text
87.4
0.001
```
