`get_order(orders, user, order_id)` should return the order whose id is
`order_id` only if its owner (`owner`) is `user`. If the order does not
exist or belongs to someone else, return `None`. The starter code does
not look at the owner.

**Expected output:**

```
{'id': 1, 'owner': 'ada', 'total': 40}
None
None
```
