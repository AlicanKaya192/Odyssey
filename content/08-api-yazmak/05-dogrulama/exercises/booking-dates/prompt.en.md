A hotel booking. Days come as the day of the year (1–365).

**What to do:**

1. `check_in`, `check_out`: 1–365. `guests`: 1–4, default `1`.
2. `check_out` must be **after** `check_in` (the same day isn't allowed):
   `model_validator(mode="after")`.
3. `POST /bookings` → `{"nights": check_out - check_in, "guests": ...}`

- `{"check_in": 10, "check_out": 13}` → `{"nights": 3, "guests": 1}`
- `{"check_in": 10, "check_out": 10}` → `422`
- `{"check_in": 10, "check_out": 8, "guests": 2}` → `422`
- `{"check_in": 10, "check_out": 12, "guests": 5}` → `422`
