## Infinite

| Function | Example | Result |
|---|---|---|
| `count(10, 5)` | `islice(..., 3)` | 10, 15, 20 |
| `cycle("AB")` | `islice(..., 3)` | A, B, A |
| `repeat("x", 3)` | | x, x, x |

## Slicing and filtering

| Function | What it does |
|---|---|
| `islice(it, n)` / `islice(it, a, b)` | the first n / from a to b |
| `takewhile(cond, it)` | take while it holds, stop at the first break |
| `dropwhile(cond, it)` | skip while it holds, then everything |
| `filterfalse(cond, it)` | the ones failing the condition |
| `compress(it, selector)` | the ones true in the selector |

## Joining and splitting

| Function | What it does |
|---|---|
| `chain(a, b, ...)` | end to end |
| `chain.from_iterable(lists)` | flattens a list of lists |
| `zip_longest(a, b, fillvalue=)` | pairs, filling the shorter one |
| `pairwise(x)` | consecutive pairs |
| `batched(x, n)` | pieces of n |
| `accumulate(x, op)` | running results |
| `groupby(x, key=)` | **neighbours** with the same key |
| `tee(it, n)` | n copies of one iterator |

## Combinatorics

| Function | Count for `"ABC"`, 2 |
|---|---|
| `product("ABC", repeat=2)` | 9 |
| `permutations("ABC", 2)` | 6 |
| `combinations("ABC", 2)` | 3 |
| `combinations_with_replacement("ABC", 2)` | 6 |

## Remember

- The results are iterators: `list(...)` to see them; they run out once.
- Never `list(...)` an infinite iterator; limit it with `islice`.
- `sorted` by the same key before `groupby`.
