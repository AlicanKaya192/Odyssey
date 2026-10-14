`bootstrap(ok1, ok2, rounds, seed)` should do the lesson's resampling:
`rng = random.Random(seed)`; in every round draw `n = len(ok1)` indices
with `rng.randrange(n)` and divide the sum of `(ok2 - ok1)` by `n`. Sort
the differences; the lower end is `diffs[rounds // 20]`, the upper end
`diffs[rounds - rounds // 20 - 1]`. Return `[actual difference, lower end,
upper end]`, each rounded to 3 places.

**Expected output:**

```
[0.125, 0.0, 0.25]
```
