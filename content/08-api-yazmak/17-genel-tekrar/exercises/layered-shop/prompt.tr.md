`errors.py` (`OutOfStock`), `deps.py` (`require_key`, `X-Api-Key:
letmein`) ve `stock.py` hazır.

**Yapman gerekenler:**

1. `routers/orders.py`: `/orders` önekli, **bütün** uç noktaları anahtar
   isteyen router; `POST /orders/{item}` stok yoksa `OutOfStock(item)`
   fırlatsın (HTTP bilmesin), varsa bir azaltıp `{"item": ..., "left": ...}`.
2. `main.py`: router'ı ekle; `OutOfStock`'u `409`,
   `{"error": "out_of_stock", "item": ...}` cevabına çeviren yakalayıcı.

- `POST /orders/pen` (anahtarsız) → `401`
- anahtarla `pen` → `{"item": "pen", "left": 1}`
- anahtarla `book` → `409`
