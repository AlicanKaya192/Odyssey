## CUPED in three lines

```python
import numpy as np
import statsmodels.formula.api as smf
from ab_data import make_engagement_test

test = make_engagement_test()
y = test["minutes"].to_numpy()
x = test["pre_minutes"].to_numpy()
theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
test["adjusted"] = y - theta * (x - x.mean())
test["b"] = (test["group"] == "B").astype(int)
diff = test.groupby("b")["adjusted"].mean().diff().iloc[-1]
model = smf.ols("minutes ~ b + pre_minutes", data=test).fit()
print(round(diff, 3), round(model.params["b"], 3))
```

```text
1.04 1.04
```

The second number asks the same question with a regression:
`pre_minutes` is a covariate in the model. CUPED is this regression done
by hand; the results come out almost the same.

## How large is the gain?

The remaining variance is about 1 − ρ²:

| ρ (before and during) | remaining variance |
|---|---|
| 0.3 | 0.91 |
| 0.5 | 0.75 |
| 0.7 | 0.51 |
| 0.9 | 0.19 |

If ρ is around 0.3 the gain is small; the same metric's earlier value
usually gives the highest correlation.

## Checklist

- Was X measured **before** assignment?
- Is X balanced across the two groups? (the balance check from the A/A
  Tests and Sample Ratio Mismatch section)
- What will X be for new users with no earlier data? (the next note)
- Was θ computed from the two groups' data together?
