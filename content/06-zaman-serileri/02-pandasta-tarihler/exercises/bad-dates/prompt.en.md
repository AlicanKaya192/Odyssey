`orders_raw.csv` is the uncleaned version: some `ordered_at` values are
not even dates. Read it with `errors="coerce"`, but not blindly.

**What to do:**

1. Read the file. Convert the `ordered_at` column with
   `format="%d.%m.%Y %H:%M"` and `errors="coerce"` into a new column called
   `ordered`.
2. Print how many values are `NaT`.
3. Print the **raw** `ordered_at` values of the `NaT` rows as a list.
4. Drop the broken rows (`dropna(subset=["ordered"])`) and print the number
   of rows left.
5. Print the earliest order time in the remaining table.

**Expected output:**

```
3
['31.02.2024 10:15', 'unknown', '00.00.0000 00:00']
237
2024-01-03 05:12:00
```

The three broken values are of three different kinds: a day that is not in
the calendar (31 February), a word that is not a date, and a placeholder
filled with zeros. Had you dropped them without looking at which ones were
broken, then on a day you wrote the format wrong you would delete half the
data without noticing.
