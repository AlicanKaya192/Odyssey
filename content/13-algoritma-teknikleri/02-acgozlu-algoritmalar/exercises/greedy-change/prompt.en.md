Write the function `greedy_change(amount, coins)`: it returns the list of
coins for the change (largest to smallest) by always giving **the largest coin
that fits**. `coins` may not come sorted; it always contains `1`.

The second line shows where greedy fails: two coins (`3 + 3`) are enough for
6, but greedy gives three.

**Expected output:**

```
[50, 25, 10, 1, 1]
[4, 1, 1]
```
