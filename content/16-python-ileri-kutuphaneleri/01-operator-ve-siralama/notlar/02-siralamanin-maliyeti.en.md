## How many times is key called?

```python
import random

calls = 0


def slow_key(x):
    global calls
    calls += 1
    return -x


result = sorted(range(1000), key=slow_key)
print(calls, result[:3])
comparisons = 0


class Counted:
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        global comparisons
        comparisons += 1
        return self.value < other.value


data = [Counted(v) for v in random.Random(1).sample(range(10_000), 1000)]
sorted(data)
print(comparisons)
```

```text
1000 [999, 998, 997]
8669
```

- **`key` was called only once per element** (1000 elements, 1000 calls).
  Python computes and stores the keys first and compares the stored keys. An
  expensive key (reading a file, computing) is therefore not a problem.
- The number of comparisons is 8,669: about `n × log₂ n` (1000 × 10 ≈
  10,000). The cost of sorting grows a little faster than the number of
  elements.

## When to use what?

| Job | Tool | Why |
|---|---|---|
| The whole list sorted | `sorted` / `sort` | in one go |
| Only the top 10 | `heapq.nlargest(10, x)` | does not sort the whole list |
| The single largest | `max(x, key=...)` | one pass |
| Frequent inserts into a sorted list | `bisect.insort` | no re-sorting each time |
| Is it in a sorted list | `bisect.bisect_left` | binary search, faster than `in` |
| Very frequent "is it in there" | `set` | unordered but the fastest |

On a sorted list, `x in list` looks from start to end; `bisect` looks by
halving. With a million elements that difference means roughly 50,000 times
fewer comparisons (about 20 against a million). Binary search is covered in
detail in the Algorithms path.
