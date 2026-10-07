The basic question of working in chunks: **can the result for the whole be
worked out from the chunks' results?** Some calculations combine directly,
some only if you accumulate something else, and some not at all.

## Those that combine directly

| Calculation | In the chunk | Combining |
|---|---|---|
| Total | `sum()` | add |
| Count | `len()` / `count()` | add |
| Minimum | `min()` | take the smallest |
| Maximum | `max()` | take the largest |
| N largest | `nlargest(N)` | join, then `nlargest(N)` again |

## Those that combine if you accumulate something else

| Calculation | Accumulate | At the end |
|---|---|---|
| Mean | total, count | total / count |
| Variance | count (n), total (s), sum of squares (q) | (q − s² / n) / (n − 1) |
| Number of distinct values | the set of values seen | the length of the set |
| Grouped mean | grouped total, grouped count | divide |

The variance formula matched pandas' `var()` to four decimals on 300 000 rows
in this section. (With very large numbers this formula can pile up rounding
error; statistics libraries use sturdier ways.)

## Those that cannot be found exactly from chunks

| Calculation | Why | What to do |
|---|---|---|
| Median | Chunk medians have no relationship to the whole's median | All values are needed, or an approximate method (Section 9) |
| Percentiles (e.g. 95%) | The same reason | An approximate method |
| Mean of means | Wrong weights when chunk sizes differ | Accumulate total and count |
| Sum of `nunique()` | The same value is counted in many chunks | Use a set |

## A check question

When you meet a new calculation, ask: "If I knew the result for two chunks,
could I find the result for the two together?"

- Total: 10 + 20 = 30. Yes.
- Mean: knowing 5 and 7 is not enough; you also need to know how many rows
  each came from. Accumulate total and count, and yes.
- Median: knowing 5 and 7 tells you very little about the median of the two
  together. No.
