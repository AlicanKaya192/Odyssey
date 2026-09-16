You will print a product's price, its tax and the total **with cents**.

The data you have:

```python
price = 12.5
tax_rate = 0.18
```

**What to do:**

1. `tax` — the amount of tax (`price * tax_rate`).
2. `total` — the price with tax.
3. Print all three as below, with **two decimal places**.

**Expected output:**

```
Price: 12.50
Tax: 2.25
Total: 14.75
```

> Do not use `round()`. The format specifier both rounds and keeps the
> trailing zero: `f"{price:.2f}"`.
