Look for outlier days in the web traffic first with a z-score, then with
a robust score based on the median and the MAD.

**What to do:**

1. Print the mean (one decimal), the median and the standard deviation (one
   decimal) on one line.
2. Compute the z-score; print the days whose absolute value exceeds 3 as a
   `"%m-%d"` list.
3. Write a function `robust(x)` that returns
   `0.6745 * (x - x.median()) / (x - x.median()).abs().median()`.
4. Print the MAD (the median of the absolute deviations from the median),
   rounded to one decimal.
5. Print the 5 days with the largest absolute robust score as a `"%m-%d"`
   list, and their scores (one decimal, absolute value) as a separate list.
6. For 8 October (the outage day) print the z-score and the robust score,
   rounded to two decimals, on one line.

**Expected output:**

```
4081.1 4002.0 914.2
['03-14', '06-20', '10-08']
337.5
['03-14', '06-20', '10-08', '11-12', '11-14']
[11.2, 9.8, 7.7, 3.7, 3.5]
-4.31 -7.72
```

Both methods put the same three days on top, but they stand out far more in
the robust score: the outage day is −4.3 as a z-score and −7.7 as a robust
score. Why? The standard deviation (914) is inflated by those three days
themselves; the MAD (337.5) is not affected by them.
