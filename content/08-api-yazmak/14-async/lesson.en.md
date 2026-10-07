# async and await

An API spends most of its time **waiting**: for the database's answer,
another API's answer, a file on disk. While it waits, the processor is
idle. `async` and `await` let you deal with other requests in that idle
time. FastAPI has both, and knowing which to write when matters: written
wrongly, the server silently slows down.

## An analogy

Think of a waiter. If they hand the order to the kitchen and **wait** by the
stove until the food is cooked (`time.sleep`), they can't look after another
table meanwhile. If they hand over the order, say "tell me when it's
ready" and go to another table (`await`), they can look after many tables at
once. `async def` means "this function can switch to other work at its
waiting points"; `await` is that waiting point.

## Two kinds of endpoint

```python
import asyncio
import time


@app.get("/async-sleep")
async def wait_well():
    await asyncio.sleep(0.5)        # other requests are handled while waiting
    return {"ok": True}


@app.get("/sync-sleep")
def wait_in_thread():
    time.sleep(0.5)                 # FastAPI runs this in a separate thread
    return {"ok": True}
```

We sent **five requests at once** to each (we measured):

```text
/async-sleep   5 requests at once: 0.51 s
/sync-sleep    5 requests at once: 0.54 s
```

Both are fine: five requests finished in half a second.

- `async def` + `await`: in one thread, switching to other requests while
  waiting.
- Plain `def`: FastAPI runs each request in a **thread pool**; while one
  waits, the others progress in their own threads.

## The real trap: blocking inside `async def`

```python
@app.get("/async-block")
async def wait_badly():
    time.sleep(0.5)                 # no await!
    return {"ok": True}
```

```text
/async-block   5 requests at once: 2.52 s
```

Five times slower. An `async def` function runs on FastAPI's **single**
event loop; `time.sleep` isn't a waiting point, it locks the loop. For that
half second the server can't look at **any** request; requests queue up.
The code works and gives no error, it's just slow: that's why it's hard to
notice.

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>await asyncio.sleep(0.5)</h4><p>Request 1 waits → the loop moves on to requests 2, 3...<br>5 requests: <b>0.51 s</b></p></div>
    <div class="no"><h4>time.sleep(0.5) (inside async def)</h4><p>Request 1 locks the loop → the others wait in line.<br>5 requests: <b>2.52 s</b></p></div>
  </div>
  <figcaption>The same code, the same result, five times the time. Blocking inside <code>async def</code> stops the whole server (we measured).</figcaption>
</figure>

## The rule

| Inside the function | Write |
|---|---|
| Things called with `await` (`asyncio.sleep`, async libraries) | `async def` |
| Ordinary blocking calls (`time.sleep`, `sqlite3`, `requests`) | `def` |
| Only calculation, no waiting | Either works; `def` is safe |

If you're not sure, write `def`. A wrong `def` spends a few resources; a
wrong `async def` locks the whole server.

`sqlite3` and `requests` are **blocking** libraries: endpoints using them
must be `def`. That's why every endpoint in the previous sections is `def`.

## Several waits: one after another, or together?

Let an endpoint need data from two places (0.3 s each):

```python
async def fetch(name, seconds):
    await asyncio.sleep(seconds)    # like waiting for another API
    return name


@app.get("/one-by-one")
async def one_by_one():
    weather = await fetch("weather", 0.3)
    news = await fetch("news", 0.3)
    return [weather, news]


@app.get("/together")
async def together():
    return await asyncio.gather(fetch("weather", 0.3), fetch("news", 0.3))
```

```text
/one-by-one  0.62 s ['weather', 'news']
/together    0.31 s ['weather', 'news']
```

`asyncio.gather` starts both waits **at the same time**; the time is as long
as the longest one. Independent waits (where one's result isn't needed by
the other) are combined this way. The result list keeps the order they were
given in.

## Work without waiting for the answer: `BackgroundTasks`

Sending a welcome email to someone who signed up takes time; they don't need
to wait for it. FastAPI can leave the work until **after** the answer:

```python
from fastapi import BackgroundTasks


def send_welcome(email: str):
    time.sleep(0.5)                 # a slow job, like sending an email
    log.append(f"welcome mail to {email}")


@app.post("/signup")
def signup(email: str, tasks: BackgroundTasks):
    tasks.add_task(send_welcome, email)
    return {"queued": True}
```

We measured with a real server (uvicorn):

```text
POST /signup          0.03 s  {"queued": true}
GET /log (right away) []
GET /log (0.7 s)      ["welcome mail to ada@x.org"]
```

The answer went out at once and the work finished afterwards. Note:
`TestClient` **waits** for the background work to finish (the same request
took 0.31 s in a test); in tests the work appears already done.

A background task may be cut off if the server stops; it isn't used for work
that must never be lost (a payment).

## Summary

- `async def` + `await`: switches to other requests while waiting.
- Plain `def`: FastAPI runs it in a thread pool; this is what you write with
  blocking libraries (`sqlite3`, `requests`).
- `time.sleep` or a blocking call inside `async def` locks **the whole
  server** (measured: 5 times slower).
- Independent waits at the same time with `asyncio.gather`.
- `BackgroundTasks`: work to do after the answer.
