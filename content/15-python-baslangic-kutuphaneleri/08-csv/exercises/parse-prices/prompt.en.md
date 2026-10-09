There is a `prices.csv` saved from Turkish Excel next to your file: the
columns are `product` and `price`, the separator is a semicolon, the decimal
separator a comma (`3,50`), and the file starts with a BOM.

Write the function `parse_prices(path)`: return a dictionary from product
name to price (`float`).

**Expected output:**

```
book 12.9
eraser 1.25
pen 3.5
```
