Patterns and a decision table for writing parallel code.

## A process pool (pure Python arithmetic)

```python
from concurrent.futures import ProcessPoolExecutor

def work(item):            # at the outermost level of the file
    ...

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(work, items))
```

With many small items: `ex.map(work, items, chunksize=1_000)`.

## A thread pool (waiting, NumPy)

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(fetch, urls))
```

## Taking results in the order they finish

```python
from concurrent.futures import as_completed

futures = [ex.submit(work, item) for item in items]
for f in as_completed(futures):
    print(f.result())          # whichever finishes first
```

`map` gives results in the order you gave the items, `as_completed` in the
order they finish.

## `multiprocessing.Pool`

```python
from multiprocessing import Pool

if __name__ == "__main__":
    with Pool(4) as pool:
        results = pool.map(work, items)
```

## Decision table

| Work | Choice |
|---|---|
| A heavy pure Python loop | Process pool |
| Waiting on the network / disk | Thread pool |
| NumPy-heavy arithmetic | Thread pool |
| pandas grouping, small to medium data | Do not parallelise; it is already fast |
| SQL on files | DuckDB (it uses all the cores itself) |
| Splitting pandas work into pieces | dask (Section 11) |

## This computer's measurements

| Work | Sequential | Parallel |
|---|---|---|
| Counting primes, 4 processes | 1.09 s | 0.50 s |
| Counting primes, 4 threads | 1.09 s | 1.12 s |
| 10 × 0.2 s waits, 10 threads | 2.01 s | 0.21 s |
| 10 000 small jobs, 4 processes | 0.0009 s | 1.78 s |
| pandas pieces sent to processes | 0.09 s | 1.14 s |

## Amdahl's law

```text
speed-up = 1 / ((1 − p) + p / n)
```

| Parallel share (p) | 4 cores | 24 cores | Infinite |
|---|---|---|---|
| 50% | 1.6 | 1.92 | 2 |
| 90% | 3.08 | 7.27 | 10 |
| 99% | 3.88 | 19.51 | 100 |
