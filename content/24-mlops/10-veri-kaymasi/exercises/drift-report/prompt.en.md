Write the function `drift_report(reference, current, columns, bins)` that applies the lesson's PSI to several columns. The rows are dictionaries:

- For every column, sort the reference's values; the edges are `ordered[len(ordered) * i // bins]`, with `i` from 1 to `bins - 1`.
- Find the bin with `bisect.bisect_left`; make the shares at least `0.0001`.
- Compute the PSI and add `[column, PSI (three digits), label]`. The label: below `0.1` `"stable"`, up to `0.25` `"moderate"`, above that `"large"`.
- Keep the columns' order.

**Expected output:**

```
['fee', 2.892, 'large']
['calls', 0.0, 'stable']
```
