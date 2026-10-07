Split the orders into folders by category.

**What to do:**

1. Build the table `df` with `make_orders(100_000)`.
2. Loop with `df.groupby("category")`. For each category create the folder
   `by_category/category=<name>` (`mkdir(parents=True, exist_ok=True)`) and
   write that category's rows, with the `category` column **dropped**, as
   `part-0.parquet` (`index=False`).
3. Print the names of the folders inside `by_category` in sorted order, each
   on its own line.
4. On the last line print the number of folders.

**Expected output:**

```
category=books
category=clothing
category=electronics
category=home
category=sports
category=toys
6
```
