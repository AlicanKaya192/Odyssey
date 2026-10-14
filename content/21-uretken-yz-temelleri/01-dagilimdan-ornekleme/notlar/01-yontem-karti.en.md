| Method | When | With NumPy | Watch out |
|---|---|---|---|
| **Categorical** | A finite number of options (word, token, class) | `np.searchsorted(np.cumsum(p), u, side="right")` or `rng.choice(k, p=p)` | The probabilities must sum to 1 |
| **Inverse transform** | A distribution whose cumulative function can be inverted | Exponential: `-np.log(1 - u) / rate` | Not every distribution has a formula |
| **Rejection** | Any shape whose density can be computed | `x[height < f(x)]` | Slow if the acceptance rate is low |
| **Histogram** | When you only have data | `np.histogram` + `rng.choice` + `rng.uniform` | Does not go beyond the observed range |
| **Monte Carlo** | Estimating a probability or a mean | `(samples > limit).mean()` | Only as right as the model |

**Seed and generator:**

```python
rng = np.random.default_rng(42)   # one generator, fixed seed
u = rng.random(5)                 # uniform numbers between 0 and 1
```

- The **order** of the calls made on the same generator changes the result:
  drawing `x` first and `height` second gives different numbers from the
  reverse.
- The old `np.random.seed(...)` + `np.random.rand(...)` style uses a single
  global generator that affects the whole program. New code prefers
  `default_rng`.

**The law of large numbers:** as the number of samples grows, the shares
approach the true probabilities. In this section `this` (0.10) never came up
in 20 draws; with 100,000 draws the shares settled exactly.
