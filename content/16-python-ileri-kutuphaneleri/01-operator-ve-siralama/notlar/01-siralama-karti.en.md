## Sorting

| Code | What it does |
|---|---|
| `sorted(x)` | a new list, the original unchanged |
| `x.sort()` | in place, returns `None` |
| `sorted(x, reverse=True)` | largest to smallest |
| `sorted(x, key=str.casefold)` | ignoring case |
| `sorted(x, key=len)` | by length |
| `sorted(d.items(), key=itemgetter(1))` | a dictionary by value |
| `sorted(x, key=lambda r: (r["a"], -r["b"]))` | a ascending, b descending |

## operator

| Code | Equivalent |
|---|---|
| `itemgetter(1)` | `lambda r: r[1]` |
| `itemgetter("age")` | `lambda r: r["age"]` |
| `itemgetter(1, 2)` | `lambda r: (r[1], r[2])` |
| `attrgetter("price")` | `lambda o: o.price` |
| `methodcaller("lower")` | `lambda s: s.lower()` |
| `operator.add`, `mul`, `neg` | `+`, `*`, unary minus |

## heapq and bisect

| Code | What it gives |
|---|---|
| `heapq.nlargest(n, x, key=...)` | the largest n |
| `heapq.nsmallest(n, x, key=...)` | the smallest n |
| `bisect.bisect(sorted_list, v)` | where v would go (right of equals) |
| `bisect.bisect_left(sorted_list, v)` | left of equals |
| `bisect.insort(sorted_list, v)` | insert without breaking the order |

## Remember

- Python's sort is stable: equal elements keep their arrival order.
- Mixed types (`3` and `"a"`) cannot be sorted.
- Moving `None`s to the end: `key=lambda v: (v is None, v)`.
