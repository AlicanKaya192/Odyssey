`advice(city)` in `weather.py` gets the temperature from `fetch_temp`;
`fetch_temp` goes to the network and fails in tests. Fake the temperature with
`patch("weather.fetch_temp", return_value=...)` and write at least **three**
tests: 5 degrees → `"coat"`, 20 degrees → `"t-shirt"` and the boundary:
**10 degrees → `"t-shirt"`**.

**Expected output:**

```

```
