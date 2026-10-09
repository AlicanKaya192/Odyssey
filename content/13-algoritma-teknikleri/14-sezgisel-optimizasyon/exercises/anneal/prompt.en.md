Write the function `anneal(x, seed)`: it searches for where `f` is smallest
with simulated annealing and returns the best `x` found, `round(..., 2)`.
`rng = random.Random(seed)`, `temp = 20.0`, 3000 steps. At each step **in this
order**:

- `cand = x + rng.uniform(-3, 3)`, `delta = f(cand) - f(x)`
- accept if `delta < 0`; otherwise accept if `rng.random() < math.exp(-delta / temp)`
- if `f(x) < f(best)`, `best = x`; then `temp *= 0.998`

**Expected output:**

```
0 -1.54
1 -1.54
2 -1.54
3 -1.54
```
