Write the function `stock_span(prices)`: for each day it returns the number of
consecutive days, going back and including that day, whose price is **not
greater** than today's (`[100, 80, 60, 70, 60, 75, 85]` →
`[1, 1, 1, 2, 1, 4, 6]`).

Monotonic stack: the stack holds the indices of days with decreasing prices.
Pop those lower than or equal to today's price; the day left on top is the
span's border. On the last line a hundred thousand days keep rising.

**Expected output:**

```
[1, 1, 1, 2, 1, 4, 6]
100000
```
