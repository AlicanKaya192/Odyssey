You will produce the **table form** of grouping by two keys — the same
thing as a pivot table in Excel.

**What you need to do:**

1. Produce a pivot table with `city` as rows, `grade` as columns and the
   **mean** score in the cells; call it `table`.
2. Print `table`.
3. Print how many cells are **empty**.
4. Print the average of the B grades in Ankara.

**Expected output:**

```
grade      A     B     C
city
Ankara  86.5  88.0   NaN
Bursa    NaN  70.0  68.0
Izmir   76.0  74.0  64.0
2
88.0
```

**The `NaN` cells matter:** **nobody** in Ankara has a C. That does not mean
"the C average in Ankara is zero" — there is no record at all.

The two should not be confused. You could print zeros with `fill_value=0`,
but then those zeros behave like real measurements in later calculations and
drag the averages down.
