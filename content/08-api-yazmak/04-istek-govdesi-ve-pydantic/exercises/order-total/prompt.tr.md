**Yapman gerekenler:** iki model ve bir uç nokta.

- `Item`: `name` (metin), `price` (ondalıklı sayı), `qty` (tam sayı,
  varsayılan `1`).
- `Order`: `customer` (metin), `items` (`Item` listesi).
- `POST /orders`: `{"customer": ..., "lines": kalem sayısı, "total": ...}`.
  `total` her kalemin `price * qty` toplamı, `round(..., 2)` ile.

```json
{"customer": "Ada", "items": [
  {"name": "pen", "price": 1.5, "qty": 4},
  {"name": "book", "price": 12.25}]}
```

Cevap: `{"customer": "Ada", "lines": 2, "total": 18.25}`

Bir kalemin fiyatı sayı değilse (`"price": "free"`) `422`.
