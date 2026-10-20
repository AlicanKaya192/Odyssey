Every row of the training table has a customer and a label date (`labels`: `[customer, date]`). The support calls are in a separate list (`calls`: `[customer, date]`). Write the function `calls_as_of(labels, calls)`:

- For every label row, count the calls that customer made **before** the label date (the same day doesn't count).
- Return the `[customer, date, count]` lists in the order of the labels.

Calls made on or after the label date weren't known at prediction time; counting them would be point-in-time leakage.

**Expected output:**

```
['C1', '2026-02-15', 1]
['C2', '2026-02-15', 0]
['C1', '2026-03-10', 3]
```
