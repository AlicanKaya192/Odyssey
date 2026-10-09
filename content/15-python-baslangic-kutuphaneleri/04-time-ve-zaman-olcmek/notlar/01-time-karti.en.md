## Clocks

| Function | What it gives | What for |
|---|---|---|
| `time.time()` | the timestamp of now (seconds) | logging, stamps |
| `time.perf_counter()` | the most precise monotonic clock | measuring durations |
| `time.monotonic()` | a monotonic clock | "have N seconds passed?" |
| `time.process_time()` | this program's processor time | calculation load |
| `time.time_ns()`, `perf_counter_ns()` | the same, as integer nanoseconds | very short durations |

A **monotonic** clock never goes back; `time.time()` can (when the clock is
corrected).

## Waiting

| Code | What it does |
|---|---|
| `time.sleep(0.5)` | waits half a second |
| `time.sleep(base * 2 ** n)` | exponential backoff (second note) |

## Timestamp ↔ date

| Code | Result |
|---|---|
| `dt.timestamp()` | date → seconds |
| `datetime.fromtimestamp(s, timezone.utc)` | seconds → UTC date |
| `datetime.fromtimestamp(s)` | seconds → **local** date (differs per computer) |
| `time.gmtime(s)` / `time.localtime(s)` | the `time` module's date structure |

## The measuring pattern

```python
import time

start = time.perf_counter()
# the job to measure
elapsed = time.perf_counter() - start
print(f"{elapsed * 1000:.1f} ms")
```

- Measure several times and take **the shortest**.
- Do not put `print` inside the code you measure; writing to the screen takes
  time too.
- The first run is often slower (files, caches); do not count it.
- More careful measuring: `timeit` (advanced Python module).
