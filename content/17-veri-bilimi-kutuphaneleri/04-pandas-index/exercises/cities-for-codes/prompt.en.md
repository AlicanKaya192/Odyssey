`cities_for(rows, codes)` should build a DataFrame from the `[code, city,
stock]` rows (`columns=["code", "city", "stock"]`), make `code` the index and
find the cities of the products in `codes` **in that order** (`loc`). Return
`[cities, total_stock]` (stock as `int`).

**Expected output:**

```
[['Bursa', 'Izmir'], 22]
```
