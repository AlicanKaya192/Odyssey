**What to do:** two models and an endpoint.

- `Item`: `name` (string), `price` (float), `qty` (integer, default `1`).
- `Order`: `customer` (string), `items` (a list of `Item`).
- `POST /orders`: `{"customer": ..., "lines": number of items, "total": ...}`.
  `total` is the sum of each item's `price * qty`, with `round(..., 2)`.

```json
{"customer": "Ada", "items": [
  {"name": "pen", "price": 1.5, "qty": 4},
  {"name": "book", "price": 12.25}]}
```

Answer: `{"customer": "Ada", "lines": 2, "total": 18.25}`

If an item's price is not a number (`"price": "free"`), `422`.
