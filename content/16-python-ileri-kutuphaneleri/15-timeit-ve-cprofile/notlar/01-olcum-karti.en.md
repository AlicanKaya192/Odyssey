## timeit

| Code | What it does |
|---|---|
| `timeit.timeit("code", setup="...", number=1000)` | the total time (s) |
| `timeit.timeit(function, number=10)` | measure a function |
| `min(timeit.repeat(..., number=n, repeat=5))` | the most reliable single value |
| `python -m timeit -s "setup" "code"` | the command line |

## cProfile and pstats

| Code | What it does |
|---|---|
| `p = cProfile.Profile(); p.enable() ... p.disable()` | profile a section |
| `p.runcall(f, x)` | profile a single call |
| `pstats.Stats(p).sort_stats("cumulative").print_stats(10)` | print the first 10 rows |
| `sort_stats("tottime")` | by its own time |
| `python -m cProfile -s cumtime app.py` | the whole program |
| `-o profile.out` | write the result to a file |

## Columns

| Column | Meaning |
|---|---|
| `ncalls` | how many times it was called |
| `tottime` | time spent inside the function itself |
| `cumtime` | total time including what it calls |
| `percall` | time / call |

## The order

1. Prepare a test or comparison that confirms the result.
2. Profile and find the biggest `cumtime` / `tottime` item.
3. Fix only that.
4. Is the result the same? Measure again.
