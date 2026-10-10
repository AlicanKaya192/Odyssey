`cart_total(prices)` adds up prices (strings like `"19.99"`) but because it
uses `float`, results like `3.3000000000000003` come out. Rewrite the
function with `Decimal`; return the total as **text** (`str`). An empty list
gives `"0"`.

**Expected output:**

```
3.30
25.10
```
