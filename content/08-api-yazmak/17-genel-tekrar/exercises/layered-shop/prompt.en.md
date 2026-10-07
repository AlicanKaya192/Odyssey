`errors.py` (`OutOfStock`), `deps.py` (`require_key`, `X-Api-Key: letmein`)
and `stock.py` are ready.

**What to do:**

1. `routers/orders.py`: a router with the `/orders` prefix whose **every**
   endpoint requires the key; `POST /orders/{item}` raises
   `OutOfStock(item)` if out of stock (it mustn't know HTTP), otherwise
   decreases by one and returns `{"item": ..., "left": ...}`.
2. `main.py`: add the router; a handler turning `OutOfStock` into `409`,
   `{"error": "out_of_stock", "item": ...}`.

- `POST /orders/pen` (no key) → `401`
- `pen` with the key → `{"item": "pen", "left": 1}`
- `book` with the key → `409`
