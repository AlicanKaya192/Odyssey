| Term | Meaning |
|---|---|
| Population | The whole group you are talking about |
| Sample | The part of the population you pick and measure |
| Parameter | A number computed from the population; usually unknown |
| Statistic | A number computed from the sample |
| Inference | Drawing conclusions about the population from a sample |
| Simple random sample | Everyone has the same chance of being picked |
| Sampling error | A statistic missing the parameter by chance |
| Bias | Missing in the same direction every time because of the selection |
| Simulation | Repeating an experiment thousands of times on a computer |

## Notation

| | Population | Sample |
|---|---|---|
| Size | $N$ | $n$ |
| Mean | $\mu$ | $\bar{x}$ |
| Share | $p$ | $\hat{p}$ |

## Sampling with pandas

```python
from ab_data import make_population

users = make_population()
sample = users.sample(n=100, random_state=1)   # 100 people, no repeats
part = users["minutes"].sample(n=50, random_state=2)
```

- With the same `random_state` the same people are picked; the result is
  reproducible.
- `replace=False` is the default: nobody is picked twice.
- With NumPy: `np.random.default_rng(seed).choice(values, size=n, replace=False)`.

## Keep in mind

- One sample's result is an estimate, not the truth itself.
- A bigger sample reduces chance, not bias.
