Write the function `top_growth(func)`:

- `tracemalloc.start()`, take a snapshot, call `func()`, take a second
  snapshot.
- Compare them with `compare_to(earlier, "lineno")` and take the
  `traceback[0]` frame of the first statistic.
- Return that line's **source text** with
  `linecache.getline(file, line).strip()` and call `tracemalloc.stop()`.

**Expected output:**

```
kept.append(bytearray(1_000))
```
