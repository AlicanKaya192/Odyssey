The async counterpart of the producer–consumer pattern from threads is
**`asyncio.Queue`**. This time we shut the workers down not with a stop
signal but by **cancelling** them when the work is done.

```python
import asyncio


async def worker(queue, results):
    while True:
        n = await queue.get()
        await asyncio.sleep(0.01)
        results.append((n, n * n))
        queue.task_done()


async def main():
    queue = asyncio.Queue()
    results = []
    workers = [asyncio.create_task(worker(queue, results)) for _ in range(3)]
    for n in range(10):
        queue.put_nowait(n)
    await queue.join()
    for w in workers:
        w.cancel()
    await asyncio.gather(*workers, return_exceptions=True)
    print(len(results), sorted(results)[:3])


asyncio.run(main())
```

```text
10 [(0, 0), (1, 1), (2, 4)]
```

## The parts

- **`await queue.get()`** waits until a job arrives; while waiting, the loop
  runs other tasks.
- **`queue.task_done()`** says "I finished the job I took".
  **`await queue.join()`** waits until `task_done` has come for every job put
  in the queue: that is, all the work is done.
- The workers are still waiting in `get()`; **`cancel()`** sends them a
  cancellation. `gather(..., return_exceptions=True)` waits for the
  cancellations to finish and swallows the `CancelledError`s.
- `results` is an ordinary list: since we run in one thread, no lock is
  needed. Tasks only switch at `await` points; `results.append` is not
  interrupted.

## The difference from the thread queue

| | `queue.Queue` | `asyncio.Queue` |
|---|---|---|
| Between | threads | tasks in the same loop |
| Waiting | `q.get()` (stops the thread) | `await q.get()` (the loop goes on) |
| Lock | built in | not needed |
| Stopping | a signal (`STOP`) | `join()` + `cancel()`, or a signal |
