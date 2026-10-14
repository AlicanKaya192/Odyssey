`order_total(order_id)` should find the order in `ORDERS` of the read-only
`shop_data.py` and return `{"order_id": ..., "total": ...}`: the total is
the sum of price × count for every `[product, unit price, count]` in the
order, rounded to 2 places. If there is no such order,
`{"error": "no order <number>"}`.

**Expected output:**

```
{'order_id': 'ORD-10077', 'total': 214.9}
{'order_id': 'ORD-61890', 'total': 78.5}
{'error': 'no order ORD-00000'}
```
