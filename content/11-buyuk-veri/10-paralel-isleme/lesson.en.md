# Parallel Processing

Your computer's processor has several **cores**; each can do a separate job.
Python tells you how many there are on this computer:

```python
import os
print(os.cpu_count())
```

```text
24
```

But the Python code you write uses **only one** of them by default. Parallel
processing means splitting the work into independent pieces and running the
pieces **at the same time** on different cores. In this section we measure
how that is done, when it really speeds things up and when it does the
opposite and slows them down. The second part is at least as important as the
first.

## Processes and threads

There are two ways to have work done at the same time:

<figure class="fig">
  <div class="versus">
    <div><h4>Process</h4><p>A separate Python, its own memory<br>Data goes by being copied<br>Not affected by the GIL<br>Expensive to start</p></div>
    <div><h4>Thread</h4><p>In the same process, shared memory<br>Data is not copied<br>Python code runs one at a time because of the GIL<br>Cheap to start</p></div>
  </div>
  <figcaption>Processes for pure Python arithmetic; threads for waiting and NumPy work.</figcaption>
</figure>

- **Process:** a Python that runs like a separate program, with its own
  memory. Processes cannot see each other's variables; data goes from one
  process to another by being **copied**.
- **Thread:** a strand of work inside the same process, sharing the same
  memory. Data is not copied, but because of the lock below, Python code cannot
  run at the same time.

## The GIL: Python's lock

Inside Python (CPython) there is a lock called the **GIL** (*Global
Interpreter Lock*): in one process **only one** thread can run Python code at
a time. Even if you open four threads, pure Python arithmetic is done one at a
time.

There are two exceptions; in these two cases a thread releases the lock:

1. **While waiting:** while reading a file, waiting for a reply from the
   network, during `time.sleep`.
2. **Inside NumPy and pandas:** big array calculations are done in C, and the
   lock is released meanwhile.

So the rule is simple: **processes for pure Python arithmetic, threads for
waiting and for NumPy work.**

## `concurrent.futures`

`concurrent.futures` from Python's standard library lets you use both ways in
the same form: `ProcessPoolExecutor` (a process pool) and `ThreadPoolExecutor`
(a thread pool). The `map` method of both applies a function to every item in
a list and gives the results **in the same order**.

A job heavy on pure Python: counting the primes between 0 and 400 000. Let us
split the range into eight pieces and try three ways:

```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def count_primes(bounds):
    start, stop = bounds
    count = 0
    for n in range(start, stop):
        if n < 2:
            continue
        d = 2
        while d * d <= n:
            if n % d == 0:
                break
            d += 1
        else:
            count += 1
    return count

if __name__ == "__main__":
    parts = [(i * 50_000, (i + 1) * 50_000) for i in range(8)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        total = sum(ex.map(count_primes, parts))
    print(total)
```

On this computer (the faster of two tries):

| Way | Result | Time |
|---|---|---|
| Sequential (`map`) | 33 860 | 1.09 s |
| 4 threads | 33 860 | 1.12 s |
| 4 processes | 33 860 | 0.50 s |

- Threads did not speed it up at all: because of the GIL, the primes were
  still counted one at a time.
- Four processes cut the work by more than half. Not four times, because
  starting processes has a cost too (more on that shortly).
- All three results are the same: running in parallel **must not change the
  answer**. Always check this.

## Why is `if __name__ == "__main__":` required?

On Windows a new process starts by **running your program from the top**. If
the code builds a pool at the outermost level of the file, every new process
tries to build a pool too, which starts new processes… In Odyssey this
unprotected code ran into the time limit.

```python
if __name__ == "__main__":
    # only the main program builds the pool
    ...
```

`__name__` is `"__main__"` in the main program and something else inside the
helper processes. The code under this line runs only once, in the main
program. The helper processes only read the **definitions** of the functions.
That is also why the function you give to the processes (`count_primes`) must
be defined at the outermost level of the file.

## Threads for waiting

In jobs such as fetching ten pages from an API or downloading ten files, most
of the time goes on **waiting**. A waiting thread releases the lock, so threads
are very effective here. Ten jobs that each wait 0.2 seconds:

