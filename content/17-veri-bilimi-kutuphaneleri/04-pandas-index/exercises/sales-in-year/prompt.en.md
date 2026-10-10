`sales_in_year(rows, year)` should build a table with a `["city", "year"]`
MultiIndex from the `[city, year, sales]` rows and return the given year's
sales in every city as `{city: sales}`. The starter code writes `loc[year]`;
but `loc` looks at the outer level (the city). For an inner level, `xs`.

**Expected output:**

```
{'Ankara': 110, 'Bursa': 65, 'Izmir': 95}
```
