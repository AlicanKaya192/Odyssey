A pool (`ThreadPoolExecutor`) is easy when all the jobs are known up front.
When jobs **arrive over time** (as a file is read, as the user clicks), the
classic pattern is **producer–consumer**: jobs are put in a queue and workers
take them from the queue and process them. `queue.Queue` is safe between
threads; it has its own lock.

```python
import queue
import threading

tasks = queue.Queue()
results = queue.Queue()
STOP = None


def worker():
    while True:
        item = tasks.get()
        if item is STOP:
            break
        results.put((item, item * item))


workers = [threading.Thread(target=worker) for _ in range(3)]
for w in workers:
    w.start()
for n in range(10):
    tasks.put(n)
for _ in workers:
    tasks.put(STOP)
for w in workers:
    w.join()
collected = sorted(results.get() for _ in range(results.qsize()))
print(len(collected), collected[:3], collected[-1])
```

```text
10 [(0, 0), (1, 1), (2, 4)] (9, 81)
```

## The parts

- **`tasks.put(job)`** adds to the queue; **`tasks.get()`** takes a job and,
  if the queue is empty, **waits** (the worker does not spin uselessly).
- **The stop signal** (`STOP = None`): one per worker. When a worker sees the
  signal it leaves the loop. Without the signal the workers wait in `get()`
  forever and `join()` never returns.
- The results are gathered in a queue too; the safe way instead of several
  threads writing to the same list.
- The order of results depends on how fast the workers are; that is why they
  are sorted at the end.

## When a queue, when a pool?

| Situation | Choice |
|---|---|
| The list of jobs is known up front | `ThreadPoolExecutor.map` |
| Jobs arrive over time, a limited number of workers | `queue.Queue` + workers |
| The producer is faster than the consumer; memory must not fill | `queue.Queue(maxsize=100)`: `put` waits when full |
