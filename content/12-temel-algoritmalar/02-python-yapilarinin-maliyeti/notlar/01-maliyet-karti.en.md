The average cost of common operations on Python's built-in structures. `n`
is the number of elements in the structure, `k` the part the operation
touches.

## List (`list`)

| Operation | Cost |
|---|---|
| `items[i]`, `items[i] = x` | `O(1)` |
| `len(items)` | `O(1)` |
| `items.append(x)` | `O(1)` amortised |
| `items.pop()` (from the end) | `O(1)` |
| `items.insert(0, x)`, `items.pop(0)` | `O(n)` |
| `x in items`, `items.index(x)`, `items.count(x)` | `O(n)` |
| `items.remove(x)` | `O(n)` |
| `items[a:b]` (slice) | `O(k)` |
| `min`, `max`, `sum` | `O(n)` |
| `items.sort()`, `sorted(items)` | `O(n log n)` |
| `items.reverse()` | `O(n)` |

## Dictionary (`dict`) and set (`set`)

| Operation | Cost |
|---|---|
| `d[key]`, `d[key] = v`, `del d[key]` | `O(1)` average |
| `key in d`, `x in s` | `O(1)` average |
| `s.add(x)`, `s.discard(x)` | `O(1)` average |
| `d.get(key, default)` | `O(1)` average |
| Building `set(items)`, `dict(...)` | `O(n)` |
| <code>a &amp; b</code>, <code>a &#124; b</code> (intersection, union) | roughly `O(len(a) + len(b))` |
| Going over all elements | `O(n)` |

The word "average" matters: with very badly spread hashes the worst case can
be `O(n)`, but with Python's built-in types you practically never meet it.

## `collections.deque`

| Operation | Cost |
|---|---|
| `append`, `appendleft` | `O(1)` |
| `pop`, `popleft` | `O(1)` |
| `items[i]` (in the middle) | `O(n)` |
| The last `k` elements with `deque(maxlen=k)` | `O(1)` to add, the oldest drops off by itself |

## String (`str`)

| Operation | Cost |
|---|---|
| `s[i]`, `len(s)` | `O(1)` |
| `sub in s`, `s.find(sub)` | worst `O(len(s) × len(sub))` |
| `s + t` | `O(len(s) + len(t))`: a new string is built |
| `"".join(parts)` | `O` of the total length |
| `s.split()`, `s.replace(...)` | `O(len(s))` |

## Three sentences to remember

1. If you will ask "is it in there?" many times, build a set or a dict.
2. If you will remove from the front, use a `deque`.
3. Multiply the cost of every one-line call inside a loop by the number of
   rounds.
