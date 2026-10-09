`itertools` and generator expressions are **lazy**: they do not collect the
values in a list up front, they produce them one by one as asked. That gives
two wins: memory and stopping early.

## Memory

```python
import tracemalloc

tracemalloc.start()
total = sum([n * n for n in range(1_000_000)])
list_peak = tracemalloc.get_traced_memory()[1]
tracemalloc.reset_peak()
total2 = sum(n * n for n in range(1_000_000))
gen_peak = tracemalloc.get_traced_memory()[1]
print(total == total2, round(list_peak / 2**20, 1), round(gen_peak / 2**10, 1))
```

```text
True 38.6 4.0
```

`tracemalloc` measures the memory Python allocates. The comprehension in
square brackets **first collected** a million squares in a list: a peak of
about 38.6 **MB**. The generator expression without brackets produced each
square, added it to the sum and forgot it: a peak of about 4 **KB**. The
result is the same; the memory is more than nine thousand times less. If you
walk the values once, there is no need to build a list.

## Stopping early and pipelines

```python
from itertools import islice

lines = ["4", "", "15", "8", "", "23", "42"]
numbers = (int(line) for line in lines if line.strip())
evens = (n for n in numbers if n % 2 == 0)
print(list(islice(evens, 2)))
```

```text
[4, 8]
```

The three steps (skip blank lines, convert to numbers, pick the even ones)
are generators linked to each other: a **pipeline**. None of them runs on its
own; when `islice` asked for two even numbers, the pipeline processed only
`4`, `15` and `8` and **stopped**: `23` and `42` were never looked at. This
is how you avoid reading a whole file of millions of lines when searching
for its first few matches.

## When a list?

| Situation | Choice |
|---|---|
| You walk the values once | generator / `itertools` |
| A very large or infinite stream | generator + `islice` |
| You walk it twice, you need its length | `list(...)` |
| Random access (`x[5]`) | `list(...)` |
| Sorting | `sorted(...)` gives a list anyway |
