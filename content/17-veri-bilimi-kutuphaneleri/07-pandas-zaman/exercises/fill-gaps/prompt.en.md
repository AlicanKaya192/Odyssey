`fill_gaps(dates, values, how)` should add the missing days to the date-indexed
series with `asfreq("D")` and fill them according to `how`:

- `"zero"`: `fillna(0)`
- `"ffill"`: `ffill()`
- `"interpolate"`: `interpolate()`

Return the result as a list rounded to 1 place.

**Expected output:**

```
zero [40.0, 42.0, 0.0, 0.0, 51.0]
ffill [40.0, 42.0, 42.0, 42.0, 51.0]
interpolate [40.0, 42.0, 45.0, 48.0, 51.0]
```
