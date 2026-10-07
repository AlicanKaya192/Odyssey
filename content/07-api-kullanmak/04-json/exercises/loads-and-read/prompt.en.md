JSON text came back from a weather API. You will turn it into a Python
dictionary and read values out of it.

**What to do:**

1. Turn `text` into a dictionary called `data` with `json.loads`.
2. Print the city, the temperature, whether it rains and the wind in the
   format below.
3. On the last line, print the name of the temperature's Python type
   (`type(...).__name__`).

**Expected output:**

```
city: Istanbul
temp: 18.5
rain: False
wind: None
temp type: float
```

JSON's `false` and `null` arrive in Python as `False` and `None`.
