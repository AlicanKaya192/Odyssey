# time and Measuring Time

`datetime` deals with the calendar: which day, which hour. The **`time`**
module works at a lower level: it reads the computer's clock, makes the
program wait and measures **how long a job takes**. In this section we look
at the timestamp, waiting with `sleep` and the right way to measure a
duration.

## Timestamps

In many places computers keep time as a single number: the seconds since
**1 January 1970 00:00 UTC** (the Unix epoch). This is called a
**timestamp**; file modification times, server logs and times in APIs are
mostly like this.

```python
import time
from datetime import datetime, timezone

moment = datetime(2026, 3, 15, 14, 30, tzinfo=timezone.utc)
stamp = moment.timestamp()
print(stamp)
print(datetime.fromtimestamp(stamp, timezone.utc))
print(datetime.fromtimestamp(0, timezone.utc))
print(time.strftime("%Y-%m-%d %H:%M", time.gmtime(stamp)))
print(time.time() > stamp, type(time.time()).__name__)
```

```text
1773585000.0
2026-03-15 14:30:00+00:00
1970-01-01 00:00:00+00:00
2026-03-15 14:30
True float
```

- `timestamp()` turns a date into seconds, `datetime.fromtimestamp(number,
  timezone.utc)` turns seconds into a date. 0 seconds is the first moment of
  1970.
- `time.time()` gives the timestamp of now as a decimal; since you are
  reading this section after 15 March 2026, it is `True`.
- `time.gmtime` and `time.strftime` do the same job inside the `time` module;
  in new code `datetime` is more readable.

If `fromtimestamp` is given no time zone, the result is in the computer's
**local** time and differs from computer to computer. Write the zone
explicitly when turning a timestamp into a date.

## Waiting: sleep

```python
import time

start = time.perf_counter()
time.sleep(0.2)
elapsed = time.perf_counter() - start
print(round(elapsed, 1))
```

```text
0.2
```

`time.sleep(seconds)` makes the program wait for the given time; a decimal
duration works too. Where it is often used: not sending too many requests to
an API in a row, waiting before retrying after an error, waiting for a file
to appear. `sleep` waits at least that long, possibly a little more; that is
why we rounded the measured duration.

## Measuring a duration: perf_counter

To measure how long a job takes, **`time.perf_counter()`** is used: read it
before and after the job and take the difference. The value itself means
nothing (its starting point is undefined); only **the difference of two
readings** is meaningful.

```python
import time

wall = time.perf_counter()
cpu = time.process_time()
time.sleep(0.3)
print(round(time.perf_counter() - wall, 1), time.process_time() - cpu < 0.05)
```

```text
0.3 True
```

There are two different durations:

- **`perf_counter`** is the wall clock: the real time from the start of the
  job to its end (0.3 seconds).
- **`process_time`** is only the time the processor worked **for this
  program**. During `sleep` the processor does not work, so it is nearly zero.

If you care about how long the user waits, use `perf_counter`; if you care
about how much load a calculation puts on the processor, use `process_time`.

## Comparing two ways

A single measurement is not reliable: the computer may be busy with
something else at that moment. Running the job a few times and taking the
**shortest** time is a common method; the shortest time is the run in which
the least got in the way.

```python
import time


def measure(func, repeat=5):
    best = float("inf")
    for _ in range(repeat):
        start = time.perf_counter()
        func()
        best = min(best, time.perf_counter() - start)
    return best


items = list(range(100_000))
as_set = set(items)
t_list = measure(lambda: 99_999 in items)
t_set = measure(lambda: 99_999 in as_set)
print(t_list > t_set * 100)
```

```text
True
```

`lambda: ...` packs the job to be measured as a function; `measure` calls it
five times. On this computer searching the list took about **0.4 ms**,
searching the set under **0.0001 ms** (close to the smallest step
`perf_counter` can measure): the list is scanned from start to end, the set
looks directly in the right place. Because durations change from computer to
computer, we printed only the result of the comparison here.

For more careful measurement the standard library has the **`timeit`**
module; it is covered in the advanced Python module together with
`cProfile`, which finds the slow lines of your code.

## Which clock?

```python
import time

for name in ["time", "monotonic", "perf_counter"]:
    info = time.get_clock_info(name)
    print(name, info.monotonic, info.adjustable)
```

```text
time False True
monotonic True False
perf_counter True False
```

`time.time()` is an **adjustable** clock: when the computer's clock is
corrected over the internet or the user changes it by hand, it can even go
backwards. That is why it is not used to measure durations. `monotonic` and
`perf_counter` never go backwards (**monotonic**); they are used for
measuring durations and for checking "have 5 seconds passed?".

## A common mistake: the same name

```python
import time
from datetime import time

try:
    time.sleep(0.1)
except AttributeError as error:
    print("AttributeError:", error)
```

```text
AttributeError: type object 'datetime.time' has no attribute 'sleep'
```

The `datetime` module also has a class called `time`. The second line bound
the name `time` to that class and the module was lost. When using both
modules, write `import time` with `import datetime as dt` or `from datetime
import datetime`; never give the same name to two things.

## Summary

- A timestamp is the seconds since 1970; go back and forth to dates with
  `timestamp()` and `fromtimestamp(..., timezone.utc)`.
- `time.sleep(seconds)` waits.
- A duration is measured with the difference of `perf_counter()`; processor
  time with `process_time()`.
- A single measurement misleads: run several times and take the shortest.
- `time.time()` is for the timestamp of now, not for measuring durations.
- Do not import the `datetime.time` class and the `time` module under the
  same name.
