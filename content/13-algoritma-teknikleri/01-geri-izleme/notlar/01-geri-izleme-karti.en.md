## The skeleton

```python
result, path = [], []

def backtrack(STATE):
    if IS_COMPLETE:
        result.append(path[:])        # a copy!
        return
    for choice in CHOICES:
        if CANNOT_WORK(choice):       # pruning
            continue                  # or, if sorted: break
        path.append(choice)           # choose
        backtrack(NEW_STATE)          # explore
        path.pop()                    # undo
```

## How many possibilities?

| Problem | Count | `n = 10` | Ready-made |
|---|---|---|---|
| Subsets | `2ⁿ` | 1024 | `combinations(items, k)` for every `k` |
| Orderings | `n!` | 3,628,800 | `permutations(items)` |
| Choices of `k` elements | `n! / (k!(n−k)!)` | `k = 3`: 120 | `combinations(items, k)` |
| `m` options at each position | `mⁿ` | `m = 3`: 59,049 | `product(options, repeat=n)` |

## Questions for pruning

- If I passed a limit on sorted data, will the next ones pass it too? →
  `break`.
- Does this choice break a rule (same column, same number)? → `continue`.
- Can even the best of the remaining options not beat the current best? →
  return (branch and bound).
- If a value appears twice, am I opening the same branch twice? → sort and
  `if i > start and items[i] == items[i - 1]: continue`.

## Common mistakes

- `result.append(path)`: all of them point to the same list and end up
  empty. Write `path[:]` or `list(path)`.
- When undoing, only doing `path.pop()` and forgetting `used[i] = False` or
  removing from the set → the next branches run with the wrong constraint.
- A list as a default value: `def f(path=[])` shares the same list across all
  calls.
- Pruning with `break` without sorting: if the data is not sorted the next
  element may be smaller, and solutions are lost.
