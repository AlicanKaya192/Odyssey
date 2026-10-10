`region_sales(orders, regions)` takes orders (`[no, city, amount]`, messy city
names) and a city → region table (`[city, region]`). It should:

1. Clean the city names with `str.strip().str.title()`.
2. Add the region with `how="left"` (no order may vanish).
3. Compute the total amount per region.

Return `{"sales": {region: total}, "unmatched": [numbers of orders with no
region]}`. **Do not write a loop.**

**Expected output:**

```
{'Aegean': 200, 'Central': 50}
[4]
```
