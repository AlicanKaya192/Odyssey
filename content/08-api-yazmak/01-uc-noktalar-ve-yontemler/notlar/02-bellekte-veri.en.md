Patterns and traps of keeping data in memory before we move to a database
(the Database section).

## Patterns

```python
state = {"count": 0}          # a single value
notes = []                     # a list of records
books = {}                     # records by id: {1: {...}, 2: {...}}
next_id = {"value": 1}         # the next id
```

All of them **outside** the functions, at the top of the file. Changing
their insides from a function is fine: `notes.append(...)`,
`books[3] = ...`, `state["count"] += 1`.

## Traps

**Defining the data inside the function.**

```python
@app.post("/counter")
def increase():
    state = {"count": 0}   # back to 0 on every request
    state["count"] += 1
    return state           # always {"count": 1}
```

**Changing a plain variable.**

```python
count = 0


@app.post("/counter")
def increase():
    count += 1   # UnboundLocalError: cannot access local variable 'count'
```

Python treats a name assigned inside a function as local. Either use a
dictionary or list, or write `global count` at the start of the function; a
dictionary is less surprising.

**Everything is wiped when the server restarts.** Because `--reload`
restarts on every save, the data is reset often; this is not a bug, it is
the nature of memory.

**Several workers.** In production a server is sometimes run with several
processes (`--workers 4`); each process has **its own** memory, and two
requests may go to two different counters. That is why shared data is kept
in a database.
