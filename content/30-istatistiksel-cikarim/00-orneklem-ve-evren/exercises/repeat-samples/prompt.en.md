We cannot tell whether one sample was lucky. Draw 500 samples: `seed` from 0
to 499, each `users["minutes"].sample(n=50, random_state=seed)`. Collect the
means and print three numbers: the smallest mean, the largest mean (2
places) and the share that are **within 1 minute** of the true mean (3
places).

**Expected output:**

```text
6.84
11.98
0.75
```
