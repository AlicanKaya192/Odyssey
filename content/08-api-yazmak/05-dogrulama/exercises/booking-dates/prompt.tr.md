Bir otel rezervasyonu. Günler yılın kaçıncı günü olarak geliyor (1–365).

**Yapman gerekenler:**

1. `check_in`, `check_out`: 1–365. `guests`: 1–4, varsayılan `1`.
2. `check_out`, `check_in`'den **sonra** olmalı (aynı gün de olmaz):
   `model_validator(mode="after")`.
3. `POST /bookings` → `{"nights": check_out - check_in, "guests": ...}`

- `{"check_in": 10, "check_out": 13}` → `{"nights": 3, "guests": 1}`
- `{"check_in": 10, "check_out": 10}` → `422`
- `{"check_in": 10, "check_out": 8, "guests": 2}` → `422`
- `{"check_in": 10, "check_out": 12, "guests": 5}` → `422`
