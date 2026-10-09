There is a `sales.csv` next to your file; its columns are `date`, `customer`, `city`, `amount`. Some cities contain a comma (`"London, UK"`).

Write the function `total_by(path, key, value)`: return, as a dictionary,
the total of the `value` column (`float`) for every `key` value; totals
`round(..., 2)`. Example: `total_by("sales.csv", "customer", "amount")`.

**Expected output:**

```
Ada 180.5
Alan 80.0
Grace 200.25
Linus 45.0
```
