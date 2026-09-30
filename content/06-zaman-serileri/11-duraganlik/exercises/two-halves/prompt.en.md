`stock_price.csv` holds the daily closing price of a share (`date`,
`close`). Without calling a test, split the series in two and see whether it
is stationary.

The price is read in the starter code as `k`.

**What to do:**

1. Write a function `halves(x)`: it splits the series in the middle
   (`half = len(x) // 2`, `x.iloc[:half]` and `x.iloc[half:]`) and returns
   four numbers rounded to two decimals as a **tuple**: the mean of the first
   half, the mean of the second half, the standard deviation of the first
   half, the standard deviation of the second half. Turn the numbers into
   plain numbers with `float(...)`.
2. Print the result of `halves(k)`.
3. Compute the daily change (`k.diff().dropna()`) and print its `halves`.

**Expected output:**

```
(119.75, 144.06, 10.01, 17.66)
(0.02, 0.15, 2.14, 2.4)
```

For the price the mean went from 120 to 144 and the standard deviation from
10 to 18: not stationary. For the series of changes the two halves are almost
the same: stationary.
