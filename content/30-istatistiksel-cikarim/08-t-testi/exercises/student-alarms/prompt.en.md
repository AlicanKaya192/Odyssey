`alarm_rates(n1, sd1, n2, sd2, reps, seed)` should measure two tests in a world
where the true difference is zero: with `np.random.default_rng(seed)`
generate `reps` × `n1` normal values with mean 10 and deviation `sd1`, and
`reps` × `n2` with deviation `sd2` (first group first). Apply Student
(`ttest_ind`, the default) and Welch (`equal_var=False`) row by row; return
the shares with `p < 0.05` as `[student, welch]` with 3 places.

**Expected output:**

```text
[0.259, 0.053]
[0.051, 0.05]
```
