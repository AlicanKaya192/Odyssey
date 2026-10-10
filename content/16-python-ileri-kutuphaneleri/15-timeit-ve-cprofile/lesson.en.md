# timeit and cProfile

Saying "this code is slow" is easy; guessing **which part** is slow usually
turns out wrong. The rule of speeding up: first **measure**, then fix the place
that takes the most time, then measure again. This section covers two standard
tools: **`timeit`**, which compares small pieces, and **`cProfile`**, which
splits the program's time function by function. A single measurement with a
clock (`time.perf_counter`) was in the time section of the Python Beginner
module.

Times change from computer to computer, so the outputs below print **ratios**
and **counts**, not times. The times on this computer are in the text.

## timeit: measuring a small piece

```python
import timeit

LIST_SETUP = "s = list(range(10_000)); x = 9_999"
SET_SETUP = "s = set(range(10_000)); x = 9_999"
list_time = min(timeit.repeat("x in s", setup=LIST_SETUP, number=1_000, repeat=5))
set_time = min(timeit.repeat("x in s", setup=SET_SETUP, number=1_000, repeat=5))
print(list_time / set_time > 100)
print(type(timeit.timeit("sum(range(100))", number=1_000)).__name__)
```

```text
True
float
```

- **`timeit.timeit(code, setup=..., number=n)`** runs the code `n` times and
  gives the total time in seconds (a `float`). `setup` runs once, outside the
  measurement.
- **`timeit.repeat(..., repeat=5)`** takes the measurement five times and
  gives five times. The **smallest** is taken: the others were affected by
  the computer being busy with something else; the smallest is closest to the
  code's own speed.
- Searching a list checks one by one to the end; searching a set computes the
  location directly. On this computer, for 1000 searches the list took
  0.069 s and the set 0.000024 s: about 2800 times.

## Comparing two solutions

```python
import timeit


def slow_unique(items):
    out = []
    for x in items:
        if x not in out:
            out.append(x)
    return out


def fast_unique(items):
    return list(dict.fromkeys(items))


data = [i % 2_000 for i in range(20_000)]
print(slow_unique(data) == fast_unique(data))
slow = min(timeit.repeat(lambda: slow_unique(data), number=3, repeat=3))
fast = min(timeit.repeat(lambda: fast_unique(data), number=3, repeat=3))
print(slow / fast > 50)
```

```text
True
True
```

- **First check that the results are the same**: fast but wrong code is
  useless.
- `timeit` can take a **function** (here a `lambda`) instead of text; there
  is no need to move variables into `setup`.
- `x not in out` looks through the whole list; as the list grows, every step
  slows down. `dict.fromkeys` drops repeats in one pass while keeping the
  order. On this computer, 3 repeats: 0.42 s against 0.0008 s.
- On the command line: `python -m timeit "sum(range(100))"`; it picks how
  many times to run by itself.

## cProfile: where does the time go?

```python
import cProfile
import pstats
import time


def load():
    time.sleep(0.05)
    return [i % 500 for i in range(50_000)]


def report(rows):
    return {key: rows.count(key) for key in set(rows)}


def main():
    return report(load())


profiler = cProfile.Profile()
profiler.enable()
main()
profiler.disable()
stats = pstats.Stats(profiler)
top = sorted(stats.stats.items(), key=lambda item: -item[1][3])[:5]
for (file, line, name), (cc, calls, total, cumulative, callers) in top:
    print(name, calls)
```

```text
main 1
report 1
<method 'count' of 'list' objects> 500
load 1
<built-in method time.sleep> 1
```

- While **`cProfile.Profile()`** is on (`enable` – `disable`), it records how
  many times every function was called and how much time it took.
- **`pstats.Stats`** reads the results. Each row has two times: **tottime**
  (spent inside the function itself) and **cumtime** (including what it
  calls). Here we sorted by cumulative time.
- Reading it: `main` covers everything; inside, `report` takes most of the
  time, and nearly all of that is `list.count`, called **500 times**. On this
  computer, of the total 0.23 s, `count` took 0.17 and `sleep` 0.05.
- Normally `stats.sort_stats("cumulative").print_stats(10)` prints it as a
  table; the table contains file paths, so here we printed only the names.

## Fixing the bottleneck, measuring again

```python
import cProfile
import pstats
from collections import Counter


def report_slow(rows):
    return {key: rows.count(key) for key in set(rows)}


def report_fast(rows):
    return dict(Counter(rows))


rows = [i % 500 for i in range(50_000)]
print(report_slow(rows) == report_fast(rows))
profiler = cProfile.Profile()
profiler.runcall(report_fast, rows)
names = [name for (_, _, name) in pstats.Stats(profiler).stats]
print("<method 'count' of 'list' objects>" in names)
```

```text
True
False
```

- `rows.count(key)` scans the whole list for every key: 500 keys × 50,000
  items. **`Counter`** counts by going through the list **once**.
- The result is the same; the new profile has no `list.count` call at all
  (`False`).
- **`profiler.runcall(f, ...)`** profiles a single call; no need to write
  `enable`/`disable`.
- The order is always this: measure → find the biggest item → fix → confirm
  the result is the same → measure again.

## From the command line

```text
python -m cProfile -s cumtime app.py     # profile the whole program
python -m timeit -s "s = set(range(10000))" "9999 in s"
```

- `-s cumtime` sorts the table by cumulative time.
- You can also write the profile to a file (`-o profile.out`) and inspect it
  with visual tools (separate packages like `snakeviz`).
- Measuring memory (`tracemalloc`) is in the memory leaks section.

## Do not

- **Speed up without measuring:** making a part that takes 5% of the time
  twice as fast makes the program 2.5% faster.
- **Trust a single measurement:** measure a few times with `repeat`, take the
  smallest.
- **Forget correctness:** does the new solution give the same result as the
  old one?
- **Micro gains for unreadable code:** without a measured, meaningful gain,
  readable code stays.

## Summary

- `timeit.repeat(..., number=n, repeat=r)` → `min(...)`; a function can be
  given too.
- `cProfile.Profile()` + `pstats.Stats`: which function was called how many
  times and how long it took; `tottime` is its own, `cumtime` includes
  sub-calls.
- `runcall(f, ...)` profiles a single call.
- Measure → fix → confirm → measure again.
