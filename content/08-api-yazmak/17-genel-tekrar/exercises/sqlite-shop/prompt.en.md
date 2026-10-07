The `products` table (`name` is `UNIQUE`) and `get_db` are ready.

**What to do:**

1. `POST /products` → `201`, `{"id": ..., "name": ..., "price": ...}`; the
   same name `409` (`"Product already exists"`).
2. `GET /products?max_price=...` → ordered by `id`; if `max_price` is given,
   `price <= max_price`. Give the value with `?`.
3. `DELETE /products/{id}` → `204`; `404` (`"Product not found"`) if no row
   was deleted.
