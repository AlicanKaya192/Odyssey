`city_table(rows)` should turn the `[city, year, sales]` rows (the same
city and year can appear more than once, some cities lack some years) into a
city × year table: `groupby(["city", "year"])["sales"].sum()`, then
`unstack(fill_value=0)`. Return:

- `"years"`: the years in the columns (a list)
- `"cities"`: the cities in the rows (a list)
- `"values"`: the table as a list of lists (`.values.tolist()`)

**Do not write a loop.**

**Expected output:**

```
[2024, 2025]
['Ankara', 'Bursa', 'Izmir']
[120, 110]
[50, 0]
[80, 95]
```
