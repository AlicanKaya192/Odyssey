You have five texts. Some are valid JSON; others were taken for JSON because
they look like Python dictionaries.

**What to do:**

1. Write the function `is_valid(text)`: it returns `True` if `json.loads` can
   read the text and `False` if it raises `json.JSONDecodeError`. Use `try` /
   `except`.
2. For every text in the `samples` list, write `valid` or `invalid`, then the
   text itself.

**Expected output:**

```
valid   {"city": "Izmir"}
invalid {'city': 'Izmir'}
invalid {"ok": True}
invalid [1, 2,]
valid   null
```

`null` on its own is valid JSON too: its value is `None`.
