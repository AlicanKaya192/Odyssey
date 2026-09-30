## Lags

```python
for k in (1, 7, 14, 28):
    X[f"lag{k}"] = y.shift(k)
```

Which lags? Those beyond the band in the ACF and PACF (Section 12), plus the
multiples of the season (7, 14, 28; 12, 24).

If you forecast `h` steps ahead, the smallest lag must be `h`.

## Windows

```python
past = y.shift(1)                         # shift first

X["mean7"] = past.rolling(7).mean()       # the recent level
X["mean28"] = past.rolling(28).mean()     # the long level
X["std7"] = past.rolling(7).std()         # recent volatility
X["max7"] = past.rolling(7).max()
X["trend"] = X["mean7"] - X["mean28"]     # is the level rising?
X["ewm"] = past.ewm(alpha=0.3, adjust=False).mean()
```

A seasonal window: past values of the same position.

```python
X["same_dow_4w"] = sum(y.shift(7 * i) for i in range(1, 5)) / 4
```

## Calendar

```python
X["dow"] = index.dayofweek
X["month"] = index.month
X["day"] = index.day
X["weekend"] = (index.dayofweek >= 5).astype(int)
X["holiday"] = index.isin(holiday_dates).astype(int)
```

| Model | How to give the day of the week |
|---|---|
| Tree-based | As a number (0–6) is enough; the tree finds the thresholds itself |
| Linear | **Dummy columns**: `pd.get_dummies(X["dow"], drop_first=True)` |

Giving a linear model the day of the week as a number 0–6 says "Sunday is six
times Monday". Turn it into dummy columns.

For cyclic variables (month, hour) use a sine and a cosine: December and
January stay neighbours.

## Transforming the target

| Transformation | Target | The way back | When |
|---|---|---|---|
| Difference | `y - y.shift(m)` | `+ lag_m` | A trending series, a tree-based model |
| Ratio | `y / y.shift(m)` | `× lag_m` | Multiplicative growth |
| Logarithm | `np.log(y)` | `np.exp` | A growing variance |
| Ratio to the level | `y / mean28` | `× mean28` | Many series on different scales |

It is good to write the features on the same base too: `lag1 - lag7`,
`mean7 - lag7`. That way the model never sees the raw level.

## Multi-step forecasts

**Recursive:**

```python
history = train.copy().astype(float)
for day in future_index:
    history.loc[day] = float("nan")
    row = features(history).loc[[day]]
    history.loc[day] = model.predict(row[columns])[0]
forecast = history.loc[future_index]
```

The table is rebuilt at every step; forecasts become the lags of the next
step. Errors accumulate; the future of external variables is needed for every
step.

**Direct, safe features:** shift every lag and window by at least `h`. One
model, one `predict`. It does not use the fresh information available for a
near horizon.

**A model per horizon:**

```python
models = {}
for h in (1, 7, 14, 28):
    target = y.shift(-h)                  # the value h days later (in training only)
    rows = X.join(target.rename("target")).dropna()
    models[h] = Model().fit(rows[columns], rows["target"])
```

Here `shift(-h)` is not leakage: it defines the target, not a feature. Each
horizon uses the freshest information it has; the price is `h` models.

## Many series, one model

With hundreds of products, add the features to the long-format table
(Section 08) **per series**:

```python
long["lag7"] = long.groupby("store")["sales"].shift(7)
long["mean28"] = (long.groupby("store")["sales"]
                      .transform(lambda v: v.shift(1).rolling(28).mean()))
```

Without `groupby`, `shift` carries the last row of one shop into the first row
of the next. The shop identifier becomes a feature too; if the scales differ,
make the target a ratio to the level.

## Checklist

1. Does every feature come from at least the horizon back, via `shift`?
2. Is there a `shift` before `rolling`, `ewm`, `expanding`?
3. Were scaling, encoding and filling `fit` on the training data only?
4. Is the validation by time?
5. Is the test **after** the training, and is a gap as long as the horizon
   needed (`gap`)?
6. Is the difference between the training and the test error reasonable?
7. What does the baseline give on the same rig?
