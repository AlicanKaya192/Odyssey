## Python's `random` module

| Job | How | Note |
|---|---|---|
| Seed | `random.seed(42)` | same seed, same sequence |
| One choice | `random.choice(xs)` | |
| `k` items without replacement | `random.sample(xs, k)` | no item comes twice |
| `k` items with replacement | `random.choices(xs, k=k)` | weights can be given too: `weights=` |
| Shuffle in place | `random.shuffle(xs)` | Fisher-Yates, returns `None` |
| Integer | `random.randint(a, b)` | `b` **included** |
| Fraction | `random.random()` | `0 <= x < 1` |

In NumPy: `rng = np.random.default_rng(42)`, then `rng.integers`,
`rng.choice`, `rng.permutation`. In scikit-learn, `random_state=42`.

## Algorithms

| Algorithm | Kind | Cost |
|---|---|---|
| Quickselect (random pivot) | Las Vegas | `O(n)` on average |
| Fisher-Yates | | `O(n)` |
| Reservoir sampling | | `O(n)` time, `O(k)` memory |
| Monte Carlo estimate | Monte Carlo | error like `1/√n` |

## Common mistakes

- `xs = random.shuffle(xs)`: `shuffle` changes the list in place and returns
  `None`; `xs` is now `None`.
- `randint(0, len(xs))`: the upper bound is included, so one too many, an index
  error.
- Choosing each position from the whole list when shuffling: a biased shuffle.
- Setting the seed inside the loop: the same "random" number every round.
- Reading a random result from a single trial: in Monte Carlo a single trial
  carries luck; look at the average of a few repeats.
