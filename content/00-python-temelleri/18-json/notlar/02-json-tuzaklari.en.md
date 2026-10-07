Most JSON mistakes come from a handful of patterns. If you recognise the
error message, you find the cause right away.

## 1. Mixing up `loads` and `load`

```python
json.loads(file)            # you gave a file, it wanted text
json.load('{"a": 1}')       # you gave text, it wanted a file
```

```text
TypeError: the JSON object must be str, bytes or bytearray, not TextIOWrapper
AttributeError: 'str' object has no attribute 'read'
```

With an `s` it is text, without one a file.

## 2. Writing it like a Python dictionary

| Written | Message |
|---|---|
| `{'name': 'Ada'}` | `Expecting property name enclosed in double quotes` |
| `{"a": 1,}` | `Illegal trailing comma before end of object` |
| `{"a": True}` | `Expecting value` |

All of them are `json.JSONDecodeError`. The `line` and `column` at the end
of the message show where it is broken.

## 3. An empty file

Reading an empty file with `json.load` is an error too:

```text
Expecting value: line 1 column 1 (char 0)
```

For the "no records yet" case, either do not create the file at all and
catch `FileNotFoundError`, or write `[]` the first time.

## 4. Adding to the end with `"a"` mode

```python
with open("log.json", "a", encoding="utf-8") as file:
    json.dump({"run": 1}, file)
```

After two runs the file holds `{"run": 0}{"run": 1}`: two separate JSON
texts side by side. Trying to read it:

```text
Extra data: line 1 column 11 (char 10)
```

A JSON file is one whole: **read → change → write from scratch with `"w"`.**

## 5. Writing with `str()`

`file.write(str(data))` writes Python's picture of the data to the file
(single quotes, `True`, `None`); that is not valid JSON and `json.load`
cannot read it. Always `json.dump`.

## 6. A number key turning into text

```python
back = json.loads(json.dumps({1: "one"}))
back[1]       # KeyError: 1
back["1"]     # "one"
```

Keep the number as a **value**, not a key (`{"id": 1}`), or convert it with
`int(...)` after reading it back.

## 7. Sets and other types

```text
TypeError: Object of type set is not JSON serializable
```

Sets and special objects other than tuples (such as dates) do not go into
JSON directly. Before writing, turn them into a type JSON knows: set →
a list with `sorted(...)`.

## 8. Asking for a missing field with square brackets

In data from outside a field may be missing. `user["email"]` raises a
`KeyError`; `user.get("email", default)` does not.
