There is a `sales.csv` next to your file; its columns are `date`, `customer`, `city`, `amount`. Some cities contain a comma (`"London, UK"`).

Write the function `filter_rows(src, dst, column, minimum)`: write the rows
of `src` whose `column` value (`float`) is equal to or greater than
`minimum` to `dst` with the same header (`DictReader` + `DictWriter`,
`reader.fieldnames`) and return how many rows it wrote.

**Expected output:**

```
2
date,customer,city,amount
2026-03-01,Ada,"London, UK",120.50
2026-03-02,Grace,"New York, US",200.25
```
