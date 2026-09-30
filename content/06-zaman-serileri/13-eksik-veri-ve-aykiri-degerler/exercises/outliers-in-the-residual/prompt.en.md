Looking for outliers in the raw series gets mixed up with the season and
the change of level. Do the same job on the residual of robust STL and see the
difference.

The function `robust(x)` is ready in the starter code.

**What to do:**

1. Apply the interquartile range rule to the **raw series**: the quartiles
   `q1` and `q3`, `iqr = q3 - q1`; print the number of days below
   `q1 - 1.5 * iqr` or above `q3 + 1.5 * iqr`.
2. Print how many of those days are **after** 2 September.
3. Fit robust STL (`STL(visits, period=7, robust=True).fit()`) and compute the
   robust score of the residual.
4. Print the 5 days with the largest absolute score as a `"%m-%d"` list, and
   their scores (one decimal, absolute value) as a separate list.
5. Print the number of days whose absolute score exceeds 3.5 and the number
   exceeding 20 on one line.

**Expected output:**

```
20
16
['03-14', '10-08', '06-20', '09-24', '12-16']
[50.0, 46.3, 45.4, 12.9, 5.8]
30 3
```

On the raw series the rule calls 20 days outliers, most of them after
September: those are not outliers, they are ordinary days at the new level. In
the residual three days break away from everything with scores of 45–50. A
fixed threshold of 3.5 flags 30 days: look at the ranking and at where the
break is rather than at a threshold.
