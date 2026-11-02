Does the number of visits (`visits`) follow a Poisson distribution? For `k`
from 0 to 5, print on each line `k`, the real share
(`value_counts(normalize=True)`) and `pmf(k)` of a Poisson model with mean
`visits.mean()` (both with 3 places). On the last line print the mean and
the variance (pandas `var()`) with 2 places: in a Poisson they should be
equal.

**Expected output:**

```text
0 0.051 0.05
1 0.148 0.149
2 0.223 0.224
3 0.226 0.224
4 0.168 0.168
5 0.102 0.101
3.0 3.0
```
