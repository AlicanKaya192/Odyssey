`order_total(items, discount, fee, free_over)` should compute the order
amount: `items` are `[price, count]` pairs; find the subtotal, apply a
discount of rate `discount`; if the discounted amount is below
`free_over`, add the shipping fee `fee`. Round the result to 2
places.

**Expected output:**

```
193.41
29.9
```
