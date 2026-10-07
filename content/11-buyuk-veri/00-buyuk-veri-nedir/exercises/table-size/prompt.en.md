Write a function that works out how many MB a table will take without
ever reading the file.

**What to do:**

Write a function called `table_mb(rows, columns)`:

- Every value in the table is `int64` or `float64`, so **8 bytes**.
- Find the total bytes with `rows * columns * 8`.
- Turn the result into megabytes (`/ 1024**2`) and return it rounded to
  **one decimal**.

Examples:

- `table_mb(1_000_000, 10)` → `76.3`
- `table_mb(10_000_000, 6)` → `457.8`
- `table_mb(1000, 1)` → `0.0`

The function does not need to print; the checker will call it with
different numbers and look at what it returns.
