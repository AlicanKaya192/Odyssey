In a discrete distribution `cdf(k)` means "$k$ and below, included", `sf(k)`
means "above $k$, **excluding** it". The wording of the question decides
which call to write:

| Wording | Maths | scipy |
|---|---|---|
| at most 3 | $X \le 3$ | `cdf(3)` |
| fewer than 3 | $X \le 2$ | `cdf(2)` |
| at least 3 | $X \ge 3$ | `sf(2)` |
| more than 3 | $X \ge 4$ | `sf(3)` |
| exactly 3 | $X = 3$ | `pmf(3)` |
| between 2 and 5 (both included) | $2 \le X \le 5$ | `cdf(5) - cdf(1)` |

## Check by measuring

```python
from scipy import stats

buyers = stats.binom(n=20, p=0.114)
print(round(float(buyers.sf(2)), 4))
print(round(float(1 - buyers.cdf(2)), 4))
print(round(float(sum(buyers.pmf(k) for k in range(3, 21))), 4))
```

```text
0.403
0.403
0.403
```

All three ask the same question ("at least 3"): `sf(2)`, `1 - cdf(2)` and the
sum of the single probabilities from 3 to 20.

## In a continuous distribution the boundary does not matter

In a normal distribution $X < 1000$ and $X \le 1000$ give the same
probability, because a single point has probability zero. The trap exists
only in discrete distributions (binomial, Poisson).

## A checking habit

If in doubt, compute the boundary value separately: if `pmf(k)` is not
small, including it or not changes the result noticeably.
