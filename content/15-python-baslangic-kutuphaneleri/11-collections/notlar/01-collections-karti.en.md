## Counter

| Code | What it does |
|---|---|
| `Counter(items)` | counts |
| `c[x]` | the count (0 if missing) |
| `c.most_common(n)` | the n most frequent, `(item, count)` |
| `c.update(items)` / `c.subtract(items)` | add / subtract |
| `c.total()` | the sum of the counts |
| `a + b`, `a - b`, `a & b`, <code>a &#124; b</code> | add, subtract, smaller, bigger |

## defaultdict

| Code | Default |
|---|---|
| `defaultdict(list)` | `[]`: grouping |
| `defaultdict(int)` | `0`: counting |
| `defaultdict(set)` | `set()`: grouping without repeats |

Reading also creates the key; check with `in` whether it exists.

## namedtuple

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x, p[0], p._replace(x=1), p._asdict()
```

## deque

| Code | What it does |
|---|---|
| `append(x)` / `appendleft(x)` | add on the right / left |
| `pop()` / `popleft()` | remove from the right / left |
| `deque(maxlen=n)` | at most n items, the old one drops |
| `rotate(k)` | rotate to the right |
| `d[0]`, `d[-1]` | look at the ends |

## ChainMap

`ChainMap(first, second, ...)`: searches for the key in order; writes go to
the first dictionary.
