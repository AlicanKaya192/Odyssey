Write the function `measure(func, repeat)`: call `func` `repeat` times,
measure each call with `time.perf_counter()` and return the **shortest**
duration in seconds. The lines below test the function: they count the calls
and expect the shortest of three calls that take 0.3, 0.05 and 0.2
seconds.

**Expected output:**

```
True
4
True
True
```
