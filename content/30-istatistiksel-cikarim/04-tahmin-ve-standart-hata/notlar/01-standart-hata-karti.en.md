## Formulas

| Estimate | Standard error | Sample needed |
|---|---|---|
| Mean $\bar{x}$ | $\dfrac{s}{\sqrt{n}}$ | $n = \left(\dfrac{s}{SE}\right)^2$ |
| Proportion $\hat{p}$ | $\sqrt{\dfrac{\hat{p}(1-\hat{p})}{n}}$ | $n = \dfrac{\hat{p}(1-\hat{p})}{SE^2}$ |

## In code

```python
import numpy as np
from scipy import stats

x = np.array([4.1, 5.0, 5.6, 6.2, 6.9, 7.4, 8.0, 9.3, 11.2, 12.5])
print(round(x.std(ddof=1) / np.sqrt(len(x)), 4))
print(round(float(stats.sem(x)), 4))
```

```text
0.8532
0.8532
```

- `scipy.stats.sem` gives the standard error of the mean; it uses `ddof=1`
  by default.
- When computing by hand in NumPy, do not forget `ddof=1`.

## Reading rule

- The standard error is how much **the mean** wobbles; the spread of single
  values is the standard deviation.
- If you write "mean ± standard error" in a report, say which one it is; it
  gets confused with "± deviation".
- Roughly: the true mean is usually within 2 standard errors of the
  estimate. The exact form of this is the confidence interval of the next
  section.

## The square-root rule

| Sample | Standard error |
|---|---|
| $n$ | $SE$ |
| $4n$ | $SE / 2$ |
| $16n$ | $SE / 4$ |
| $100n$ | $SE / 10$ |
