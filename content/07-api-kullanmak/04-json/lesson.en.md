# JSON: the Language of APIs

The data in an API's response is almost always written in the same format:

```json
{"city": "Istanbul", "temp": 18.5, "rain": false, "days": ["mon", "tue"]}
```

This format is called **JSON** (JavaScript Object Notation). JavaScript is in
the name, but today every language can read and write it. The reason it is
loved is simple: people can read it by eye and programs can process it
easily.

Good news: since you know Python, you already know most of JSON. It looks a
lot like a Python dictionary. In this section you will learn the
similarities, the **differences** and Python's built-in `json` module.

## Why is JSON text?

Only **text** (really, bytes) can travel between a client and a server. A
Python dictionary is an object in memory; you cannot put it on the wire as it
is. So there are two steps:

<figure class="fig">
  <div class="flow">
    <span class="node">Python dictionary<br><small>on the server</small></span><span class="arrow">→ json.dumps →</span>
    <span class="node acc">JSON text<br><small>on the way</small></span><span class="arrow">→ json.loads →</span>
    <span class="node">Python dictionary<br><small>on your side</small></span>
  </div>
  <figcaption>Only text crosses the wire. The object is turned into text and sent, then turned back into an object on the other side.</figcaption>
</figure>

- Turning an object into text is called **serialization**.
- Turning text back into an object is called **parsing** or
  **deserialization**.

The server turns its data into JSON text and sends it; you turn the incoming
text into a Python object and use it.

## JSON's six types

JSON has only six kinds of value, and each has a counterpart in Python:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Object</span><span><code>{"city": "Izmir"}</code> → Python <code>dict</code></span></div>
    <div class="anat-row"><span>Array</span><span><code>["mon", "tue"]</code> → Python <code>list</code></span></div>
    <div class="anat-row"><span>String</span><span><code>"Izmir"</code> → Python <code>str</code></span></div>
    <div class="anat-row"><span>Number</span><span><code>18</code>, <code>18.5</code> → Python <code>int</code>, <code>float</code></span></div>
    <div class="anat-row"><span>Boolean</span><span><code>true</code>, <code>false</code> → Python <code>True</code>, <code>False</code></span></div>
    <div class="anat-row"><span>Null</span><span><code>null</code> → Python <code>None</code></span></div>
  </div>
  <figcaption>All of JSON's types. Objects and arrays can be nested; the rest are single values.</figcaption>
</figure>

That is all. Types such as dates, sets and tuples do not exist in JSON; we
will see shortly how to carry them.

## Differences from a Python dictionary

Because the two look so alike, the differences are easy to miss:

| | JSON | Python |
|---|---|---|
| Text quotes | **Double** quotes only: `"city"` | Single or double: `'city'` |
| True / false | `true`, `false` (lower case) | `True`, `False` |
| Empty value | `null` | `None` |
| Dictionary key | **Text** only | Text, number, tuple... |
| Trailing comma | **Forbidden**: `[1, 2,]` is an error | Allowed |
| Comments | None | `# ...` |

The most common mistake is the first row: taking the dictionary Python
`print`s for JSON. `{'city': 'Izmir'}` is **not valid JSON**, because the
quotes are single.

## `json.loads`: from text to Python

```python
import json

text = '{"city": "Istanbul", "temp": 18.5, "rain": false, "wind": null}'
data = json.loads(text)

print(data)          # {'city': 'Istanbul', 'temp': 18.5, 'rain': False, 'wind': None}
print(data["temp"])  # 18.5
print(type(data))    # <class 'dict'>
```

`loads` means "load string": load the text. The result is an ordinary Python
dictionary; `false` is now `False`, `null` is now `None`. From here on you
work with it like any dictionary.

## `json.dumps`: from Python to text

```python
import json

book = {"title": "Emma", "tags": ["classic", "novel"], "price": 12.5}
text = json.dumps(book)
print(text)   # {"title": "Emma", "tags": ["classic", "novel"], "price": 12.5}
```

