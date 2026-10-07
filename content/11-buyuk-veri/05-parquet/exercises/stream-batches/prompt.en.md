Read the Parquet file in pieces with `iter_batches` and find the quantity
sold per category.

**What to do:**

1. The starter code writes 200 000 orders in a single group.
2. Loop with `iter_batches(batch_size=60_000, columns=["category", "quantity"])`;
   turn each piece into a table with `to_pandas()`.
3. In each piece add the result of `groupby("category")["quantity"].sum()`
   to a list; also count the pieces.
4. Combine the results (`pd.concat(...).groupby(level=0).sum()`), sort from
   largest to smallest and print the category and total quantity on each
   line.
5. On the last line print the number of pieces.

**Expected output:**

```
clothing 99008
books 97594
home 87918
electronics 62055
toys 53359
sports 43992
4
```
