This section's file is not as clean as the earlier ones. Before building
anything you need to see what you are dealing with.

`cars.csv` holds 120 cars; the columns are `age`, `km`, `engine`, `fuel`,
`gearbox` and `price`.

**What you need to do:**

1. Read the file and print how many rows it has.
2. Find the columns that **have missing values**. Produce a `column:count`
   string for each and print the list. Columns with no gaps must not appear.
3. Print the names of the **text columns** as a list.
4. Print the distinct values in the `fuel` column, **sorted**.

**Expected output:**

```
120
['engine:14']
['fuel', 'gearbox']
['diesel', 'lpg', 'petrol']
```

**Three findings, three problems:**

- **14 rows of `engine` are empty.** sklearn does not work with missing
  values; you would get `ValueError: Input contains NaN`.
- **Two columns are text.** A model works with numbers; you would get
  `could not convert string to float: 'diesel'`.
- **`fuel` has three categories with no order between them.** Saying
  `petrol=0, diesel=1, lpg=2` would teach the model an order that does not
  exist.

The next exercises solve these three in turn.

**A warning:** many sources find text columns with `df.dtypes == "object"`.
In pandas 3, text columns are no longer `object` and that check returns an
**empty list**. The way that works is `select_dtypes(exclude="number")` —
"the columns that are not numbers".
