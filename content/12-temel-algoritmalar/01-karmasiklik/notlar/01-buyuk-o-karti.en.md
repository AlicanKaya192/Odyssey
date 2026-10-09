## Classes (fast to slow)

| Big O | Work when the input doubles | Typical code |
|---|---|---|
| `O(1)` | stays the same | indexing, a formula |
| `O(log n)` | grows by 1 step | a loop that halves every round |
| `O(n)` | doubles | a single loop |
| `O(n log n)` | a little more than doubles | an efficient sort |
| `O(n²)` | quadruples | two nested loops |
| `O(n³)` | grows eightfold | three nested loops |
| `O(2ⁿ)` | gets squared | trying every subset |

"When the input doubles, how many times bigger does the work get?" is the
most practical way to find an algorithm's class by measuring.

## Simplification rules

- `5n + 3` → `O(n)` (the constant factor and the constant term go)
- `n² + 100n` → `O(n²)` (the smaller term goes)
- `n + log n` → `O(n)`
- `3` → `O(1)`
- With two separate inputs both stay: `len(a) × len(b)` → `O(a·b)`

## Reading the code

```python
for x in items:          # n rounds
    print(x)             # 1 step       → O(n)

for x in items:          # n rounds
    for y in items:      # n each round → O(n²)
        ...

while n > 1:             # halved every round
    n //= 2              #              → O(log n)

for x in items:          # O(n)
    ...
for x in items:          # O(n)
    for y in items:      # O(n²)
        ...              # total O(n + n²) = O(n²)
```

## Things to watch

- **Hidden loops:** `x in a_list`, `a_list.index(x)`, `a_list.count(x)`,
  `sum(a_list)`, `max(a_list)` are one line each but each is `O(n)`. Used
  inside a loop, the total becomes `O(n²)`. (The topic of the next section.)
- **An early exit does not change the worst case:** leaving the loop early
  with `return` speeds up the best case; the worst case is still `O(n)`.
- **Big O hides the constant:** on small inputs an `O(n²)` algorithm can be
  faster than an `O(n log n)` one with a large constant. Big O answers
  "what happens on large input".
