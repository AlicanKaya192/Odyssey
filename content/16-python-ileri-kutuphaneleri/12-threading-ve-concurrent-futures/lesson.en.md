# threading and concurrent.futures

A program spends much of its time **waiting**: for a reply from the network, a
file from disk, a result from the database. Sending five requests one after
another and waiting for each takes as long as all the waits added up.
**Threads** let the program move on to other work while it waits. This section
covers `threading` and the easy interface on top of it, `concurrent.futures`:
when they speed things up, when they do not, and what can break in shared
data.

## Other work while waiting: ThreadPoolExecutor

```python
import time
from concurrent.futures import ThreadPoolExecutor


def fetch(n):
    time.sleep(0.2)
    return n * n


start = time.perf_counter()
one_by_one = [fetch(n) for n in range(5)]
sequential = time.perf_counter() - start

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=5) as pool:
    together = list(pool.map(fetch, range(5)))
threaded = time.perf_counter() - start

print(one_by_one, together)
print(sequential >= 1.0, threaded < 0.5)
```

```text
[0, 1, 4, 9, 16] [0, 1, 4, 9, 16]
True True
```

- `fetch` imitates a function waiting for data from the network: it sleeps
  for 0.2 seconds. Five of them in a row take 1 second; with the pool, about
  0.2 seconds on this computer.
- **`ThreadPoolExecutor(max_workers=5)`** builds a **pool** of five threads.
  `pool.map(function, inputs)` hands each input to a free thread; the results
  come back **in input order**.
- When the `with` block ends, the pool waits for all the work to finish and
  shuts down.
- It helps because a sleeping (waiting) thread lets go of the processor;
  network, disk and database waits are like that.

## The Thread object: starting and waiting by hand

```python
import threading

results = {}


def work(name, n):
    results[name] = sum(range(n))


threads = []
for i in range(1, 4):
    threads.append(threading.Thread(target=work, args=(f"t{i}", 10 ** i)))
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print(sorted(results.items()))
print(threading.active_count())
```

```text
[('t1', 45), ('t2', 4950), ('t3', 499500)]
1
```

- **`Thread(target=function, args=(...))`** defines a thread, **`start()`**
  runs it, **`join()`** waits for it to finish.
- A thread cannot **return** a value; the result is written to a shared
  structure (a dictionary here). The pool's `map`/`submit` do this for you,
  which is why they are usually preferred.
- Once all are `join`ed, only the main thread remains: `active_count()` is 1.

## Race conditions and Lock

```python
import threading
import time

count = 0


def add():
    global count
    for _ in range(1000):
        value = count
        time.sleep(0)
        count = value + 1


workers = [threading.Thread(target=add) for _ in range(4)]
for w in workers:
    w.start()
for w in workers:
    w.join()
print(count < 4000)

count = 0
lock = threading.Lock()


def safe_add():
    global count
    for _ in range(1000):
        with lock:
            value = count
            time.sleep(0)
            count = value + 1


workers = [threading.Thread(target=safe_add) for _ in range(4)]
for w in workers:
    w.start()
for w in workers:
    w.join()
print(count)
```

```text
True
4000
```

- Four threads add 1000 each; 4000 is expected. But if another thread steps in
  between "read" and "write" (`sleep(0)` makes that easy here), two of them
  read the same old value and write the same new value: increments **get
  lost**. On this computer the result was different on every run (between
  1047 and 1622).
- **`threading.Lock`** is a lock: only one thread at a time enters a
  `with lock:` block. The read-change-write step becomes indivisible; the
  result is 4000.
- The rule: every piece of shared data that several threads **change** is
  protected with a lock. Data that is only read, and results returned by the
  pool, are no problem.
- A single line like `count += 1` is not safe either: underneath it is still
  read-add-write. On this computer an unlocked `+=` showed no error, but
  Python does not guarantee it; such a bug is very hard to find when it
  finally appears.

## Future: the promise of a result

```python
from concurrent.futures import ThreadPoolExecutor, as_completed


def check(x):
    if x < 0:
        raise ValueError(f"negative: {x}")
    return x * 10


with ThreadPoolExecutor() as pool:
    futures = {pool.submit(check, x): x for x in [1, -2, 3]}
    done = []
    for future in as_completed(futures):
        x = futures[future]
        try:
            done.append((x, future.result()))
        except ValueError as error:
            done.append((x, f"error: {error}"))
print(sorted(done))
```

```text
[(-2, 'error: negative: -2'), (1, 10), (3, 30)]
```

- **`pool.submit(function, argument)`** puts the work in the queue at once and
  returns a **Future**: a promise that "the result will be here later".
- **`future.result()`** waits for the result and gives it. If the work raised
  an error, the error is raised **here**, when `result()` is called; if you do
  not catch it, it is not lost.
- **`as_completed(futures)`** gives the jobs **in the order they finish**; the
  first to finish comes first. Since the order can change on every run, the
  result is sorted at the end.
- Keeping a Future → input mapping in a dictionary is the common way to know
  which result belongs to which input.

## CPU-heavy work: the GIL and ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def cpu(n):
    total = 0
    for i in range(n):
        total += i * i
    return total


if __name__ == "__main__":
    jobs = [300_000] * 4
    plain = [cpu(n) for n in jobs]
    with ThreadPoolExecutor(max_workers=4) as pool:
        threaded = list(pool.map(cpu, jobs))
    with ProcessPoolExecutor(max_workers=4) as pool:
        processed = list(pool.map(cpu, jobs))
    print(plain == threaded == processed, plain[0])
```

```text
True 8999955000050000
```

- Standard Python (CPython) has a **GIL** (global interpreter lock): only one
  thread runs Python code at a time. A waiting thread releases the lock, so
  the pool speeds up I/O work; but in loops that compute, the threads take
  turns.
- Running the same code with `jobs = [3_000_000] * 4` and timing it, on this
  computer: 0.63 s one after another, still 0.63 s with threads, **0.39 s
  with the process pool**.
- **`ProcessPoolExecutor`** starts separate Python processes; each has its
  own GIL and the jobs really run at the same time. The price: starting a
  process takes time, inputs and results travel with pickle (the pickle
  section), and for small jobs there can be more loss than gain.
- **`if __name__ == "__main__":`** is required: on Windows a new process
  imports the file from the top; without the guard every process tries to
  start new processes.
- Since Python 3.13 there is also a separate GIL-free ("free-threaded") build
  of Python; there, threads can speed up computation too. The Python on this
  computer has the GIL.

## Which one when?

| Work | Tool |
|---|---|
| Waiting for network, disk, database (I/O) | `ThreadPoolExecutor` |
| Pure Python computation, big loops (CPU) | `ProcessPoolExecutor` |
| NumPy / pandas computation | usually not needed; the library runs in C |
| Thousands of simultaneous connections | `asyncio` (the next section) |

## Summary

- `ThreadPoolExecutor` + `map` / `submit`: overlaps the waits.
- `Thread(target=..., args=...)`, `start()`, `join()`; the result goes into a
  shared structure.
- Every place that changes shared data: `with lock:`.
- Future: `result()` gives the result or raises the job's error;
  `as_completed` is the finishing order.
- For CPU work, a process pool and `if __name__ == "__main__":`.
