How much of the memory goes to numbers, and how much to text?

**What to do:**

1. Write the file of 20 000 orders and read it into `df`.
2. Separate the numeric columns with `df.select_dtypes("number")` and the
   text columns with `df.select_dtypes(exclude="number")`.
3. Measure the memory of both groups with
   `memory_usage(deep=True, index=False).sum()` (`index=False` leaves out the
   index).
4. Print each group's share of the total as a percentage, rounded to one
   decimal: first `numbers`, then `text` (example form: `numbers 12.3`).
5. Print the table's bytes per row (total / number of rows), rounded to one
   decimal.

**Expected output:**

```
numbers 31.8
text 68.2
100.5
```

Four of the eight columns are text, but their share of memory is far more
than half.
