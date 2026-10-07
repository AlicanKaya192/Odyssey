What runs in which order in a `yield` dependency. We measured with two
requests; the dependency writes to a log at each step:

```python
def resource():
    log.append("open")
    try:
        yield "R"
    except HTTPException as e:
        log.append(f"saw {e.status_code}")
        raise
    finally:
        log.append("close")
```

## The endpoint succeeds

```text
GET /ok   200 {"r": "R"}
log:      open → endpoint → close
```

## The endpoint raised `HTTPException`

```text
GET /fail   404 {"detail": "nope"}
log:        open → endpoint → saw 404 → close
```

- The endpoint's error comes back into the dependency **at the `yield`
  line**; `except` can see it.
- `finally` ran in both cases.
- The error was raised again with `raise` inside `except`, so the client
  still got `404`. Without `raise` the error would be swallowed; don't do
  that.

## When is it used?

| Resource | Before `yield` | In `finally` |
|---|---|---|
| A SQLite connection | `sqlite3.connect(...)` | `conn.close()` |
| A transaction | — | `commit` if no error, otherwise `rollback` |
| A temporary file | open the file | close/delete the file |
| Timing | the start time | write the elapsed time |

You'll use the first row in the database section.
