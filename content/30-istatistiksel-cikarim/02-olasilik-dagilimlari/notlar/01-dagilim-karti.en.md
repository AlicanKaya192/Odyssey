## Building a distribution object

```python
from scipy import stats

buyers = stats.binom(n=20, p=0.114)      # discrete
visits = stats.poisson(mu=3.0)           # discrete
load = stats.norm(loc=850, scale=120)    # continuous
wait = stats.expon(scale=10)             # continuous, mean 10
```

## The same methods on every distribution

| Method | Question | Note |
|---|---|---|
| `pmf(k)` | the probability of exactly `k` | discrete only |
| `pdf(x)` | the density at `x` | continuous only; not a probability |
| `cdf(x)` | `x` or less | cumulative |
| `sf(x)` | more than `x` | `1 - cdf(x)`, more precise for small probabilities |
| `ppf(q)` | the value with `q` below it | the inverse of `cdf` |
| `mean()`, `std()` | expected value, deviation | |
| `rvs(size, random_state)` | a random sample | reproducible with a seed |

## Which distribution?

| Situation | Distribution |
|---|---|
| $n$ independent yes/no trials | binomial |
| A single yes/no | Bernoulli (`stats.bernoulli(p)`) |
| How many events in a period | Poisson |
| Time between two events | exponential (`stats.expon`) |
| A symmetric, bell-shaped measurement | normal |
| Every value equally likely | uniform (`stats.uniform`) |

## Formulas

- Binomial: mean $np$, deviation $\sqrt{np(1-p)}$.
- Poisson: mean and variance $\lambda$.
- Normal: the 68% / 95% / 99.7% rule; exactly 95% within $\pm 1.96\,\sigma$.
