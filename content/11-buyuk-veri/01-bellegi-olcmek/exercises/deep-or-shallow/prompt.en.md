See for yourself which column `deep=True` makes a difference on.

**What to do:**

1. Write the file of 20 000 orders.
2. Read it with the `payment` column as `object`:
   `pd.read_csv("orders.csv", dtype={"payment": object})`.
3. Measure the memory of the `payment` column first without `deep`, then with
   `deep=True` (`df["payment"].memory_usage(...)`); print the two numbers on
   one line.
4. Do the same for the `quantity` column.
5. For `payment`, print the ratio of the deep measurement to the shallow one,
   rounded to one decimal.

**Expected output:**

```
160132 1075752
160132 160132
6.7
```

For the numeric column the two measurements are the same; for `object` text
the shallow one is a small part of the truth.
