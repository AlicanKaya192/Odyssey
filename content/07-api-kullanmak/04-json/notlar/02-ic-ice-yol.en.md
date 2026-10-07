How to reach the value you want in nested JSON: step by step.

## A sample response

```json
{
  "city": "Izmir",
  "updated": "2024-03-01T09:00",
  "forecast": [
    {"day": "mon", "temp": 24, "wind": {"speed": 12, "dir": "N"}},
    {"day": "tue", "temp": 21}
  ]
}
```

## Building the path

The path for "what is Monday's wind speed?":

| Step | Expression | What you hold |
|---|---|---|
| 1 | `data` | a dictionary |
| 2 | `data["forecast"]` | a list (the days) |
| 3 | `data["forecast"][0]` | a dictionary (Monday) |
| 4 | `data["forecast"][0]["wind"]` | a dictionary (the wind) |
| 5 | `data["forecast"][0]["wind"]["speed"]` | `12` |

At each step ask yourself: **a dictionary (by name) or a list (by position)?**
If you are not sure, `print(type(...))`.

## A missing field

Tuesday's record has no `wind`. `data["forecast"][1]["wind"]` raises a
`KeyError`. The safe way:

```python
day = data["forecast"][1]
wind = day.get("wind", {})
print(wind.get("speed", "unknown"))   # unknown
```

`get("wind", {})` gives an empty dictionary when the field is missing; the
second `get` then takes the default from that empty dictionary. That way the
chain does not break.

## Going through every day

```python
for day in data["forecast"]:
    print(day["day"], day["temp"])
```

Looping over dictionaries inside a list is the most common thing you will do
with API responses. The next section is about turning exactly that into a
table.
