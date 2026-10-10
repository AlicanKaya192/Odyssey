# asyncio

In the previous section you overlapped waits with threads. **asyncio** does
the same job in a single thread: the moment a function starts waiting it says
"I am waiting, you carry on" and the turn passes to the next one. Servers that
handle thousands of network connections at once (FastAPI, aiohttp) work with
this model. This section covers the `async` / `await` syntax, running jobs
together, time limits, errors and the most common mistake (blocking while
waiting).

## async def, await, asyncio.run

```python
import asyncio


async def fetch(n):
    await asyncio.sleep(0.2)
    return n * n


async def main():
    pending = fetch(2)
    print(type(pending).__name__)
    print(await pending)


asyncio.run(main())
```

```text
coroutine
4
```

- **`async def`** defines a **coroutine** function. Calling it does not run
  it; it returns a `coroutine` object (the first line).
- **`await`** runs the coroutine and waits for its result. `await` can only be
  written inside another `async def`.
- **`await asyncio.sleep(0.2)`** means "I will wait 0.2 seconds; let other
  work run meanwhile". `time.sleep` does not say that (see below).
- **`asyncio.run(main())`** sets up the event loop, runs `main` to the end and
  closes it. It is usually called once, at the very top of the program.

## gather: waiting together

```python
import asyncio
import time


async def fetch(n):
    await asyncio.sleep(0.2)
    return n * n


async def main():
    start = time.perf_counter()
    one_by_one = [await fetch(n) for n in range(5)]
    sequential = time.perf_counter() - start
    start = time.perf_counter()
    together = await asyncio.gather(*(fetch(n) for n in range(5)))
    concurrent = time.perf_counter() - start
    print(one_by_one, together)
    print(sequential >= 1.0, concurrent < 0.5)


asyncio.run(main())
```

```text
[0, 1, 4, 9, 16] [0, 1, 4, 9, 16]
True True
```

- Calling one after another with `await` adds up the waits: 5 × 0.2 = 1
  second.
- **`asyncio.gather(coroutines...)`** starts them all together and, once all
  are done, returns the results as a list **in the given order**. On this
  computer, 0.2 seconds.
- There is one thread; the speed comes from switching to another coroutine
  during the wait.

## The most common mistake: blocking while waiting

```python
import asyncio
import time


async def blocking(n):
    time.sleep(0.2)
    return n


async def main():
    start = time.perf_counter()
    await asyncio.gather(*(blocking(n) for n in range(3)))
    blocked = time.perf_counter() - start
    start = time.perf_counter()
    await asyncio.gather(*(asyncio.to_thread(time.sleep, 0.2) for _ in range(3)))
    offloaded = time.perf_counter() - start
    print(blocked >= 0.6, offloaded < 0.4)


asyncio.run(main())
```

```text
True True
```

- **`time.sleep`** **stops** the event loop: no coroutine can run meanwhile.
  Even with `gather`, the three jobs ran one after another (0.6 s). The same
  goes for `requests.get`, reading a big file, or a long computation.
- Inside `async def`, only waits that can be **`await`ed** are used:
  `asyncio.sleep`, async libraries (`aiohttp`, `httpx`'s async client, async
  database drivers).
- If you must call a blocking function, **`asyncio.to_thread(f, ...)`** runs
  it in a separate thread and the loop stays free (0.2 s).

## Time limits: timeout

```python
import asyncio


async def slow():
    await asyncio.sleep(1)
    return "done"


async def main():
    try:
        async with asyncio.timeout(0.1):
            await slow()
    except TimeoutError:
        print("TimeoutError")
    try:
        await asyncio.wait_for(slow(), timeout=0.1)
    except TimeoutError:
        print("wait_for: TimeoutError")


asyncio.run(main())
```

```text
TimeoutError
wait_for: TimeoutError
```

- **`async with asyncio.timeout(seconds):`** puts a time limit on everything
  inside the block; when time is up, the work inside is **cancelled** and
  `TimeoutError` is raised.
- **`asyncio.wait_for(coroutine, timeout=...)`** does the same for a single
  job.
- Every job that waits for the network gets a time limit; a server that does
  not answer must not keep the program waiting forever.

## Tasks and errors: TaskGroup

```python
import asyncio


async def job(name, delay, fail=False):
    await asyncio.sleep(delay)
    if fail:
        raise ValueError(name)
    return name


async def main():
    async with asyncio.TaskGroup() as group:
        a = group.create_task(job("a", 0.2))
        b = group.create_task(job("b", 0.1))
    print(a.result(), b.result())
    try:
        async with asyncio.TaskGroup() as group:
            group.create_task(job("x", 0.1, fail=True))
            y = group.create_task(job("y", 0.5))
    except* ValueError as errors:
        print([str(e) for e in errors.exceptions], y.cancelled())
    results = await asyncio.gather(job("p", 0.1), job("q", 0.05, fail=True),
                                   return_exceptions=True)
    print(results)


asyncio.run(main())
```

```text
a b
['x'] True
['p', ValueError('q')]
```

- **`create_task`** starts a coroutine right away as a **task**.
- **`asyncio.TaskGroup`** is a group of tasks: when the `async with` block
  ends, all tasks in the group are waited for. Results with `task.result()`.
- If one task in the group fails, **the others are cancelled** (`y` was
  cancelled before finishing) and the errors are gathered in an
  `ExceptionGroup`. **`except*`** catches the errors of a given type in that
  group.
- **`gather(..., return_exceptions=True)`** puts the error in place of the
  result instead of raising it: even if one fails, the others complete.

## How many at once? Semaphore

```python
import asyncio


async def download(n, gate, state):
    async with gate:
        state["active"] += 1
        state["peak"] = max(state["peak"], state["active"])
        await asyncio.sleep(0.05)
        state["active"] -= 1
        return n


async def main():
    gate = asyncio.Semaphore(3)
    state = {"active": 0, "peak": 0}
    results = await asyncio.gather(*(download(n, gate, state) for n in range(10)))
    print(len(results), state["peak"])


asyncio.run(main())
```

```text
10 3
```

- Ten tasks started at once, but at most three at a time could pass through
  the **`asyncio.Semaphore(3)`** gate (`peak` is 3).
- Sending a thousand requests to a server at once strains it (and you); most
  APIs limit the number of simultaneous requests. A semaphore keeps that limit
  in code.

## When asyncio?

| Situation | Choice |
|---|---|
| Many network waits, an async library exists | `asyncio` |
| A few waits, the library is synchronous (`requests`) | `ThreadPoolExecutor` |
| CPU-heavy computation | `ProcessPoolExecutor` |
| A blocking call inside async code | `asyncio.to_thread` |

## Summary

- `async def` defines a coroutine; `await` runs it and waits; at the very top
  `asyncio.run(main())`.
- `gather` waits together; results in the given order.
- No `time.sleep` or synchronous I/O inside `async def`; `to_thread` if
  needed.
- Time limits with `asyncio.timeout` / `wait_for`.
- `TaskGroup`: if one fails, the others are cancelled; catch with `except*`.
- `Semaphore(n)` limits the number of jobs at once.
