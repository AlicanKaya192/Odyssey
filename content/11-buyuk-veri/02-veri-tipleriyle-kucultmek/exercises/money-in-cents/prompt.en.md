Work out the total of a million orders' prices with three different ways of
storing them and compare the drifts.

**What to do:**

1. Build the table with `make_orders(1_000_000)`; `prices = df["unit_price"]`.
2. The real total: `prices.sum()`.
3. The `float32` total: make the prices `float32` and add them up **inside
   `float32`** (`.sum()`), turning the result into a number with
   `float(...)`.
4. The cents total: turn the prices into cents
   (`(prices * 100).round().astype("int64")`), add them up and divide by 100.
5. Print the three totals, rounded to two decimals, on separate lines.
6. On the last line print the `float32` total's difference from the real
   total and the cents total's difference from the real total, both to two
   decimals, on one line.

**Expected output:**

```
736869041.37
736869056.0
736869041.37
14.63 0.0
```

The cents total matches the real total to the cent; the `float32` total
drifted by 14.63 lira.
