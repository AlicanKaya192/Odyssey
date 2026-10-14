`validate(data)` should return the list of error codes (the order
matters):

- Only `["object"]` if `data` is not a dictionary.
- `"missing:<field>"` for each missing field, in the order `category`,
  `urgent`, `order_id`.
- `"category"` if `category` is there and not in `LABELS`.
- `"urgent"` if `urgent` is there and not a `bool`.
- `"order_id"` if `order_id` is not `None` and does not fully match
  `ORD-` + five digits.

**Expected output:**

```
[]
['missing:order_id', 'category', 'urgent']
['object']
```
