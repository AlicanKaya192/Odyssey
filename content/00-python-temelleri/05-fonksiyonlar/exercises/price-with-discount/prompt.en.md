You are going to write a small sales calculation.

Define a function called `total_price`. It takes three parameters:

| Parameter | Meaning |
|---|---|
| `price` | the unit price of the item |
| `count` | how many were bought |
| `discount` | the discount to apply — **default value 0** |

The function should work out the total and hand it back with `return`:
unit price times count, minus the discount.

Then call the function twice:

- Into `full`, buy 3 of a 50-unit item with **no discount**.
- Into `reduced`, make the same purchase **with a discount of 20**.

Print both, one under the other.

Expected output:

```
150
130
```

> Do not use `print` inside the function. Hand the result back with `return` and
> do the printing outside.
