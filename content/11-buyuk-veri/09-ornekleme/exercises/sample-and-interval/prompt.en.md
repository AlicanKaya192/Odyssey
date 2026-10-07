Estimate the mean price with a sample and build its confidence interval.

**What to do:**

1. `orders = make_orders(200_000)`; print the real mean `unit_price`, rounded
   to two decimals.
2. Take a sample with `orders.sample(n=5_000, random_state=1)`; print the
   sample mean rounded to two decimals.
3. Print the standard error (`std() / np.sqrt(n)`) rounded to two decimals.
4. Print the lower and upper bounds of the 95% confidence interval (± 1.96
   standard errors), rounded to two decimals, on one line.
5. Print whether the real mean is inside the interval.

**Expected output:**

```
739.31
748.36
12.16
724.54 772.19
True
```
