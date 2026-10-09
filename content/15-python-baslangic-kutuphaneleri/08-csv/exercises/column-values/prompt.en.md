There is a `sales.csv` next to your file; its columns are `date`, `customer`, `city`, `amount`. Some cities contain a comma (`"London, UK"`).

Write the function `column_values(path, column)`: read the file with
`csv.DictReader` and return the values of the given column in order as a
list. The starter code uses `split(",")`; look at the output.

**Expected output:**

```
London, UK
Wilmslow
New York, US
Helsinki
London, UK
```
