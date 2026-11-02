From session length (`minutes`) draw 3000 samples each of `n` = 4 and
`n` = 64 people: `rng.choice(x, size=(3000, n)).mean(axis=1)` (the same
`rng`, first 4 then 64). On each line write `n`, the mean of the means (2
places), the standard deviation of the means (3 places) and the formula
`x.std() / np.sqrt(n)` (3 places). The last two columns should come out
close.

**Expected output:**

```text
4 9.03 3.052 3.064
64 9.05 0.764 0.766
```
