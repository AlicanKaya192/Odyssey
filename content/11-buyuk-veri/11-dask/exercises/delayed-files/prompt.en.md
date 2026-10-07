Run a function that works out each file's revenue lazily and in parallel
with `delayed`.

**What to do:**

1. The starter code writes the four CSV files.
2. Write the function `file_revenue(path)`: it reads the file with pandas and
   returns the total of `quantity * unit_price`.
3. Put the recipes `delayed(file_revenue)(path)` for the four files in a list;
   `total = delayed(sum)(parts)`.
4. Print the name of `total`'s type.
5. Print the result of `total.compute()` rounded to two decimals.

**Expected output:**

```
Delayed
327426855.28
```
