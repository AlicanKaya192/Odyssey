Work done after the answer, and code that runs while the server starts and
stops.

## Several background tasks

```python
@app.post("/orders")
def place_order(tasks: BackgroundTasks):
    tasks.add_task(update_stock)
    tasks.add_task(send_receipt, "ada@x.org")
    return {"ok": True}
```

The tasks run **in the order they were added**, after the answer (we
measured: `task1`, then `task2 hi`). `add_task(function, arguments...)`: the
arguments come after the function, separated by commas.

## What isn't a background task for?

- Work that must happen (a payment, a record): if the server stops
  meanwhile, the work is cut off and nobody knows.
- Work lasting minutes: it eats the same server's resources. Separate job
  queue systems (Celery, RQ) are used for these.

## On startup and shutdown: `lifespan`

Jobs like loading a model into memory or setting up a database connection
pool should happen **once, not on every request**:

```python
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app):
    events.append("startup")     # while the server starts
    yield
    events.append("shutdown")    # while the server stops


app = FastAPI(lifespan=lifespan)
```

We measured: with `TestClient`, entering the `with` block wrote `startup`
and leaving it wrote `shutdown`. When you serve an ML model you'll load it
right here (the Serving a Model section).

How it differs from a `yield` dependency:

| | `yield` dependency | `lifespan` |
|---|---|---|
| When? | On every request | Once per server |
| Example | A database connection | Loading a model |
