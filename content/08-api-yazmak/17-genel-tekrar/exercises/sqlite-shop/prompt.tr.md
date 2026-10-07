`products` tablosu (`name` `UNIQUE`) ve `get_db` hazır.

**Yapman gerekenler:**

1. `POST /products` → `201`, `{"id": ..., "name": ..., "price": ...}`;
   aynı ad `409` (`"Product already exists"`).
2. `GET /products?max_price=...` → `id` sırasıyla; `max_price` verilirse
   `price <= max_price`. Değeri `?` ile ver.
3. `DELETE /products/{id}` → `204`; silinen satır yoksa `404`
   (`"Product not found"`).
