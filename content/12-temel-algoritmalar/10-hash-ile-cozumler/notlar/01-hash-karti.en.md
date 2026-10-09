## What can be hashed?

| Type | Hashable? | Note |
|---|---|---|
| `int`, `float`, `bool` | yes | `hash(1) == hash(1.0) == hash(True)`: equal values, equal hashes |
| `str` | yes | a different seed on every run (fixed within a process) |
| `tuple` | yes if its contents are | `(1, [2])` cannot be hashed |
| `frozenset` | yes | the immutable form of a set; for sets of sets |
| `list`, `dict`, `set` | no | mutable; `TypeError: unhashable type` |
| Your own class | by default: by identity | for by-content, `__eq__` + `__hash__` |

## Costs

| Operation | Average | Worst |
|---|---|---|
| `d[k]`, `k in d`, `d[k] = v`, `del d[k]` | `O(1)` | `O(n)` (if everything falls in the same bucket) |
| `s.add(x)`, `x in s` | `O(1)` | `O(n)` |
| Building (`set(items)`) | `O(n)` | |

## Design questions

- **What should the key be?** Members of the same group must produce the same
  key, different ones different keys. Sorted letters for anagrams; `w.lower()`
  if case does not matter; a tuple for a two-field key.
- **Store a count or an index?** A counter for "how many times"; the first or
  last index for "where"; a list for "which ones".
- **Will memory suffice?** Every pattern needs `O(n)` extra memory. For
  billions of values, approximate structures (Bloom filter, Count-Min) come in
  the Algorithm Techniques module.

## Writing `__hash__`

```python
class Card:
    def __init__(self, rank, suit):
        self.rank, self.suit = rank, suit
    def __eq__(self, other):
        return (self.rank, self.suit) == (other.rank, other.suit)
    def __hash__(self):
        return hash((self.rank, self.suit))    # a tuple of the fields used in equality
```

The fields that go into the hash must **not change** later: if a field changes
while the object is in a dictionary, it stays in the wrong bucket and cannot
be found. `@dataclass(frozen=True)` gets this right by itself.
