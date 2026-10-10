A real leak does not show up in one go; it becomes visible as the program runs
for hours. The way to watch a long-running service: take a **baseline
snapshot**, then take new snapshots at intervals and compare them with the
baseline. If the same line grows every time, the leak is there.

```python
import tracemalloc

sessions = {}


def serve(request_id):
    sessions[request_id] = {"id": request_id, "data": "x" * 200 + str(request_id)}
    return "ok"


tracemalloc.start()
baseline = tracemalloc.take_snapshot()
growth = []
for batch in range(3):
    for i in range(batch * 2_000, (batch + 1) * 2_000):
        serve(i)
    snapshot = tracemalloc.take_snapshot()
    top = snapshot.compare_to(baseline, "lineno")[0]
    growth.append(top.size_diff // 1024)
print(top.traceback[0].lineno, growth)
```

```text
7 [906, 1816, 2798]
```

## Reading it

- After every 2000 requests, the line that grew the most is always **line 7**
  (`sessions[...] = ...`), and the growth goes up by about 0.9 MB each time:
  sessions are never deleted.
- In a real service, instead of a loop there is a timer or an admin endpoint
  (like `/debug/memory`) that takes a snapshot and writes the top 10 lines to
  the log.
- `tracemalloc` slows the program down and spends memory while it tracks
  allocations; it is not kept on all the time, only switched on while hunting
  a leak.

## Ways to fix it

- **A time limit:** record the last use time of a session and delete old
  sessions at intervals.
- **A count limit:** drop the oldest session with an `OrderedDict` (LRU), or
  use `lru_cache(maxsize=...)`.
- **Keep it outside:** write sessions to a database or a cache server instead
  of memory.

## Checklist

1. Does memory really grow **all the time**, or does it climb to a peak and
   stop? (A cache can fill up and stop; that is not a leak.)
2. Compare snapshots with `tracemalloc`; find the growing line.
3. **Who holds** the objects created on that line? A module-level
   dictionary/list, a registered listener, a stored exception?
4. Put a limit on it or switch to a weak reference.
5. After fixing it, take the same measurement again.