```python
import time
from concurrent.futures import ThreadPoolExecutor

def wait(i):
    time.sleep(0.2)
    return i

with ThreadPoolExecutor(max_workers=10) as ex:
    result = list(ex.map(wait, range(10)))
```

2.01 seconds sequentially, 0.21 seconds with ten threads: all ten waits
happened at once.

NumPy's big calculations release the lock too: eight 600 × 600 matrix
calculations took 0.23 seconds sequentially and 0.06 seconds with four
threads.

## The cost of parallelism

Starting a process, sending it data and getting the result back are not free.
If the job is small, this cost swallows the gain.

**Very small jobs.** Squaring ten thousand numbers:

| Way | Time |
|---|---|
| Sequential | 0.0009 s |
| 4 processes, each number separately | 1.78 s |
| 4 processes, `chunksize=2_500` | 0.20 s |

Sending each number to a process separately made the job two thousand times
slower. `chunksize` sends the numbers in groups of 2 500 and cuts down the
back and forth, but it is still far behind the sequential calculation.

**Sending a pandas table.** I split two million orders into eight pieces and
worked out the revenue per city with four processes:

| Way | Time |
|---|---|
| Sequential, one table | 0.09 s |
| 4 processes, pieces sent to the processes | 1.14 s |
| Sequential, 8 Parquet files | 0.27 s |
| 4 processes, each process reads its own file | 0.82 s |

The parallel way was **twelve times slower**. The reasons:

1. pandas' grouping is already very fast (in C); there is no heavy work to
   split.
2. Each piece goes to the process by being **copied**.
3. On Windows every new process loads pandas again; on this computer
   `import pandas` alone takes about half a second (0.53–0.69 s).

The lesson: parallel processing is for **heavy, independent** work. If each
piece's work does not take seconds, a single core is usually faster.

## Amdahl's law

Not every part of a program can be parallel: splitting the data, combining
the results and opening the file are done in sequence. **Amdahl's law** says
that the part that cannot be parallel puts a ceiling on the speed-up:

```text
speed-up = 1 / ((1 − p) + p / n)
```

`p` is the share of the work that can be done in parallel, `n` the number of
cores.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>50% parallel</span><span>4 cores: 1.6× · 24 cores: 1.92× · infinite: 2×</span></div>
    <div class="anat-row"><span>90% parallel</span><span>4 cores: 3.08× · 24 cores: 7.27× · infinite: 10×</span></div>
    <div class="anat-row"><span>99% parallel</span><span>4 cores: 3.88× · 24 cores: 19.51× · infinite: 100×</span></div>
  </div>
  <figcaption>The smaller the sequential part, the higher the ceiling. The ceiling is 1 / (1 − p).</figcaption>
</figure>

Even if 90 percent of the work is parallel, 24 cores speed it up only 7.27
times; infinitely many cores cannot pass 10 times. The 10 percent that stays
sequential decides everything.

## When to go parallel?

1. **Is the work heavy?** If each piece does not take at least a few
   seconds, look at other ways first (the right types, Parquet, DuckDB).
2. **Are the pieces independent?** If one's result is needed by another, it
   cannot be parallel.
3. **What kind of work?** Pure Python arithmetic → processes. Waiting
   (network, disk) → threads. NumPy-heavy → threads.
4. **Is the result the same?** Compare it with the sequential solution.

Often the easiest parallelism is **using a tool that splits the work itself**:
DuckDB already uses all the cores (Section 7). dask in the next section also
splits pandas work into pieces and spreads it over the cores by itself.

## Summary

- `os.cpu_count()` gives the number of cores; Python code uses one by
  default.
- A process is a Python with separate memory, a thread a strand of work with
  shared memory in the same process.
- Because of the GIL, threads do not speed up pure Python arithmetic; they do
  speed up waiting and NumPy work.
- `ProcessPoolExecutor` / `ThreadPoolExecutor` and `map`; the order of results
  is kept.
- Code that uses processes must sit under `if __name__ == "__main__":`;
  otherwise on Windows every process starts new processes.
- Parallelism has a cost: with small jobs and pandas jobs where data is sent,
  it was slower than sequential.
- Amdahl: the part that stays sequential puts a ceiling on the speed-up.
