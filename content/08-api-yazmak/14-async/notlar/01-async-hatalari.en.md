The most common mistakes with `async`; all measured.

## Forgetting `await`

```python
async def fetch():
    await asyncio.sleep(0.01)
    return "data"


@app.get("/forgot")
async def forgot():
    result = fetch()            # no await
    ...
```

`fetch()` didn't run; `result` is a **coroutine** object
(`type(result).__name__` → `'coroutine'`). Trying to return it in the answer
gives `500`. Python also prints a "coroutine was never awaited" warning.
Everything defined with `async def` is called with `await`.

## A blocking call inside `async def`

| Blocking | Why is it bad? | Instead |
|---|---|---|
| `time.sleep(1)` | Locks the event loop | `await asyncio.sleep(1)` |
| `requests.get(...)` | The same | make the endpoint `def` |
| A `sqlite3` query | The same | make the endpoint `def` |
| A big calculation (millions of loops) | The same | `def` |

We measured: five requests at once to an endpoint with `time.sleep(0.5)`
inside `async def` took **2.52 s**; the correctly written one 0.51 s.

## `await` inside `def`

`await` can only be written inside `async def`; inside a plain `def` it's a
`SyntaxError`. If you need to call an async function from a plain endpoint,
make the endpoint `async def`.

## Which one should I choose?

1. Is there an `await` in the function? → `async def`.
2. Is there a blocking library (`sqlite3`, `requests`, reading files)? → `def`.
3. Neither → `def` (the safe side).

A project can mix both; FastAPI decides for each endpoint separately.
