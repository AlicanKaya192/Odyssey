Write the function `report(argv)`:

- Define `--min` (`type=Decimal`, default `Decimal("0")`) and an optional
  `--customer` with `argparse`.
- Build an in-memory SQLite table `orders (id INTEGER PRIMARY KEY, customer
  TEXT, total TEXT)` and insert `ORDERS` with `executemany`.
- Take the rows; turn the amount into a `Decimal` and drop those below
  `--min` and (if given) those of other customers.
- Return `[id, "amount"]` lists in id order. You can filter the customer in
  SQL with `?`.

**Expected output:**

```
[[1, '19.99'], [3, '12.50'], [4, '40.00']]
[[1, '19.99'], [3, '12.50']]
```
