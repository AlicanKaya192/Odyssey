Compute the autocorrelation of the daily sales at the first 7 lags, first
by hand and then with `acf`.

**What to do:**

1. For each lag from 1 to 7 compute `s.corr(s.shift(k))`; print them rounded
   to two decimals as a list.
2. Call `acf(s, nlags=7)`; drop lag 0 (`[1:]`) and print the rest rounded to
   two decimals as a list.
3. Print the lag at which the `acf` result is highest (lag 0 excluded).
4. Print the length of the `acf` array and its first element on one line.

**Expected output:**

```
[0.69, 0.28, 0.11, 0.1, 0.27, 0.68, 0.96]
[0.69, 0.28, 0.11, 0.1, 0.26, 0.67, 0.94]
7
8 1.0
```

The two lists are very close but not the same: `acf` uses the mean and
variance of the whole series at every lag. Both tell the same story: the
strongest link is with 7 days earlier.
