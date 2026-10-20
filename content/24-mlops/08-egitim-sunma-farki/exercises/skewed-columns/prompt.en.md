The column means in training and at serving time are given in the same order. Write the function `skewed_columns(names, trained, live, tolerance)` and return, in order, the names of the columns with a big difference:

- A big difference: `abs(live - trained) > tolerance * abs(trained)`.
- If the training mean is `0`, no ratio can be made: flag it if the live one isn't `0` too.

**Expected output:**

```
['monthly_fee', 'support_calls', 'is_pro']
[]
```
