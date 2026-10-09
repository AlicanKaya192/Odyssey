A high R² does not show that the model has the right shape. The **residuals**
(`y − ŷ`) should be scattered randomly; if there is a pattern, the model is
missing something. Let us fit a line to a curved relation:

```python
import numpy as np

rng = np.random.default_rng(4)
x = np.sort(rng.uniform(0, 10, 90))
y = 2 + 0.5 * x ** 2 + rng.normal(0, 2, 90)       # curved in reality
A = np.column_stack([np.ones(90), x])
w = np.linalg.lstsq(A, y, rcond=None)[0]
resid = y - A @ w
r2 = 1 - (resid ** 2).sum() / ((y - y.mean()) ** 2).sum()
print(round(r2, 3))
for part in np.array_split(resid, 3):              # left, middle, right
    print(round(part.mean(), 2))
```

```text
0.941
1.62
-3.27
1.65
```

R² looks high, but the residuals follow a pattern: positive on the left and
right, negative in the middle. The line stays below the curve at the ends and
above it in the middle. The fix is to add the feature `x²` to the model.
Plotting the residuals against `x` or the prediction (or looking at the means
of parts like this) is the first thing to do after any regression.
