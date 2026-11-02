`needed_n(sigma, target)` should return the sample size needed to bring the
standard error down to `target`: `(sigma / target) ** 2`, rounded **up**
(`math.ceil`). The starter code forgot to square.

**Expected output:**

```text
151
144
```
