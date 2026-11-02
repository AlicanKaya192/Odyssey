Two details of the bootstrap are often mixed up.

## Why with replacement?

Without replacement, drawing a sample of the same size takes the **same**
rows in a different order every time and the statistic never changes. With
replacement some rows are picked two or three times and some not at all;
this imitates "if another sample had come". In a large sample about 37% of
the rows are not picked in each new sample: $(1 - 1/n)^n \approx e^{-1}$.

## Why the same size?

The standard error depends on the sample size (Estimation and Standard
Error section: $s/\sqrt{n}$). Smaller resamples widen the interval
artificially, larger ones narrow it.

## The percentile interval and others

In this section we used the simplest way, the **percentile interval**.
There are versions that behave better for skewed statistics (like BCa);
`scipy.stats.bootstrap` offers them ready-made. The idea is the same:
build the statistic's distribution by resampling.

## Permutation versus bootstrap

- The **bootstrap** answers "how much does the estimate move?": it gives an
  interval.
- The **permutation test** answers "if there were no effect, how surprising
  is this difference?": it gives p.
