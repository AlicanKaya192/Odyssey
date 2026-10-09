Complete the `Product` dataclass: the fields are `name: str`,
`price: float`, `quantity: int = 1`; the `total()` method returns
`price * quantity`. Then let `order_total(rows)` build `Product` objects from
`[name, price, quantity]` rows and return the sum of the totals with
`round(..., 2)`.

**Expected output:**

```
Product(name='pen', price=1.5, quantity=4)
18.0
```
