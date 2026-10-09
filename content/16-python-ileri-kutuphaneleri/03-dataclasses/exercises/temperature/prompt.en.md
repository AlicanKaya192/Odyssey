The `Temperature` dataclass: `celsius: float` and `fahrenheit: float`,
which is not asked for in `__init__` (`field(init=False)`). In
`__post_init__`, raise `ValueError("below absolute zero")` if celsius is
below -273.15, otherwise compute `fahrenheit = celsius * 9 / 5 + 32`.

**Expected output:**

```
Temperature(celsius=100, fahrenheit=212.0)
ValueError: below absolute zero
```
