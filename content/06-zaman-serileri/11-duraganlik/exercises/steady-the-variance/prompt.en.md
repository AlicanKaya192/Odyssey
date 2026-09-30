Measure why differencing is not enough for the passenger series and what
the logarithm fixes.

**What to do:**

1. Compute `d = p.diff()`. Print its standard deviation for three periods
   (2013–2016, 2017–2020, 2021–2024), rounded to one decimal, as a list.
2. Print the same for `np.log(p).diff()` with three decimals.
3. For each list print the ratio of the last period to the first, rounded to
   two decimals, on one line.
4. The yearly growth rate: `growth = np.log(p).diff(12)`. Print its mean as a
   percentage rounded to one decimal (`growth.mean() * 100`).
5. Print the date of the first defined value of `growth` and its number of
   `NaN` values on one line.

**Expected output:**

```
[14.2, 23.0, 34.7]
[0.093, 0.097, 0.1]
2.44 1.08
10.2
2014-01-01 12
```

With the plain difference the size of the waves grows 2.4 times from period to
period; after the logarithm the ratio is very close to 1. Yearly growth
averages around 10%: while the level tripled, the growth **rate** stayed
constant.
