Build the interval for a multi-step forecast from **the real errors** on a
rolling origin: with the quantiles of each week of the horizon.

In the starter code `snaive(train, h)` and `cuts` (13 cuts) are ready.

**What to do:**

1. At each cut compute the error of the 28-day seasonal naive forecast
   (`actual − forecast`); collect them in a 13 × 28 numpy array.
2. Set aside the first 9 experiments to **build** the interval and the last 4
   to **test** it.
3. From the errors of the first 9 experiments compute the 10% and 90%
   quantiles for each week of the horizon (columns 0–6, 7–13, 14–20, 21–27);
   print four lines as `week lower upper` with one decimal.
4. For the same weeks print the share of errors in the last 4 experiments
   within those bounds, with two decimals, as a list.
5. Print the overall coverage of the last 4 experiments with three decimals.

**Expected output:**

```
1 -28.8 24.8
2 -37.0 15.8
3 -25.8 21.6
4 -32.8 18.8
[0.93, 0.54, 0.64, 0.54]
0.661
```

For the first week the interval holds; in the later weeks the interval it
calls 80% misses about half the time. Why? The last four experiments are the
autumn and the end of the year: sales are rising and the errors shift to the
positive side. The errors of the first nine experiments do not represent that
period. An empirical interval is assumption-free but **not magic**: it works
to the extent that past errors resemble future ones. Every miss is above the
upper bound and not one day is below the lower one: the interval is not
narrow, it is **shifted**.
