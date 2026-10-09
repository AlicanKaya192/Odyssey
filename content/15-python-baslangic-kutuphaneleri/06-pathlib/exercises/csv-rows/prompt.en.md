Next to your file there is a ready `shop` folder:

- `shop/README.txt`
- `shop/data/sales.csv`, `stock.csv`
- `shop/data/old/sales-2025.csv`
- `shop/src/app.py`

Write the function `csv_rows(folder)`: for every `.csv` file in the folder
and its subfolders, return how many data rows it has, excluding the header
line, as a dictionary. The key is the file's path relative to `folder`, with
`/` (`rglob`, `relative_to`, `as_posix`).

**Expected output:**

```
data/old/sales-2025.csv 4
data/sales.csv 3
data/stock.csv 2
```
