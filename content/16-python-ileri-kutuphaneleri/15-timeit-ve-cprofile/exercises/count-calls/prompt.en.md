`count_calls(n)` should profile `fib(n)` with `cProfile.Profile().runcall`
and return **how many times `fib` was called in total**. In the
`pstats.Stats(profiler).stats` dictionary the key is `(file, line, name)` and
the value is `(cc, nc, tottime, cumtime, callers)`; the total including
recursive calls is `nc`.

**Expected output:**

```
177 1973
```
