Everything you need when working with JSON, on one page.

## Four functions

| Function | What it does |
|---|---|
| `json.loads(text)` | turns JSON text into a Python structure |
| `json.dumps(structure)` | turns a Python structure into JSON text |
| `json.load(file)` | reads the JSON in an open file |
| `json.dump(structure, file)` | writes the structure to an open file as JSON |

The way to remember: **`s` = string (text).** With an `s` it works with text,
without one it works with a file.

## Patterns

```python
import json

# Reading from a file
with open("data.json", encoding="utf-8") as file:
    data = json.load(file)

# Writing to a file (readable, keeping non-English letters)
with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

# A field that may be missing
email = user.get("email", "no email")

# A default if the file is missing or broken
try:
    with open("settings.json", encoding="utf-8") as file:
        settings = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    settings = {"theme": "dark"}
```

## JSON and Python types

| JSON | Python |
|---|---|
| `{ }` object | `dict` |
| `[ ]` array | `list` |
| `"text"` | `str` |
| `36`, `3.5` | `int`, `float` |
| `true`, `false` | `True`, `False` |
| `null` | `None` |

## JSON writing rules

- Strings and keys go in **double quotes**: `"name"`, no single quotes.
- A key is **always text**: `{1: "a"}` is written as `{"1": "a"}`.
- `true`, `false`, `null` in lower case.
- **No comma** after the last item.
- No comments.

## There and back

| In Python | When it comes back from JSON |
|---|---|
| a tuple `(1, 2)` | a list `[1, 2]` |
| a number key `{1: "a"}` | a text key `{"1": "a"}` |
| a set `{"a", "b"}` | cannot be written: turn it into a list with `sorted(...)` first |

## Reading nested data

```python
data["students"][0]["scores"][1]
```

From left to right: one step in, **by key** in a dictionary, **by position**
in a list. If you get stuck, print the in-between step and look at its type
(`type(...)`).
