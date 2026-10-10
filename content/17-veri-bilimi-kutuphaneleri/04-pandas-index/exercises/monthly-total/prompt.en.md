`monthly_total(jan, feb)` takes two months' city → sales dictionaries. It
should turn both into `pd.Series` and add them **by label**; a city missing in
one month counts as 0 (`add(..., fill_value=0)`). Return the result as a
`{city: int}` dictionary. The starter code adds by order with `.values`.

**Expected output:**

```
Ankara 220
Bursa 50
Izmir 170
Konya 40
```
