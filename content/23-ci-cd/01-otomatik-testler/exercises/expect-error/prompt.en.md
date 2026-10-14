`ages.py` turns text into an age. If it is not a number, or outside 0–150, it raises `ValueError`.

Write at least **four** tests in `main.py`:

- `parse_age("42")` → `42`
- `parse_age("abc")` → `ValueError`
- `parse_age("-1")` → `ValueError`
- `parse_age("200")` → `ValueError`

Use `with pytest.raises(ValueError):` in the tests that expect an error.
