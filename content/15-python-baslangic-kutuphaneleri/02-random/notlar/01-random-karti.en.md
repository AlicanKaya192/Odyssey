## Producing numbers

| Function | What it gives |
|---|---|
| `random()` | a decimal in `[0, 1)` |
| `uniform(a, b)` | a decimal between `a` and `b` |
| `randint(a, b)` | an integer between `a` and `b`, **both included** |
| `randrange(a, b, step)` | one value of `range(a, b, step)`; `b` excluded |
| `gauss(mu, sigma)` | the normal distribution |
| `expovariate(lambd)` | the exponential distribution (waiting times) |

## Picking and shuffling

| Function | What it does | Repeats possible? |
|---|---|---|
| `choice(xs)` | a single element | — |
| `choices(xs, weights=..., k=n)` | `n` picks | yes (with replacement) |
| `sample(xs, n)` | `n` different elements | no |
| `shuffle(xs)` | shuffles the list in place, returns `None` | — |

## Reproducibility

- `random.seed(n)`: sets the shared generator (the whole program is
  affected).
- `r = random.Random(n)`: a separate generator only you use; preferred in
  tests and experiments.
- Same seed + same order of calls = same result. Inserting one call changes
  every number after it.

## Common mistakes

- Assigning the result of `shuffle`: `x = random.shuffle(xs)` → `x` is
  `None`. If you need a shuffled **copy**, use `r.sample(xs, len(xs))`.
- Forgetting that 6 is included in `randint(1, 6)`; in `randrange(1, 6)` 6 is
  excluded.
- Using `random` in security-sensitive code: use `secrets`.
