In a directional test, every customer's probabilities **before** (`before`) and **after** (`after`) the change are given in the same order. The probability is expected not to fall. Write the function `directional_share(before, after, tolerance)`:

- If the probability after is not less than the one before minus `tolerance`, the test counts as held for that customer (very small drops are tolerated).
- Return the share of customers it held for, rounded to three digits.
- If the list is empty, `None`.

**Expected output:**

```
0.75
1.0
None
```
