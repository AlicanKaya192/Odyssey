You will print a small receipt: the items, a subtotal, a discount and the
total.

The data you have:

```python
order_no = 7
items = [("Keyboard", 1, 450.0), ("Mouse", 2, 175.5), ("Cable", 3, 39.9)]
discount = 0.1
```

**What to do:**

1. Print the order number with **three digits**, padded with zeros.
2. Print every item with a loop: the name left aligned in **12**, the
   quantity right aligned in **4**, and the line total (`count * price`)
   right aligned in **10** with two digits.
3. `subtotal` — the sum of the lines.
4. `saving` — the discount amount (`subtotal * discount`).
5. `total` — the amount after the discount.
6. Print the last three lines: the label left aligned in **16** and the
   amount right aligned in **10** with two digits. The discount amount is
   **negative**.

**Expected output:**

```
Order 007
Keyboard       1    450.00
Mouse          2    351.00
Cable          3    119.70
Subtotal            920.70
Discount (10%)      -92.07
Total               828.63
```

> The discount label carries the percentage too:
> `f"Discount ({discount:.0%})"`.
