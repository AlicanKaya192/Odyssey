# statsmodels: GLMs and Formulas

In the previous section we built the model with arrays using `sm.OLS(y, X)`:
we added the constant column by hand, and a text column would have had to be
turned into numbers by us as well. statsmodels' second interface is the
**formula**: you write the model as a sentence, as in the R language
(`"price ~ area + C(city)"`), and the library does the rest. This section
covers the formula language, categorical columns, interactions and the
generalised forms of linear regression (GLMs): logistic for a yes/no
outcome, Poisson for a count outcome.

## OLS with a formula

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

rng = np.random.default_rng(11)
df = pd.DataFrame({
    "area": rng.uniform(50, 200, 300).round(),
    "city": rng.choice(["Ankara", "Izmir", "Istanbul"], 300),
    "age": rng.uniform(0, 40, 300).round(),
})
bonus = df["city"].map({"Ankara": 0, "Izmir": 40, "Istanbul": 120})
noise = rng.normal(0, 30, 300)
df["price"] = 50 + 3 * df["area"] - 2 * df["age"] + bonus + noise
res = smf.ols("price ~ area + age + C(city)", data=df).fit()
for name, value in res.params.items():
    print(f"{name:20} {value:8.2f}")
```

```text
Intercept               40.57
C(city)[T.Istanbul]    118.14
C(city)[T.Izmir]        43.82
area                     3.04
age                     -1.88
```

- `smf.ols(formula, data=df)`: left of `~` is the target, right are the
  explanatory columns. Columns are taken from the DataFrame by name, and **the
  constant term is added automatically** (`Intercept`).
- `C(city)` means "this column is categorical". The formula turns it into
  dummy columns: `C(city)[T.Istanbul]`, `C(city)[T.Izmir]`. Ankara is the
  **base** (first alphabetically): the other cities' coefficients are
  differences from Ankara.
- The differences that made the data are Izmir 40, Istanbul 120; the model
  found 43.82 and 118.14.

## Changing the base and predicting

```python
formula = "price ~ area + age + C(city, Treatment('Istanbul'))"
other = smf.ols(formula, data=df).fit()
print(other.params.filter(like="T.").round(2).tolist())
new = pd.DataFrame({"area": [100], "age": [10], "city": ["Izmir"]})
print(res.predict(new).round(1).tolist())
```

```text
[-118.14, -74.32]
[370.1]
```

- `Treatment('Istanbul')` makes Istanbul the base: now Ankara is −118.14,
  Izmir −74.32 (relative to Istanbul; `filter(like="T.")` picked only the
  city rows). The model is the same, only the way of reading changed; the
  `area` and `age` coefficients stayed the same.
- For prediction the new data is given **raw**: the city name as text. The
  formula applies the encoding it learned in training to the new row itself;
  no `add_constant` or dummy columns are needed.

## Interactions and transformations

```python
extra = 1.5 * df["area"] * (df["city"] == "Istanbul")  # the Istanbul extra
df["price2"] = 50 + 3 * df["area"] + extra - 2 * df["age"] + rng.normal(0, 30, 300)
inter = smf.ols("price2 ~ area * C(city) + age", data=df).fit()
print({k: round(v, 2) for k, v in inter.params.items() if "area" in k})
curve = smf.ols("price ~ area + I(area ** 2) + np.log(age + 1)", data=df).fit()
print(curve.model.exog_names)
```

```text
{'area': 3.04, 'area:C(city)[T.Istanbul]': 1.49, 'area:C(city)[T.Izmir]': -0.02}
['Intercept', 'area', 'I(area ** 2)', 'np.log(age + 1)']
```

- This time a square metre is **more expensive** in Istanbul: 4.5 per unit of
  area instead of 3. `area * C(city)` adds both the separate effects and the
  **interaction** (`area:C(city)[T.Istanbul]`): "does the effect of area
  change with the city?" The model found a difference of 1.49 (truly 1.5);
  −0.02 for Izmir, that is no difference.
- The operation inside `I(...)` is computed as it is: `I(area ** 2)` is the
  squared column. (Without `I`, `**` means something else in a formula.)
  NumPy functions like `np.log(...)` are written directly too.

## Logistic regression: smf.logit

```python
from sklearn.linear_model import LogisticRegression

