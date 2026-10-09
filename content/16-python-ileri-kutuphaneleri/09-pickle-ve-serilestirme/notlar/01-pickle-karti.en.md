## Basics

| Code | What it does |
|---|---|
| `pickle.dumps(obj)` | object → `bytes` |
| `pickle.loads(data)` | `bytes` → object |
| `pickle.dump(obj, file)` | write to a file (`"wb"`) |
| `pickle.load(file)` | read from a file (`"rb"`) |
| `pickle.HIGHEST_PROTOCOL` | the newest format |

## Your own class

| Code | When |
|---|---|
| `__getstate__(self)` | return the state to store (remove the lock, the connection) |
| `__setstate__(self, state)` | on load, put the state back and rebuild what was removed |
| `__reduce__(self)` | how the object is built: `(function, arguments)` |

## Errors

| Error | Cause |
|---|---|
| `TypeError: write() argument must be str, not bytes` | the file was opened with `"w"`; it should be `"wb"` |
| `TypeError: cannot pickle '_thread.lock' object` | there is a part that cannot be stored |
| `PicklingError: Can't pickle <function <lambda> ...>` | a lambda or nested function cannot be found by name |
| `AttributeError: module '__main__' has no attribute 'Point'` | the class is missing when loading |
| `UnpicklingError: invalid load key` | the file is not a pickle or is damaged |

## shelve

```python
import shelve

with shelve.open("cache") as db:
    db["key"] = {"a": 1}       # write
    value = db.get("key", {})  # read
    value["a"] = 2
    db["key"] = value          # assign the change back
    del db["key"]              # delete
```

## Rules

- **Never load pickle from an untrusted source**; JSON for the outside world.
- For data kept for a long time, JSON or CSV too: when a class name changes,
  the pickle file no longer opens.
- Where pickle fits: temporary caches inside Python, carrying objects between
  processes.
