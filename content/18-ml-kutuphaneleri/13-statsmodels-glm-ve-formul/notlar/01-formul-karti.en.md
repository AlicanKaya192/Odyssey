## The formula language

| Code | Meaning |
|---|---|
| `y ~ a + b` | `y` from `a` and `b`; the constant is automatic |
| `y ~ a + b - 1` | no constant |
| `C(c)` | categorical (dummy columns) |
| `C(c, Treatment('X'))` | base category `X` |
| `a:b` | the interaction only |
| `a * b` | `a + b + a:b` |
| `I(a ** 2)`, `I(a / 1000)` | the operation as it is |
| `np.log(a)`, `np.sqrt(a)` | NumPy functions |
| `Q("my col")` | a column with a space in its name |

## Models

| Code | Outcome type |
|---|---|
| `smf.ols(f, data)` | a continuous number |
| `smf.logit(f, data)` | 0/1; `np.exp(params)` is the odds ratio |
| `smf.glm(f, data, family=sm.families.Poisson())` | a count; `offset=np.log(time)` |
| `smf.glm(f, data, family=sm.families.NegativeBinomial(alpha=1.0))` | an overdispersed count |
| `smf.glm(f, data, family=sm.families.Binomial())` | 0/1 the GLM way (same as logit) |
| `smf.glm(f, data, family=sm.families.Gamma(link=sm.families.links.Log()))` | positive, right-skewed (amounts) |

## Reading a coefficient

| Model | `exp(coefficient)` |
|---|---|
| OLS | not needed: change per unit |
| Logit | odds ratio |
| Poisson / neg. binomial | rate ratio |
| Gamma with a log link | a multiplier of the mean |

## Rules

- For prediction the new data is given raw; the formula applies the encoding
  itself.
- `.fit(disp=0)` silences logit/negative binomial training messages.
- In a count model, do not forget the `offset` when observation times
  differ.
