Process four Parquet files in four processes, combine the results and
compare them with the calculation done in one process.

**What to do:**

1. Write the function `category_quantity(path)` at the outermost level of the
   file: it reads the file with `pd.read_parquet` and returns the result of
   `groupby("category")["quantity"].sum()`.
2. In the `if __name__ == "__main__":` block:
   - split the table `make_orders(100_000)` into four pieces of 25 000 and
     write them as `part-0.parquet` … `part-3.parquet` (`index=False`),
   - process the four files with `ProcessPoolExecutor(max_workers=2)`;
     combine the results with `pd.concat(...).groupby(level=0).sum()`,
   - sort by category and print the category and total quantity on each
     line,
   - do the same calculation on the whole table and print whether the two
     results are the same.

**Expected output:**

```
books 49172
clothing 49153
electronics 30440
home 44366
sports 22432
toys 26628
True
```
