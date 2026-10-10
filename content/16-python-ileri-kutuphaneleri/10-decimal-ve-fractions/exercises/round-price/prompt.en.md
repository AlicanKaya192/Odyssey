Write the function `round_price(text, rule)`: turn `text` into a `Decimal`
and round it to two decimals. If `rule` is `"up"`, use `ROUND_HALF_UP`; if
`"even"`, `ROUND_HALF_EVEN`. Return the result as text (`"2.665"`, `"up"` →
`"2.67"`).

**Expected output:**

```
2.67 2.66
10.00
```