`dumps` means "dump string": pour it into text. You use it when sending data
to an API (a `POST` body). The output is now **text**; you cannot take
`text["title"]` out of it.

### Readable output: `indent`

Long JSON on one line is unreadable. `indent` adds indentation:

```python
print(json.dumps(book, indent=2))
```

```json
{
  "title": "Emma",
  "tags": [
    "classic",
    "novel"
  ],
  "price": 12.5
}
```

You will use this a lot when inspecting an API's response.

### Non-English letters: `ensure_ascii`

```python
print(json.dumps({"city": "Kadıköy"}))
# {"city": "Kadıköy"}

print(json.dumps({"city": "Kadıköy"}, ensure_ascii=False))
# {"city": "Kadıköy"}
```

By default `dumps` writes non-English letters as codes such as `ı`. That
is not wrong; `loads` reads it back as `ı`. But when writing to a file or
reading on screen, `ensure_ascii=False` is more readable.

## Reading from and writing to files

`load` and `dump`, without the final `s`, do the same job with a **file**:

```python
import json

with open("books.json", encoding="utf-8") as handle:
    books = json.load(handle)

with open("copy.json", "w", encoding="utf-8") as handle:
    json.dump(books, handle, indent=2, ensure_ascii=False)
```

In short: **with `s` it is a string**, without it a file.

## Nested structures

API responses are often nested: a list inside a dictionary, dictionaries
inside a list.

```python
text = '''
{
  "city": "Izmir",
  "forecast": [
    {"day": "mon", "temp": 24},
    {"day": "tue", "temp": 21}
  ]
}
'''
data = json.loads(text)
print(data["forecast"][1]["temp"])   # 21
```

Read from the outside in: `data["forecast"]` is a list, `[1]` is the second
day (a dictionary), `["temp"]` is that day's temperature. If you get lost,
check what you are holding at each step with `type(...)`.

## Missing keys: `get`

Not every record in a response has every field. `data["wind"]` raises a
`KeyError` if the key is missing; `get` returns a default value instead:

```python
day = {"day": "mon", "temp": 24}
print(day.get("wind"))        # None
print(day.get("wind", 0))     # 0
```

`get` is one of the things you will use most with real APIs.

## Broken JSON: `JSONDecodeError`

If the incoming text is not valid JSON, `loads` raises an error:

```python
import json

try:
    json.loads("{'city': 'Izmir'}")
except json.JSONDecodeError as error:
    print("not JSON:", error)
# not JSON: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

The message also says where the problem is: line 1, column 2, the first
single quote. An API sometimes returns an HTML page instead of JSON when
something goes wrong; code that calls `loads` without checking the status
code fails exactly here.

## Types JSON does not have

`dumps` knows only the six types. Others must first be turned into one of
them:

- A **tuple** becomes a list: `(1, 2)` → `[1, 2]`. It comes back as a list.
- A **set** raises an error: `Object of type set is not JSON serializable`.
  Turn it into a list first with `sorted(...)` or `list(...)`.
- A **date** raises an error too. It is usually carried as text:
  `"2024-03-01"` (the ISO 8601 format from Section 01).
- A **number key** becomes text: `{1: "a"}` → `{"1": "a"}`. Read back, the
  key is `"1"`, not `1`.

## Summary

- JSON is the text format APIs write data in. It has six types: object,
  array, string, number, `true`/`false`, `null`.
- Differences from a Python dictionary: double quotes only, lower-case
  `true`/`false`/`null`, keys are text only, no trailing comma.
- `json.loads(text)` → a Python object; `json.dumps(obj)` → text. `load`/`dump`
  without the `s` work with files.
- `indent=2` gives readable output, `ensure_ascii=False` writes non-English
  letters as they are.
- In nested data, go from the outside in; use `get` for fields that may be
  missing.
- Invalid text raises `json.JSONDecodeError`; sets and dates are turned into
  lists and text first.
