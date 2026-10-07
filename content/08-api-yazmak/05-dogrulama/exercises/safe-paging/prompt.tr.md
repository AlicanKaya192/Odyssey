`items` listesi hazır (8 öğe).

**Yapman gereken:** `GET /items` iki sorgu parametresi alsın ve listeden
bir dilim döndürsün:

- `limit`: 1–5, varsayılan `3`
- `offset`: 0 ya da büyük, varsayılan `0`

- `GET /items` → `["apple", "bread", "cheese"]`
- `GET /items?limit=2&offset=6` → `["grapes", "honey"]`
- `GET /items?limit=6` → `422`
- `GET /items?offset=-1` → `422`
