Write `timeit(fn, repeat=5)`: run `fn` `repeat` times, measure each with
`time.perf_counter()` and return the **shortest** time. The ready code below
compares row-by-row and batch prediction; the output is not a time but the
result of the comparison.

**Expected output:**

```
True
```
