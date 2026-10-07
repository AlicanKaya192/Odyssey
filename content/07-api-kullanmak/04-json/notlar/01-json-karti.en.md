Everything you need to go back and forth between JSON and Python.

## Four functions

| Function | Direction | With |
|---|---|---|
| `json.loads(text)` | JSON → Python | Text |
| `json.dumps(obj)` | Python → JSON | Text |
| `json.load(handle)` | JSON → Python | A file |
| `json.dump(obj, handle)` | Python → JSON | A file |

A way to remember: **`s` = string**.

## Type counterparts

| JSON | Python |
|---|---|
| `{"a": 1}` object | `dict` |
| `[1, 2]` array | `list` |
| `"text"` | `str` |
| `3`, `3.5` | `int`, `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

## `dumps` settings

```python
json.dumps(obj, indent=2)            # readable, indented
json.dumps(obj, ensure_ascii=False)  # non-English letters as they are
json.dumps(obj, sort_keys=True)      # keys in alphabetical order
```

## Not JSON

| Python | What to do |
|---|---|
| `tuple` | Becomes a list on its own |
| `set` | Raises an error → `sorted(s)` |
| a date | Raises an error → the text `"2024-03-01"` |
| `{1: "a"}` | The key becomes `"1"` |

## Is it valid?

```text
{"city": "Izmir"}      valid
{'city': 'Izmir'}      single quotes → invalid
{"ok": True}           capital True → invalid (must be true)
{"a": 1,}              trailing comma → invalid
{"note": None}         None → invalid (must be null)
```
