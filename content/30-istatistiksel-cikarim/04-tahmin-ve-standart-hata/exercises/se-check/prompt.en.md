`se_check(values, n, reps, seed)` should compare two numbers by
simulation: with `np.random.default_rng(seed)` draw `reps` samples of `n`
people with replacement; `real` = the standard deviation of the sample
means, `estimated` = the average of each sample's **own** standard error
(`std(ddof=1) / sqrt(n)`). Return `[real, estimated]` (3 places). The starter
code forgets `ddof` and finds the standard error too small in small
samples.

**Expected output:**

```text
[3.441, 2.901]
[1.223, 1.225]
```
