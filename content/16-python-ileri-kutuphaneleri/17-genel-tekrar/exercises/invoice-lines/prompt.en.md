`invoice_total(rows, rate)` computes the total of `[name, "price", qty]`
rows with a tax rate (`rate`, a string) but uses `float`. Rewrite it like
this:

- Turn each row into a `@dataclass` named `Line` (`name: str`,
  `price: Decimal`, `qty: int`).
- Compute the subtotal with `Decimal` and multiply it by `(1 + Decimal(rate))`.
- Round the result with `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`
  and return it as **text**.

**Expected output:**

```
34.12
```