score = rng.normal(0, 1, 1000)
premium = rng.integers(0, 2, 1000)
chance = 1 / (1 + np.exp(-(-1 + 0.8 * score + 1.2 * premium)))
d2 = pd.DataFrame({"y": (rng.random(1000) < chance).astype(int),
                   "score": score, "premium": premium})
logit = smf.logit("y ~ score + premium", data=d2).fit(disp=0)
print({k: round(v, 3) for k, v in logit.params.items()})
print({k: round(v, 2) for k, v in np.exp(logit.params).items()})
sk = LogisticRegression().fit(d2[["score", "premium"]], d2["y"])
print(sk.coef_.round(3).tolist())
```

```text
{'Intercept': -1.03, 'score': 0.746, 'premium': 1.22}
{'Intercept': 0.36, 'score': 2.11, 'premium': 3.39}
[[0.739, 1.194]]
```

- `smf.logit` is the model for a 0/1 outcome; `disp=0` silences the training
  messages. The coefficients are close to those that made the data (0.746
  and 1.22; truly 0.8 and 1.2).
- A logistic coefficient is a log odds ratio; `np.exp` turns it into an
  **odds ratio**: with a premium membership the odds of the event are 3.39
  times higher. One unit more `score`, 2.11 times.
- scikit-learn's `LogisticRegression` is a little different on the same data
  (0.739, 1.194): by default it is **penalised** (`C=1`) and pulls the
  coefficients towards zero. If coefficients are wanted for interpretation,
  use statsmodels (or `C=np.inf`).

## A count outcome: Poisson GLM

An insurance company studies the number of claims per customer. Customers
were insured for different lengths of time (10–365 days); someone insured
longer naturally reports more claims.

```python
days = rng.integers(10, 365, 500)
risk = rng.normal(0, 1, 500)
claims = rng.poisson(np.exp(-4 + 0.5 * risk) * days)
d3 = pd.DataFrame({"claims": claims, "risk": risk, "days": days})
poisson = sm.families.Poisson()
fair = smf.glm("claims ~ risk", data=d3, family=poisson,
               offset=np.log(d3["days"])).fit()
naive = smf.glm("claims ~ risk", data=d3, family=poisson).fit()
print({k: round(v, 3) for k, v in fair.params.items()})
print({k: round(v, 3) for k, v in naive.params.items()})
print(round(np.exp(fair.params["risk"]), 3))
line = smf.ols("claims ~ risk", data=d3).fit()
print(int((line.fittedvalues < 0).sum()))
```

```text
{'Intercept': -4.009, 'risk': 0.496}
{'Intercept': 1.283, 'risk': 0.44}
1.642
4
```

- `smf.glm(..., family=Poisson())`: the outcome is a count (0, 1, 2, ...) and
  the model builds the **logarithm of the mean** count linearly. That is why
  a prediction is never negative.
- `offset=np.log(days)` says "each customer was observed for a different
  time"; the model learns the daily **rate**. The coefficients are the same
  as those that made the data: −4.009 and 0.496 (truly −4 and 0.5).
- When the offset is forgotten, the constant is entirely wrong (1.283) and
  the risk coefficient is 0.44: the time information leaks elsewhere.
- `np.exp(0.496)` = 1.642: one unit more risk raises the claim **rate** by
  64% (a rate ratio).
- Plain linear regression on the same data predicts a **negative** number of
  claims for 4 customers.

## Summary

- Formula: `smf.ols("y ~ a + b + C(c)", data=df)`; the constant is automatic,
  categorical `C()`, the base `Treatment('...')`.
- Interaction `a * C(c)` (`a:C(c)` only the interaction), transformation
  `I(a ** 2)`, `np.log(a)`.
- A yes/no outcome: `smf.logit`; `np.exp(params)` is the odds ratio.
- A count outcome: `smf.glm(..., family=sm.families.Poisson())`; with
  different observation times, `offset=np.log(time)`.
