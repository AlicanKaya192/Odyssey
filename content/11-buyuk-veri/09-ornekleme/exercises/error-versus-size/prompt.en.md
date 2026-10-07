Measure how spread out the estimates are as the sample grows.

**What to do:**

1. `orders = make_orders(200_000)`.
2. Loop over the values 200, 2 000 and 20 000 for `n`. For each `n` take 100
   samples with `random_state` from 0 to 99 and put each one's mean
   `unit_price` in a list.
3. For each `n` print `n` and the standard deviation of the estimates
   (`np.std`, two decimals) on one line.
4. On the last line print the ratio of the spread with samples of 200 to that
   with samples of 20 000 (one decimal).

**Expected output:**

```
200 60.06
2000 19.37
20000 5.95
10.1
```

The sample grew a hundredfold and the spread fell to about a tenth: the
square root rule.
