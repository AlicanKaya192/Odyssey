For each of the `load_ms` and `minutes` columns, print on one line the
column name, the mean, the median, the standard deviation (pandas `std()`)
and the 95th percentile (`np.percentile(x, 95)`), all with 1 place. On the
last line print the name of the column whose mean and median differ the
most (the largest absolute difference).

**Expected output:**

```text
load_ms 849.7 850.0 120.3 1048.0
minutes 9.0 7.5 6.1 20.5
minutes
```
