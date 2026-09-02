You will find outliers by **rule**, not by eye.

The starter code has a `values` series: daily order counts for a week.

**What you need to do:**

1. Compute the first and third quartiles and print them **side by side**.
2. Compute the lower and upper bounds (1.5 times the interquartile range)
   and print them **side by side**.
3. Print the values outside those bounds **as a list**.
4. Print the mean (to two decimals) and the median of the series **side by
   side**.

**Expected output:**

```
49.75 52.25
46.0 56.0
[140]
61.62 50.5
```

**What the IQR rule is:** `quantile(0.25)` is the value a quarter of the data
falls below and `quantile(0.75)` three quarters. The distance between them is
the **interquartile range**, and it shows the spread of the middle half of
the data. Anything more than 1.5 times that distance outside the interval
counts as an outlier.

**Why the last line matters:** 140 is a single value, but it lifts the mean
from 50 to 61.6. The median stays at 50.5. When you suspect an outlier, the
median is the more reliable summary.

And remember: the rule **finds** the outlier, it does not decide whether to
delete it. 140 orders could be a data error, or it could be a campaign day.
