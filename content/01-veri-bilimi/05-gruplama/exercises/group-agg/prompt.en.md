Instead of a single calculation you will do **three at once** and produce a
report table.

**What you need to do:**

1. Group by city and produce a three-column report called `report`:
   - `people` — how many people are in that city
   - `average` — the mean score
   - `highest` — the highest score
2. **Round to one place** and print the result.
3. Print how many people are in Izmir on its own.

**Expected output:**

```
        people  average  highest
city
Ankara       3     87.0       91
Bursa        2     69.0       70
Izmir        3     71.3       76
3
```

**The form you will use:**

```python
data.groupby("city").agg(
    new_name=("which column", "which calculation"),
    ...
)
```

This reads best when producing a report: you choose the column names, and
what is computed from where is visible at a glance.

Because the result is a table, you can take a single cell with
`loc[row, column]`.
