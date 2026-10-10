## concurrent.futures

| Code | What it does |
|---|---|
| `with ThreadPoolExecutor(max_workers=8) as pool:` | a thread pool |
| `pool.map(f, inputs)` | results in input order |
| `future = pool.submit(f, x)` | one job, returns a Future |
| `future.result(timeout=5)` | wait for the result; the job's error is raised here |
| `as_completed(futures)` | the first to finish comes first |
| `wait(futures, timeout=1)` | `(done, not_done)` sets |
| `ProcessPoolExecutor` | a process pool (CPU work) |

## threading

| Code | What it does |
|---|---|
| `t = threading.Thread(target=f, args=(x,))` | define a thread |
| `t.start()`, `t.join()` | start, wait |
| `lock = threading.Lock()` + `with lock:` | one thread at a time |
| `threading.active_count()` | the number of running threads |
| `queue.Queue()`; `put`, `get` | a safe queue |

## Choosing

| Work | Tool |
|---|---|
| Waiting for network, disk, database | `ThreadPoolExecutor` |
| Pure Python computation | `ProcessPoolExecutor` + `if __name__ == "__main__":` |
| Thousands of simultaneous connections | `asyncio` |

## Traps

- Changing shared data without a lock: increments get lost.
- Never calling `future.result()`: the job's error stays invisible.
- Opening a process pool without `if __name__ == "__main__":`.
- Not giving queue workers a stop signal: `join()` hangs.
