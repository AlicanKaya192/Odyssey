## Formulas and NumPy counterparts

| Measure | Formula | NumPy |
|---|---|---|
| Mean | `Σx / n` | `x.mean()` |
| Variance | `Σ(x − mean)² / n` | `x.var()` (`n − 1` with `ddof=1`) |
| Standard deviation | `√variance` | `x.std()` |
| Percentile | `(n − 1)·q/100` in the sorted list, linear in between | `np.percentile(x, q)` |
| Median | the 50th percentile | `np.median(x)` |
| Covariance | `Σ(x − mean_x)(y − mean_y) / n` | `np.cov(x, y, ddof=0)` |
| Pearson | covariance / (sd_x · sd_y) | `np.corrcoef(x, y)[0, 1]` |
| Histogram | count in equal bins | `np.histogram(x, bins, range)` |

## Numerical soundness

- Instead of `E[x²] − (E[x])²`, subtract the mean first (two passes) or use
  Welford.
- When adding many small numbers, Python's `math.fsum` does not accumulate
  rounding error; NumPy's `sum` uses pairwise summation.
- The standard deviation of a constant column is 0: dividing by it produces
  `inf` or `nan`.

## Common mistakes

- `int()` truncates towards zero: `int(-0.3)` gives 0, `math.floor(-0.3)` gives
  −1. That is why out-of-range negative values can land in the wrong bin when
  computing a bin number; check the range first.
- `np.cov` divides by `n − 1` by default, `np.var` by `n`.
- Taking correlation for causation; ignoring a relation because the
  correlation is 0.
