The same few patterns usually show up at the top of a profile. Two of them are
measured below; in each, the code first checks that the result is the same,
then that the speed went up at least 10 times.

```python
import timeit

customers = [{"id": i, "name": f"c{i}"} for i in range(3_000)]
orders = [{"id": n, "customer": (n * 7) % 3_000} for n in range(3_000)]


def match_nested():
    result = []
    for order in orders:
        for customer in customers:
            if customer["id"] == order["customer"]:
                result.append((order["id"], customer["name"]))
    return result


def match_dict():
    by_id = {c["id"]: c["name"] for c in customers}
    return [(order["id"], by_id[order["customer"]]) for order in orders]


scores = list(range(2_000, 0, -1))


def best_each_time():
    return [sorted(scores)[0] for _ in range(200)]


def best_once():
    best = min(scores)
    return [best for _ in range(200)]


for slow, fast in [(match_nested, match_dict), (best_each_time, best_once)]:
    same = slow() == fast()
    slow_time = min(timeit.repeat(slow, number=1, repeat=3))
    fast_time = min(timeit.repeat(fast, number=1, repeat=3))
    print(slow.__name__, same, slow_time / fast_time > 10)
```

```text
match_nested True True
best_each_time True True
```

On this computer the first got about 600 times faster and the second about
100 times.

## The patterns

| Slow | Fast | Why |
|---|---|---|
| Matching with nested loops | build a dictionary (index) first, then look up | 3000 + 3000 steps instead of 3000 × 3000 comparisons |
| `sorted(...)` every time in a loop | `min` / `sorted` once | not doing the same work 200 times |
| `in` on a list | `in` on a set | a set computes the location directly |
| Dropping repeats with `x not in list` | `dict.fromkeys` / `set` | one pass |
| `list.count(k)` for every key | `Counter` | one pass |
| `insert(0, x)` at the start of a list | `collections.deque.appendleft` | no shifting |
| `iterrows` row by row in pandas | a column operation (vectorised) | the loop runs in C |

The shared idea: **do not do the same work over and over** and **pick the
right data structure**. Which pattern matters in your program is, again, what
the profile tells you.
