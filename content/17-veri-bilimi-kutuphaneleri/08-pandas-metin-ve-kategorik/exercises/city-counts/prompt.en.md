`city_counts(names)` should clean hand-entered city names (`str.strip()`,
`str.title()`) and return how many times each city appears as `{city: count}`
sorted by name (`value_counts().sort_index().to_dict()`). The starter code
counts without cleaning. **Do not write a loop.**

**Expected output:**

```
{'Ankara': 2, 'Izmir': 3}
```
