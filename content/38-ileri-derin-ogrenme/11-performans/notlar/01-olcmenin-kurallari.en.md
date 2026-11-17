A wrong measurement is worse than none at all: you "fix" the wrong place and
leave the real bottleneck. A few rules make a measurement trustworthy.

## Rules

- **Warm-up:** the first call is always slow (memory allocation, caches,
  compilation). Run it once before measuring, or take the shortest of several
  repeats.
- **Repeat:** a single measurement is noise. Another program running in the
  background can double one measurement; the shortest is the closest to the
  job's real cost.
- **Same conditions:** the two paths you compare are measured with the same
  data, the same batch size and the same number of threads. PyTorch uses
  several threads on the CPU (`torch.get_num_threads()`); on another machine
  that number differs and so do the times.
- **Think in ratios:** "0.3 s" says nothing; "the batch is more than ten
  times faster" means something on every machine.

## A Python loop or a tensor operation?

The most common slowness is walking a tensor's elements one by one in
Python.

```python
import time
import torch


def timeit(fn, repeat=3):
    best = float("inf")
    for _ in range(repeat):
        start = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - start)
    return best


t = torch.randn(100_000, generator=torch.Generator().manual_seed(0))
slow = timeit(lambda: sum(v for v in t.tolist()))
fast = timeit(lambda: t.sum())
print(fast < slow / 10)
print(abs(sum(t.tolist()) - t.sum().item()) < 1e-2)
```

```text
True
True
```

- The same sum: Python adds every number as a separate object; `t.sum()` adds
  the whole array in C code, in one call. On this computer the difference is
  tens of times.
- The second line: the two results are not identical (in floating point the
  order of addition changes the last digits) but they are the same number.

The same rule holds everywhere: preprocessing that walks rows with `for`, a
loop full of `.item()` calls, or a training loop that prints at every step
can eat more time than the model itself.
