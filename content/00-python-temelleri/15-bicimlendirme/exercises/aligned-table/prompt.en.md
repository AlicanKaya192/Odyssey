You will print a product table with the columns lined up.

The data you have:

```python
rows = [("Pencil", 3, 12.5), ("Notebook", 12, 145.0), ("Eraser", 5, 7.25)]
```

**What to do:**

1. Print the header row first: product, quantity, price.
2. Then print each row **with a loop**.
3. The name is left aligned in **12**, the quantity right aligned in **5**,
   and the price right aligned in **10** with two decimal places.

**Expected output:**

```
Product       Qty     Price
Pencil          3     12.50
Notebook       12    145.00
Eraser          5      7.25
```

> Use the same widths in the header, otherwise it will not sit on top of
> the columns.
