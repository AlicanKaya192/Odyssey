`encode_cities(train, test)` should encode cities with `OneHotEncoder`: `fit`
on the training cities, `transform` the test cities. The test may hold a city
never seen in training; it must not fail (`handle_unknown="ignore"`). Return:

- `"names"`: the `get_feature_names_out()` names (a list)
- `"test"`: the encoded test as an `int` list of lists

Pass the data as `pd.DataFrame({"city": ...})`.

**Expected output:**

```
['city_Ankara', 'city_Bursa', 'city_Izmir']
[[0, 0, 0], [0, 1, 0]]
```
