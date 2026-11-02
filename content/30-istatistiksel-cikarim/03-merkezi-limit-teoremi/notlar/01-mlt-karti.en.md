## The theorem in one line

The mean of $n$ independently picked values is approximately normally
distributed as $n$ grows:

$$\bar{X} \approx N\!\left(\mu,\ \dfrac{\sigma}{\sqrt{n}}\right)$$

## Standard errors

| What | Standard error |
|---|---|
| Mean | $\dfrac{\sigma}{\sqrt{n}}$ |
| Proportion | $\sqrt{\dfrac{p(1-p)}{n}}$ |

## What it says and what it does not

| Says | Does not say |
|---|---|
| The distribution of means approaches a bell | The data itself becomes normal |
| The means are centred on $\mu$ | One sample's mean equals $\mu$ |
| The width shrinks with $\sqrt{n}$ | A given $n$ is enough for any data |

## When fast, when slow?

- For symmetric data a few dozen people are enough.
- For moderately skewed data (session length) the bell is clear with tens of
  people.
- For very skewed data (spend: mostly zero, a few very large) thousands may
  be needed.
- Check: draw sample means by simulation, look at the two tails separately.

## Code pattern

```python
import numpy as np

rng = np.random.default_rng(0)
values = rng.exponential(scale=10, size=50_000)
means = rng.choice(values, size=(5000, 40)).mean(axis=1)
se_formula = values.std() / np.sqrt(40)
print(round(means.std(), 3), round(se_formula, 3))
```

```text
1.577 1.589
```

Both numbers measure the same thing: one from simulation, one from the
formula.
