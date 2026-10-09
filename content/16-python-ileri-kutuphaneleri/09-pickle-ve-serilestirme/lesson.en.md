# pickle and Serialisation

Turning an object in memory into a sequence of bytes that can be written to
a file or sent over a network is called **serialisation**; turning it back
is **deserialisation**. In the Python path's JSON section you saw one way:
`json`. This section covers Python's own format: **`pickle`**. It keeps
tuples, sets, dates and your own classes exactly as they are, which JSON
cannot carry; but that has a price, and the price is a **security** matter.

## dumps and loads

```python
import json
import pickle
from datetime import date

data = {"name": "ada", "tags": {"math", "code"}, "point": (3, 4),
        "born": date(1815, 12, 10)}
blob = pickle.dumps(data)
back = pickle.loads(blob)
print(type(blob).__name__, back == data)
print(type(back["point"]).__name__, type(back["born"]).__name__)
try:
    json.dumps(data)
except TypeError as error:
    print("json:", error)
```

```text
bytes True
tuple date
json: Object of type set is not JSON serializable
```

- **`pickle.dumps(obj)`** turns the object into `bytes`, **`pickle.loads(data)`**
  rebuilds it. The names match `json`: here the `s` means "bytes in memory"
  rather than a string.
- The object that comes back is **equal** and the types are kept: the tuple
  stayed a tuple, the date a date, the set a set. JSON stopped at the set in
  the same dictionary.
- The result is binary data; it cannot be read in a text editor and cannot
  be opened by languages other than Python.

## Writing to a file: dump and load

```python
import pickle
from pathlib import Path

scores = {"ada": [90, 85], "alan": [75]}
path = Path("scores.pkl")
with path.open("wb") as file:
    pickle.dump(scores, file)
with path.open("rb") as file:
    print(pickle.load(file))
try:
    with path.open("w") as file:
        pickle.dump(scores, file)
except TypeError as error:
    print("TypeError:", error)
```

```text
{'ada': [90, 85], 'alan': [75]}
TypeError: write() argument must be str, not bytes
```

- **`pickle.dump(obj, file)`** / **`pickle.load(file)`**: the forms without
  `s` work directly with a file.
- The file is opened in **binary mode**: `"wb"` to write, `"rb"` to read.
  Bytes cannot be written to a file opened in text mode (`"w"`); this is the
  most common mistake.
- The extension is free; `.pkl` or `.pickle` are common.

## Your own objects

```python
import pickle


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


p = Point(1, 2)
back = pickle.loads(pickle.dumps([p, p]))
print(back, back[0] is back[1])
node = {"name": "root"}
node["self"] = node
copy = pickle.loads(pickle.dumps(node))
print(copy["self"] is copy)
blob = pickle.dumps(Point(3, 4))
del Point
try:
    pickle.loads(blob)
except AttributeError as error:
    print("AttributeError:", error)
```

```text
[Point(1, 2), Point(1, 2)] True
True
AttributeError: module '__main__' has no attribute 'Point'
```

- Class instances are stored too: pickle writes the object's **attributes**
  and **its class's name** (`__main__.Point`).
- Two references to the same object come back as **one object** too (`is` →
  `True`); cycles, like a dictionary pointing at itself, are no problem.
- **The class's code is not in the file.** When loading, pickle looks the
  class up by name; if it cannot find it (the class was deleted, renamed, or
  is not defined in another program), loading fails. Pickle files kept for a
  long time are fragile for this reason: renaming a class makes old files
  unreadable.

## Parts that are not stored

Some objects cannot be serialised: locks, open files, database connections.
A class that holds one of them cannot be stored either.

```python
import pickle
import threading


class Counter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def add(self):
        with self.lock:
            self.count += 1

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["lock"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.Lock()


try:
    pickle.dumps(threading.Lock())
except TypeError as error:
    print("TypeError:", error)
c = Counter()
c.add()
c.add()
back = pickle.loads(pickle.dumps(c))
back.add()
print(back.count, type(back.lock).__name__)
```

```text
TypeError: cannot pickle '_thread.lock' object
3 lock
```

- **`__getstate__`** returns the state to store: a copy of the attributes,
  with the lock removed.
- **`__setstate__`** is called when loading: it puts the state back and
  **rebuilds** the lock. The loaded counter keeps working.
- The same pattern applies to connections and caches: do not store them,
  rebuild them on load.

## Security: pickle.loads runs code

```python
import pickle


class Trap:
    def __reduce__(self):
        return (print, ("this ran while loading!",))


blob = pickle.dumps(Trap())
print(len(blob) > 0)
pickle.loads(blob)
```

```text
True
this ran while loading!
```

- **`__reduce__`** says "how to rebuild" an object: a function and its
  arguments. pickle **calls** that function when loading.
- Here a harmless `print` was called; someone with bad intentions can put in
  a call that deletes files or downloads a program the same way. `loads`
  alone is enough; you do not even have to use the object.
- **The rule: never load pickle data from a source you do not trust** (a
  file downloaded from the internet, data a user uploaded, a message from the
  network). For exchanging data with the outside world, JSON is used; JSON
  carries only data and cannot run code.

## shelve: a persistent store like a dictionary

```python
import shelve

with shelve.open("cache") as db:
    db["ada"] = {"score": 90}
    db["alan"] = {"score": 75}
with shelve.open("cache") as db:
    print(sorted(db), db["ada"]["score"])
    db["ada"]["score"] = 100
with shelve.open("cache") as db:
    print(db["ada"]["score"])
    record = db["ada"]
    record["score"] = 100
    db["ada"] = record
with shelve.open("cache") as db:
    print(db["ada"]["score"])
```

```text
['ada', 'alan'] 90
90
100
```

- **`shelve`** is a dictionary on disk: the keys are strings, the values any
  object stored with pickle. It reads and writes each value separately, so it
  does not load all the data into memory.
- **The trap:** `db["ada"]["score"] = 100` was **not written** to the record
  (still 90). `db["ada"]` gives a **copy** read from disk; changing the copy
  does not touch the disk. The right way: take it, change it, **assign it
  back** (`db["ada"] = record`). (`shelve.open(..., writeback=True)` solves it
  too, but keeps everything read in memory.)
- shelve uses pickle too: the same security rule applies.

## Which one when?

| | `json` | `pickle` |
|---|---|---|
| Readable | text, readable by eye | binary |
| Languages | every language | Python only |
| Types | dict, list, str, numbers, `bool`, `None` | almost any Python object |
| Security | data only | can run code while loading |
| Use | file formats, APIs, settings | temporary caches inside Python, between processes |

Python itself uses pickle: `multiprocessing` carries the objects and results
it sends to processes with pickle (the process pool in the Big Data path),
and `copy.deepcopy` uses the same `__reduce__` mechanism.

## Summary

- `pickle.dumps` / `loads` in memory, `dump` / `load` with a file; the file
  `"wb"` / `"rb"`.
- Types and references to the same object are kept; the class is looked up
  by name, its code is not stored.
- `__getstate__` / `__setstate__` for parts that cannot be stored.
- **Untrusted pickle data is never loaded**: `loads` can run code.
- `shelve` is a dictionary on disk; after changing a value, assign it back.
